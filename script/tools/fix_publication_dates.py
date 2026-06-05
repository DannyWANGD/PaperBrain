import argparse
import json
import logging
import re
from pathlib import Path

import yaml

from src.config_loader import load_config
from src.paths import PaperBrainPaths


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def _split_frontmatter(text):
    match = re.match(r"^---\n([\s\S]*?)\n---\n?", text)
    if not match:
        return {}, text, None
    data = yaml.safe_load(match.group(1)) or {}
    return data if isinstance(data, dict) else {}, text[match.end():], match


def _date_only(value):
    if not value:
        return ""
    return str(value)[:10]


def _frontmatter_text(data):
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()


def _run_state_candidates(paths, day, provider):
    run_records = paths.run_records_dir
    return [
        paths.state_path(day, provider),
        paths.legacy_state_path(day, provider),
        run_records / f"{day}-{provider}" / "state.json",
        run_records / f"{day}-single" / "state.json",
        run_records / f"{day}-{provider}-run-state.json",
        run_records / f"{day}-single-run-state.json",
    ]


def fix_dates(dates, provider="openrouter", dry_run=False):
    config = load_config()
    paths = PaperBrainPaths.from_config_dict(config)
    changed_notes = []
    changed_runs = []

    for day in dates:
        run_path = next((candidate for candidate in _run_state_candidates(paths, day, provider) if candidate.exists()), None)
        if run_path is None:
            logger.warning("Run state not found: %s", paths.state_path(day, provider))
            continue

        data = json.loads(run_path.read_text(encoding="utf-8"))
        run_changed = False
        for paper in data.get("papers", []):
            authoritative_date = _date_only(paper.get("published")) or _date_only(data.get("date")) or day
            if not authoritative_date:
                continue

            if paper.get("publication_date") != authoritative_date:
                paper["publication_date"] = authoritative_date
                run_changed = True

            metadata = paper.get("metadata")
            if isinstance(metadata, dict):
                metadata_date = metadata.get("publication_date")
                if metadata_date and metadata_date != "Unknown":
                    paper["metadata_publication_date"] = metadata_date

            note_path = paper.get("note_path")
            if note_path:
                note_changed = _fix_note_frontmatter(Path(note_path), authoritative_date, dry_run=dry_run)
                if note_changed:
                    changed_notes.append(str(note_path))

        if run_changed and not dry_run:
            run_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            changed_runs.append(str(run_path))
        elif run_changed:
            changed_runs.append(str(run_path))

    return changed_runs, changed_notes


def _fix_note_frontmatter(note_path, authoritative_date, dry_run=False):
    if not note_path.exists():
        logger.warning("Note not found: %s", note_path)
        return False

    text = note_path.read_text(encoding="utf-8")
    fm, body, match = _split_frontmatter(text)
    if match is None:
        logger.warning("No frontmatter found: %s", note_path)
        return False

    previous_date = str(fm.get("publication_date") or "")
    if previous_date == authoritative_date:
        return False

    if previous_date and previous_date.lower() != "unknown":
        fm.setdefault("metadata_publication_date", previous_date)
    fm["publication_date"] = authoritative_date

    if not dry_run:
        note_path.write_text(f"---\n{_frontmatter_text(fm)}\n---\n\n{body.lstrip()}", encoding="utf-8")
    logger.info("Fixed %s: %s -> %s", note_path.name, previous_date or "Unknown", authoritative_date)
    return True


def main():
    parser = argparse.ArgumentParser(description="Fix note publication_date values from run-state published dates.")
    parser.add_argument("dates", nargs="+", help="Run dates to fix, e.g. 2026-05-29 2026-06-01.")
    parser.add_argument("--provider", default="openrouter")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    changed_runs, changed_notes = fix_dates(args.dates, provider=args.provider, dry_run=args.dry_run)
    logger.info("Changed run states: %s", len(changed_runs))
    logger.info("Changed notes: %s", len(changed_notes))


if __name__ == "__main__":
    main()
