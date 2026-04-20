"""
enrich_empty_themes.py
Re-runs AI enrichment only for theme pages whose AI sections are empty.
Usage: python enrich_empty_themes.py --provider openrouter
"""
import os, re, sys, argparse, logging
sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from src.config_loader import load_config, load_prompts, load_themes
from src.theme_manager import ThemeManager

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

# All 6 AI-enriched sections
AI_SECTIONS = [
    "领域里程碑工作",
    "前沿信号雷达",
    "体系化关联补充",
    "开放性问题",
    "主题关系可视化",
    "本周推进建议",
]

def is_empty(theme_path):
    try:
        with open(theme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False
    for section in AI_SECTIONS:
        pattern = rf"## [^\n]*{re.escape(section)}[^\n]*\n(?:- 暂无|- \[ \] 暂无|_暂无_)"
        if re.search(pattern, content):
            return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="openrouter")
    args = parser.parse_args()

    config = load_config()
    prompts = load_prompts()
    themes = load_themes()
    tm = ThemeManager(config, provider=args.provider, themes=themes, prompts=prompts)

    all_notes = tm._load_all_notes()
    theme_to_notes = tm._assign_notes_to_themes(all_notes)

    empty_themes = []
    for theme in tm.theme_defs:
        path = tm._theme_file_path(theme)
        if os.path.exists(path) and is_empty(path):
            empty_themes.append(theme)

    logger.info(f"Found {len(empty_themes)} themes with empty AI sections.")

    for i, theme in enumerate(empty_themes, 1):
        path = tm._theme_file_path(theme)
        matched = theme_to_notes.get(theme["id"], [])
        logger.info(f"[{i}/{len(empty_themes)}] Enriching {theme['id']} ({len(matched)} notes)...")
        ai_enrichment = tm._generate_ai_enrichment(theme, matched)
        content = tm._render_template(theme, matched, ai_enrichment)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"  Done.")

    tm._write_theme_index()
    logger.info("All empty themes enriched.")

if __name__ == "__main__":
    main()
