import os
import json
import logging
from typing import List, Dict
import re
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBase:
    """
    Implements a lightweight LLM-based RAG system.
    Instead of heavy vector databases, it uses the long-context capability of Flash models
    to scan existing notes and find relevant connections.
    """
    def __init__(self, config, provider='doubao', prompts=None):
        self.config = config
        self.provider = provider
        self.prompts = prompts or {}
        self.notes_dir = os.path.join(config['obsidian']['vault_path'], config['obsidian']['detailed_notes_folder'])
        
        # Setup Client (Same logic as Analyser)
        if provider == 'openrouter':
            self.api_key = config['openrouter']['api_key']
            self.base_url = "https://openrouter.ai/api/v1"
            self.model_flash = config['openrouter'].get('model_flash', 'google/gemini-2.0-flash-001')
        else:
            self.api_key = config['doubao']['api_key']
            self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
            self.model_flash = config['doubao'].get('model_flash', 'doubao-seed-2-0-lite-260215')

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def _openrouter_model_candidates(self, primary_model: str):
        if self.provider != 'openrouter':
            return [primary_model]

        cfg = self.config.get('openrouter', {})
        fallbacks = cfg.get('model_flash_fallbacks', [])
        if not isinstance(fallbacks, list):
            fallbacks = []

        defaults = [
            "google/gemini-2.0-flash-001",
            "openai/gpt-4o-mini",
            "deepseek/deepseek-chat",
        ]

        candidates = []
        for m in [primary_model, *fallbacks, *defaults]:
            if m and m not in candidates:
                candidates.append(m)
        return candidates

    def _chat_with_fallback(self, models, messages, **kwargs):
        last_err = None
        for model in models:
            try:
                return self.client.chat.completions.create(model=model, messages=messages, **kwargs)
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

    def scan_notes(self) -> List[Dict]:
        """
        Scans all markdown files in the Research_Notes directory.
        Returns a list of dicts: {'filename': str, 'title': str, 'summary': str}
        """
        notes = []
        if not os.path.exists(self.notes_dir):
            logger.warning(f"Notes directory not found: {self.notes_dir}")
            return []

        for filename in os.listdir(self.notes_dir):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(self.notes_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
                title = title_match.group(1) if title_match else filename.replace('.md', '')

                abstract_match = re.search(r'##\s+📌?\s*Abstract\s*(.*?)(##|$)', content, re.DOTALL | re.IGNORECASE)
                summary = abstract_match.group(1).strip()[:1000] if abstract_match else content[:1000]

                notes.append({
                    'filename': filename,
                    'title': title,
                    'summary': summary
                })
            except Exception as e:
                logger.warning(f"Error reading note {filename}: {e}")

        return notes

    def retrieve_context(self, new_paper_title: str, new_paper_abstract: str, k=3) -> str:
        """
        Uses LLM to select the most relevant notes from the vault.
        Returns a formatted string of relevant notes to be injected into the prompt.
        """
        existing_notes = self.scan_notes()

        if not existing_notes:
            return ""

        notes_list_str = ""
        for i, note in enumerate(existing_notes):
            notes_list_str += f"ID: {i}\nFilename: {note['filename']}\nTitle: {note['title']}\nSummary: {note['summary'][:200]}...\n---\n"

        system_prompt = self.prompts.get('rag', {}).get('system', "You are a helpful research assistant.")
        user_template = self.prompts.get('rag', {}).get('retrieve_user', """
        I am analyzing a new paper:
        Title: {title}
        Abstract: {abstract}

        Here is a list of my existing research notes:
        {notes_list}

        Task:
        Identify the top {k} most relevant notes that I should review to understand the connection between this new paper and my previous knowledge.
        Return ONLY a JSON array of indices, e.g., [0, 5, 12]. If none are relevant, return [].
        """)
        prompt = user_template.format(
            title=new_paper_title,
            abstract=new_paper_abstract,
            notes_list=notes_list_str,
            k=k
        )

        try:
            extra_params = {}
            if self.provider == 'openrouter':
                 extra_params['extra_headers'] = {
                    "HTTP-Referer": "https://paperbrain.ai",
                    "X-Title": "PaperBrain"
                 }

            models = self._openrouter_model_candidates(self.model_flash)
            response = self._chat_with_fallback(
                models=models,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                **extra_params
            )
            
            content = response.choices[0].message.content
            # Sanitize and parse JSON
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if not json_match:
                logger.warning(f"RAG retrieval: model returned no JSON array. Raw: {content[:200]}")
                return "No directly relevant prior notes found."
            indices = json.loads(json_match.group(0))
            
            selected_notes = [existing_notes[i] for i in indices if 0 <= i < len(existing_notes)]
            
            if not selected_notes:
                return "No directly relevant prior notes found."
                
            # Format the output for the Pro model
            context_str = "**📚 Related Notes from Your Vault (Context-Aware RAG):**\n"
            for note in selected_notes:
                context_str += f"- **[[{note['filename'].replace('.md','')}]]** ({note['title']}):\n  _{note['summary']}...\n"
            
            return context_str
            
        except Exception as e:
            logger.error(f"Error in RAG retrieval: {e}")
            return "Error retrieving context."
