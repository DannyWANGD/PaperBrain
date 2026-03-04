import os
import asyncio
import logging
from openai import OpenAI
import edge_tts
import nest_asyncio

# Apply nest_asyncio to allow running asyncio in Jupyter/scripts that might already have an event loop
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Podcaster:
    def __init__(self, config, provider='doubao'):
        self.config = config
        self.provider = provider
        # config['obsidian']['vault_path'] might be relative, so we need to resolve it
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up one level from src to script
        vault_path = os.path.abspath(os.path.join(base_dir, config['obsidian']['vault_path']))
        
        self.output_dir = os.path.join(vault_path, "Podcasts")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Setup Client
        if provider == 'openrouter':
            self.api_key = config['openrouter']['api_key']
            self.base_url = "https://openrouter.ai/api/v1"
            self.model_pro = config['openrouter'].get('model_pro', 'anthropic/claude-3.5-sonnet')
        else:
            self.api_key = config['doubao']['api_key']
            self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
            self.model_pro = config['doubao'].get('model_pro', 'doubao-seed-2-0-pro-260215')

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=120.0  # Increased timeout for long script generation
        )

    def generate_script(self, paper_title, analysis_content, rag_context=""):
        """
        Generates a podcast script based on the paper analysis and RAG context.
        """
        prompt = f"""
        You are a professional tech podcaster (like Lex Fridman or a specialized AI researcher host).
        Your task is to create a script for a short "Research Briefing" audio segment (about 3-5 minutes).
        
        Topic: {paper_title}
        
        Deep Analysis Report:
        {analysis_content}
        
        Context from Knowledge Base (RAG):
        {rag_context}
        
        **Instructions**:
        1. **Style**: Engaging, intellectual, but accessible. Start with a hook.
        2. **Structure**:
           - **Intro**: Hook the listener with the problem statement.
           - **Core Idea**: Explain the "Aha Moment" and the technical innovation clearly.
           - **Context**: Mention how this relates to previous work (from the RAG context if available). e.g. "This reminds us of the paper X we discussed last week, but..."
           - **Critique**: Briefly mention limitations.
           - **Outro**: A thought-provoking closing sentence.
        3. **Format**: Write ONLY the spoken text. Do not include [Sound Effect] or [Host] labels. Just the monologue script.
        4. **Language**: English only.
        """
        
        try:
            extra_params = {}
            if self.provider == 'openrouter':
                 extra_params['extra_headers'] = {
                    "HTTP-Referer": "https://paperbrain.ai", 
                    "X-Title": "PaperBrain"
                 }

            response = self.client.chat.completions.create(
                model=self.model_pro,
                messages=[
                    {"role": "system", "content": "You are an expert science communicator."},
                    {"role": "user", "content": prompt}
                ],
                **extra_params
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating podcast script: {e}")
            return ""

    async def _synthesize_audio(self, text, output_path):
        """Uses edge-tts to generate audio file."""
        # Voices: en-US-ChristopherNeural (Male), en-US-EricNeural (Male), en-US-AnaNeural (Female), en-US-AriaNeural (Female)
        voice = "en-US-ChristopherNeural" 
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    def create_podcast(self, paper_title, analysis_content, rag_context=""):
        """
        Main method to generate script and audio.
        Returns the path to the audio file.
        """
        logger.info(f"Generating Podcast for: {paper_title}")
        
        # 1. Generate Script
        script = self.generate_script(paper_title, analysis_content, rag_context)
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
