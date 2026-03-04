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
    def __init__(self, config, provider='doubao'):
        self.config = config
        self.provider = provider
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

    def scan_notes(self) -> List[Dict]:
        """
        Scans all markdown files in the Research_Notes directory.
        Returns a list of dicts: {'filename': str, 'title': str, 'summary': str}
        """
        notes = []
        if not os.path.exists(self.notes_dir):
            return []

        for filename in os.listdir(self.notes_dir):
            if not filename.endswith(".md"):
                continue
            
            filepath = os.path.join(self.notes_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Simple extraction
                    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
                    title = title_match.group(1) if title_match else filename.replace('.md', '')
                    
                    # Extract Abstract or Summary (first 1000 chars)
                    # Try to find "## Abstract" or just take the beginning
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
            return "No existing notes found in the vault."
            
        # Construct the prompt context
        # We list all notes with their ID and Summary
        notes_list_str = ""
        for i, note in enumerate(existing_notes):
            notes_list_str += f"ID: {i}\nFilename: {note['filename']}\nTitle: {note['title']}\nSummary: {note['summary'][:200]}...\n---\n"
            
        # Prompt for the Flash model
        prompt = f"""
        I am analyzing a new paper:
        Title: {new_paper_title}
        Abstract: {new_paper_abstract}
        
        Here is a list of my existing research notes:
        {notes_list_str}
        
        Task:
        Identify the top {k} most relevant notes that I should review to understand the connection between this new paper and my previous knowledge.
        Return ONLY a JSON array of indices, e.g., [0, 5, 12]. If none are relevant, return [].
        """
        
        try:
            extra_params = {}
            if self.provider == 'openrouter':
                 extra_params['extra_headers'] = {
                    "HTTP-Referer": "https://paperbrain.ai", 
                    "X-Title": "PaperBrain"
                 }

            response = self.client.chat.completions.create(
                model=self.model_flash,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                **extra_params
            )
            
            content = response.choices[0].message.content
            # Sanitize and parse JSON
            json_str = re.search(r'\[.*\]', content, re.DOTALL).group(0)
            indices = json.loads(json_str)
            
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
