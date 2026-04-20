from src.config_loader import load_config, load_prompts, load_themes
from src.theme_manager import ThemeManager
import argparse


def main():
    parser = argparse.ArgumentParser(description="Rebuild AI-enriched theme pages")
    parser.add_argument("--provider", type=str, default="openrouter", choices=["doubao", "openrouter"])
    args = parser.parse_args()
    config = load_config()
    prompts = load_prompts()
    themes = load_themes()
    manager = ThemeManager(config, provider=args.provider, themes=themes, prompts=prompts)
    manager.rebuild_theme_pages()
    print("Theme pages rebuilt successfully.")


if __name__ == "__main__":
    main()
