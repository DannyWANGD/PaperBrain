import argparse
import logging

from src.config_loader import load_config
from src.research_indexer import ResearchIndexer


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Rebuild the Obsidian research index.")
    parser.add_argument(
        "--no-update-notes",
        action="store_true",
        help="Only regenerate index files; do not rewrite note frontmatter.",
    )
    args = parser.parse_args()

    config = load_config()
    indexer = ResearchIndexer(config)
    notes = indexer.build(update_notes=not args.no_update_notes)
    logger.info("Indexed %s research notes.", len(notes))


if __name__ == "__main__":
    main()
