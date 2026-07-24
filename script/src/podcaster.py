import os
import asyncio
import logging
from openai import OpenAI
import edge_tts
from src.network_safety import configured_http_proxy
from src.paths import PaperBrainPaths

try:
    import nest_asyncio
    nest_asyncio.apply()
except Exception:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Podcaster:
    def __init__(self, config, provider='doubao', prompts=None):
        self.config = config
        self.provider = provider
        self.prompts = prompts or {}
        paths = PaperBrainPaths.from_config_dict(config)
        self.output_dir = os.path.join(str(paths.vault_path), "Podcasts")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Setup Client
        if provider == 'openrouter':
            self.api_key = config['openrouter']['api_key']
            self.base_url = "https://openrouter.ai/api/v1"
            self.model_pro = config['openrouter'].get('model_podcast', config['openrouter'].get('model_pro', 'moonshotai/kimi-k3'))
        else:
            self.api_key = config['doubao']['api_key']
            self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
            self.model_pro = config['doubao'].get('model_pro', 'doubao-seed-2-0-pro-260215')

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=120.0  # Increased timeout for long script generation
        )

    def _openrouter_model_candidates(self, primary_model: str):
        if self.provider != 'openrouter':
            return [primary_model]

        cfg = self.config.get('openrouter', {})
        fallbacks = cfg.get('model_podcast_fallbacks', cfg.get('model_pro_fallbacks', []))
        if not isinstance(fallbacks, list):
            fallbacks = []

        defaults = [
            "moonshotai/kimi-k3",
            "x-ai/grok-4.5",
            "qwen/qwen3.7-max",
            "z-ai/glm-5.2",
            "minimax/minimax-m3",
            "deepseek/deepseek-v4-pro",
        ]

        candidates = []
        for m in [primary_model, *fallbacks, *defaults]:
            if m and m not in candidates and not self._is_disallowed_openrouter_model(m):
                candidates.append(m)
        return candidates

    @staticmethod
    def _is_disallowed_openrouter_model(model):
        value = str(model or "").strip().lower().lstrip("~")
        author = value.split("/", 1)[0] if "/" in value else ""
        return author in {"anthropic", "openai", "google", "google-ai", "googleai"} or any(
            term in value for term in ("claude", "gpt", "openai", "gemini")
        )

    def generate_script(self, paper_title, analysis_content, rag_context="", duration_minutes=5):
        """Generates a podcast script based on the paper analysis and RAG context."""
        duration_minutes = max(1, int(duration_minutes))
        target_words_min = duration_minutes * 130
        target_words_max = duration_minutes * 170

        system_prompt = self.prompts.get('podcast', {}).get('system', "You are an expert science communicator.")
        user_template = self.prompts.get('podcast', {}).get('script_user', """
        You are a professional tech podcaster (like Lex Fridman or a specialized AI researcher host).
        Your task is to create a script for a **detailed "Deep Dive" audio segment** (target duration: ~{duration_minutes} minutes).

        Topic: {paper_title}

        Deep Analysis Report:
        {analysis_content}

        Context from Knowledge Base (RAG):
        {rag_context}

        **Tone & Style**:
        - **Natural & Conversational**: Use fillers occasionally ("you know", "right?"), rhetorical questions, and varied sentence structures. Avoid sounding robotic or like a news anchor.
        - **Enthusiastic but Critical**: Be genuinely excited about the innovation but maintain a healthy skepticism about limitations.
        - **Storytelling**: Frame the research as a narrative. What was the struggle before this? What is the hero (the new method)? What is the climax (the results)?

        **Structure (Aim for ~{target_words_min}-{target_words_max} words for {duration_minutes} mins)**:
        1. **The Hook**: Start with a provocative question or a real-world scenario that this technology solves.
        2. **The "Status Quo"**: Explain why previous methods failed. Use analogies (e.g., "It's like trying to teach a cat calculus...").
        3. **The Breakthrough (The "Meat")**: Deep dive into the technical innovation. Don't just list features; explain the *intuition*.
        4. **The Connection (RAG)**: Weave in the related work naturally. "This is actually a fascinating pivot from what we saw in [Related Paper X]..."
        5. **The Critique**: Honest assessment of where it breaks.
        6. **The Outro**: A philosophical or forward-looking conclusion.

        **Format**: Write ONLY the spoken text. Do not include [Sound Effect] or [Host] labels. Just the monologue script.
        **Language**: English only.
        """)
        prompt = user_template.format(
            duration_minutes=duration_minutes,
            paper_title=paper_title,
            analysis_content=analysis_content,
            rag_context=rag_context,
            target_words_min=target_words_min,
            target_words_max=target_words_max,
        )

        try:
            extra_params = {}
            if self.provider == 'openrouter':
                 extra_params['extra_headers'] = {
                    "HTTP-Referer": "https://paperbrain.ai",
                    "X-Title": "PaperBrain"
                 }
                 extra_body = {
                    "provider": {
                        "sort": self.config.get('openrouter', {}).get("routing_sort", "throughput"),
                        "data_collection": self.config.get('openrouter', {}).get("routing_data_collection", "deny"),
                        "allow_fallbacks": True,
                        "require_parameters": False,
                    }
                 }
                 effort = self.config.get('openrouter', {}).get("reasoning_effort_analysis")
                 if effort:
                    extra_body['reasoning'] = {"effort": effort}
                 extra_params['extra_body'] = extra_body

            models = self._openrouter_model_candidates(self.model_pro)
            last_err = None
            for model in models:
                try:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        **extra_params
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    msg = str(e)
                    last_err = e
                    if self.provider == 'openrouter' and (
                        "not available in your region" in msg
                        or "Error code: 403" in msg
                        or "Error code: 404" in msg
                    ):
                        logger.warning(f"[WARN] OpenRouter model failed, trying fallback: {model} ({msg})")
                        continue
                    raise
            raise last_err
        except Exception as e:
            logger.error(f"Error generating podcast script: {e}")
            return ""

    async def _synthesize_audio(self, text, output_path):
        """Uses edge-tts to generate audio file."""
        # Voices: en-US-ChristopherNeural (Male), en-US-EricNeural (Male), en-US-AnaNeural (Female), en-US-AriaNeural (Female)
        voice = "en-US-ChristopherNeural" 
        communicate = edge_tts.Communicate(text, voice, proxy=configured_http_proxy())
        await communicate.save(output_path)

    def create_podcast(self, paper_title, analysis_content, rag_context="", duration_minutes=5):
        """
        Main method to generate script and audio.
        Returns the path to the audio file.
        """
        logger.info(f"Generating Podcast for: {paper_title}")
        
        # 1. Generate Script
        script = self.generate_script(paper_title, analysis_content, rag_context, duration_minutes=duration_minutes)
        if not script:
            return None
            
        # Clean script (remove markdown bolding which TTS might read weirdly, though usually fine)
        clean_script = script.replace("**", "").replace("*", "").replace("#", "")
        
        # 2. Synthesize
        # Sanitize filename
        safe_title = "".join([c for c in paper_title if c.isalpha() or c.isdigit() or c==' ']).strip()[:50]
        filename = f"{safe_title}_Podcast.mp3"
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            asyncio.run(self._synthesize_audio(clean_script, output_path))
            logger.info(f"Podcast saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error synthesizing audio: {e}")
            return None
