import argparse
import json
import logging
import os
import re
from pathlib import Path

from src.config_loader import load_config
from src.paths import PaperBrainPaths


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

LEGACY_RENAME_MAP = {
    "Rethinking_VLM_Rep_VLA_Init": "Rethinking VLM Representation for VLA Initialization",
}


def _target_name(stem):
    if stem in LEGACY_RENAME_MAP:
        return LEGACY_RENAME_MAP[stem]
    return re.sub(r"\s+", " ", stem.replace("_", " ")).strip()


def _wiki_link_patterns(old_stem, new_stem):
    escaped = re.escape(old_stem)
    return [
        (re.compile(rf"\[\[{escaped}\]\]"), f"[[{new_stem}]]"),
        (re.compile(rf"\[\[{escaped}\|"), f"[[{new_stem}|"),
    ]


def _replace_links(text, rename_map):
    for old_stem, new_stem in rename_map.items():
        for pattern, repl in _wiki_link_patterns(old_stem, new_stem):
            text = pattern.sub(repl, text)
    return text


def _rewrite_text_files(vault, rename_map, dry_run=False):
    suffixes = {".md", ".json", ".base"}
    changed = []
    for path in vault.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        updated = _replace_links(text, rename_map)
        if updated != text:
            changed.append(path)
            if not dry_run:
                path.write_text(updated, encoding="utf-8")
    return changed


def _rewrite_run_state_paths(vault, rename_map, dry_run=False):
    changed = []
    run_records = vault / "Run_Records"
    state_paths = list(run_records.glob("*-run-state.json")) + list(run_records.glob("*/state.json"))
    for path in state_paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        touched = False
        for paper in data.get("papers", []):
            note_path = paper.get("note_path")
            if note_path:
                p = Path(note_path)
                old_stem = p.stem
                if old_stem in rename_map:
                    paper["note_path"] = str(p.with_name(f"{rename_map[old_stem]}.md"))
                    touched = True

            short_title = paper.get("short_title")
            if short_title in rename_map:
                paper["short_title"] = rename_map[short_title]
                touched = True
        if touched:
            changed.append(path)
            if not dry_run:
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return changed


def _rename_notes(notes_dir, dry_run=False):
    rename_map = {}
    conflicts = []
    for path in notes_dir.glob("*.md"):
        if "_" not in path.stem:
            continue
        new_stem = _target_name(path.stem)
        if not new_stem or new_stem == path.stem:
            continue
        new_path = path.with_name(f"{new_stem}.md")
        if new_path.exists() and new_path.resolve() != path.resolve():
            conflicts.append((path, new_path))
            continue
        rename_map[path.stem] = new_stem

    if conflicts:
        for old, new in conflicts:
            logger.warning("Rename conflict skipped: %s -> %s", old.name, new.name)

    for old_stem, new_stem in rename_map.items():
        old_path = notes_dir / f"{old_stem}.md"
        new_path = notes_dir / f"{new_stem}.md"
        logger.info("Rename note: %s -> %s", old_path.name, new_path.name)
        if not dry_run:
            old_path.rename(new_path)
    return rename_map


def fix_rethinking_mermaid(vault, dry_run=False):
    notes_dir = vault / "Research_Notes"
    candidates = [
        notes_dir / "Rethinking_VLM_Rep_VLA_Init.md",
        notes_dir / "Rethinking VLM Rep VLA Init.md",
        notes_dir / "Rethinking VLM Representation for VLA Initialization.md",
    ]
    path = next((p for p in candidates if p.exists()), None)
    if not path:
        logger.warning("Rethinking VLM note not found; Mermaid fix skipped.")
        return None

    text = path.read_text(encoding="utf-8")
    replacement = """```mermaid
graph LR
    Paper["Rethinking VLM Representation for VLA Initialization"]
    VLM["Pretrained VLM"]
    LoRA["LoRA Adaptation"]
    VQA["Embodied VQA Data"]
    Rep["Preserved Representation"]
    Init["Better VLA Initialization"]
    Policy["Downstream VLA Policy"]

    Paper --> VLM
    VLM --> LoRA
    LoRA --> Rep
    VQA --> LoRA
    Rep --> Init
    Init --> Policy
```

"""
    updated = re.sub(r"```mermaid\s*[\s\S]*?```\s*", replacement, text, count=1)
    if updated != text:
        logger.info("Fixed Mermaid block in %s", path.name)
        if not dry_run:
            path.write_text(updated, encoding="utf-8")
        return path
    return None


def normalize_note_filenames(dry_run=False):
    config = load_config()
    paths = PaperBrainPaths.from_config_dict(config)
    vault = paths.vault_path
    notes_dir = paths.notes_dir

    fixed_mermaid = fix_rethinking_mermaid(vault, dry_run=dry_run)
    rename_map = _rename_notes(notes_dir, dry_run=dry_run)
    rewrite_map = {**LEGACY_RENAME_MAP, **rename_map}
    if rewrite_map:
        text_changes = _rewrite_text_files(vault, rewrite_map, dry_run=dry_run)
        run_changes = _rewrite_run_state_paths(vault, rewrite_map, dry_run=dry_run)
    else:
        text_changes = []
        run_changes = []

    return {
        "fixed_mermaid": str(fixed_mermaid) if fixed_mermaid else "",
        "renamed_notes": rename_map,
        "updated_text_files": [str(p) for p in text_changes],
        "updated_run_states": [str(p) for p in run_changes],
    }


def main():
    parser = argparse.ArgumentParser(description="Normalize Research_Notes filenames by replacing underscores with spaces.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = normalize_note_filenames(dry_run=args.dry_run)
    logger.info("Mermaid fixed: %s", result["fixed_mermaid"] or "no")
    logger.info("Renamed notes: %s", len(result["renamed_notes"]))
    logger.info("Updated text files: %s", len(result["updated_text_files"]))
    logger.info("Updated run states: %s", len(result["updated_run_states"]))


if __name__ == "__main__":
    main()
