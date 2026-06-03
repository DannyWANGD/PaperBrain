import argparse
import logging
import os
import re

from src.config_loader import load_config
from src.knowledge_base import KnowledgeBase
from src.podcaster import Podcaster


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def generate_podcast_for_note(filename, provider="doubao", duration_minutes=5):
    config = load_config()
    knowledge_base = KnowledgeBase(config, provider=provider)
    podcaster = Podcaster(config, provider=provider)

    vault_path = config["obsidian"]["vault_path"]
    notes_dir = os.path.join(vault_path, config["obsidian"]["detailed_notes_folder"])

    if not filename.endswith(".md"):
        filename += ".md"
    filepath = os.path.join(notes_dir, filename)

    if not os.path.exists(filepath):
        logger.error("Note not found: %s", filepath)
        return None

    logger.info("Reading note: %s", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    title = title_match.group(1) if title_match else filename.replace(".md", "")

    analysis_match = re.search(
        r"##\s+.*?AI Analysis\s*(.*?)(?=^##\s+|\Z)",
        content,
        re.DOTALL | re.IGNORECASE | re.MULTILINE,
    )
    if analysis_match:
        analysis_content = analysis_match.group(1).strip()
    else:
        logger.warning("Could not find an AI Analysis section. Using the first 4000 chars.")
        analysis_content = content[:4000]

    abstract_match = re.search(
        r"##\s+.*?Abstract\s*(.*?)(?=^##\s+|\Z)",
        content,
        re.DOTALL | re.IGNORECASE | re.MULTILINE,
    )
    abstract = abstract_match.group(1).strip() if abstract_match else ""

    logger.info("Retrieving RAG context...")
    rag_context = knowledge_base.retrieve_context(title, abstract)

    logger.info("Generating podcast for '%s'...", title)
    output_path = podcaster.create_podcast(
        title,
        analysis_content,
        rag_context,
        duration_minutes=duration_minutes,
    )
    if output_path:
        logger.info("Podcast generated at: %s", output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate a podcast for a Research_Notes file.")
    parser.add_argument("filename", type=str, help="Filename in Research_Notes, e.g. FASTER.md")
    parser.add_argument("--provider", type=str, default="doubao", choices=["doubao", "openrouter"])
    parser.add_argument("--minutes", type=int, default=5, help="Target podcast duration")
    args = parser.parse_args()

    generate_podcast_for_note(
        args.filename,
        provider=args.provider,
        duration_minutes=max(1, args.minutes),
    )


if __name__ == "__main__":
    main()
