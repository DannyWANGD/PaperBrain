import argparse
import os
import logging
import yaml
from src.config_loader import load_config # Use new secure loader
from src.podcaster import Podcaster
from src.knowledge_base import KnowledgeBase
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# def load_config(path=None): ... REMOVED

def generate_podcast_for_note(filename, provider='doubao', duration_minutes=5):
    config = load_config()
    
    # Initialize components
    knowledge_base = KnowledgeBase(config, provider=provider)
    podcaster = Podcaster(config, provider=provider)
    
    # 1. Locate and Read the Note
    # config['obsidian']['vault_path'] is relative to the script directory in config.yaml (e.g., "../")
    # We need to resolve it to an absolute path based on where the config file is
    base_dir = os.path.dirname(os.path.abspath(__file__))
    vault_path = os.path.abspath(os.path.join(base_dir, config['obsidian']['vault_path']))
    notes_dir = os.path.join(vault_path, config['obsidian']['detailed_notes_folder'])
    
    # Handle filename with or without extension
    if not filename.endswith(".md"):
        filename += ".md"
        
    filepath = os.path.join(notes_dir, filename)
    
    if not os.path.exists(filepath):
        logger.error(f"Note not found: {filepath}")
        return

    logger.info(f"Reading note: {filename}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read note: {e}")
        return

    # 2. Extract Title and Analysis Content
    # Assume title is the first H1
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1) if title_match else filename.replace('.md', '')
    
    # Extract AI Analysis part (usually under ## 🧠 AI Analysis)
    analysis_match = re.search(r'##\s+🧠\s*AI Analysis\s*(.*?)(##|$)', content, re.DOTALL | re.IGNORECASE)
    
    if analysis_match:
        analysis_content = analysis_match.group(1).strip()
    else:
        logger.warning("Could not find '## 🧠 AI Analysis' section. Using full content.")
        analysis_content = content[:4000] # Limit to avoid context overflow if using full content

    # Also try to extract Abstract for RAG context search
    abstract_match = re.search(r'##\s+📌\s*Abstract\s*(.*?)(##|$)', content, re.DOTALL | re.IGNORECASE)
    abstract = abstract_match.group(1).strip() if abstract_match else ""

    # 3. Retrieve RAG Context
    logger.info("Retrieving RAG Context...")
    rag_context = knowledge_base.retrieve_context(title, abstract)
    
    # 4. Generate Podcast
    logger.info(f"Generating Podcast for '{title}'...")
    output_path = podcaster.create_podcast(title, analysis_content, rag_context, duration_minutes=duration_minutes)
    
    if output_path:
        logger.info(f"SUCCESS! Podcast generated at: {output_path}")
    else:
        logger.error("Failed to generate podcast.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a podcast for a specific Research Note")
    parser.add_argument("filename", type=str, help="Filename of the note in Research_Notes (e.g., 'Solaris.md')")
    parser.add_argument("--provider", type=str, default="doubao", choices=["doubao", "openrouter"], help="AI Provider")
    parser.add_argument("--minutes", type=int, default=5, help="Target podcast duration in minutes (default: 5)")
    
    args = parser.parse_args()
    
    generate_podcast_for_note(args.filename, provider=args.provider, duration_minutes=max(1, args.minutes))
