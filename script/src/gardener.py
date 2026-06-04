import os
import re
import logging
import yaml
from datetime import datetime
from src.paths import PaperBrainPaths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeGardener:
    def __init__(self, config, provider='doubao'):
        self.config = config
        self.provider = provider
        paths = PaperBrainPaths.from_config_dict(config)
        self.vault_path = str(paths.vault_path)
        self.notes_folder = str(paths.notes_dir)

    _SUFFIXES = [
        'ation', 'tion', 'sion', 'ment', 'ness', 'able', 'ible',
        'ing', 'ous', 'ive', 'ful', 'less', 'ity', 'ally',
        'ies', 'ed', 'er', 'ly', 'al', 'es', 's',
    ]

    def _stem(self, word):
        word = word.lower().strip()
        for suffix in self._SUFFIXES:
            if word.endswith(suffix) and len(word) - len(suffix) >= 3:
                return word[:-len(suffix)]
        return word

    def _is_match(self, alias, search_text):
        """Tiered alias matching for robust but conservative backlinking."""
        alias = alias.strip()
        if len(alias) < 4:
            return False

        alias_norm = alias.replace('_', ' ').lower()
        if ' ' not in alias_norm:
            return bool(re.search(rf'\b{re.escape(alias_norm)}\b', search_text, re.IGNORECASE))

        alias_tokens = {self._stem(w) for w in alias_norm.split() if len(w) >= 3}
        if not alias_tokens:
            return False
        text_tokens = {self._stem(w) for w in re.findall(r'\b\w+\b', search_text.lower())}
        overlap = len(alias_tokens & text_tokens)
        return overlap >= max(1, len(alias_tokens) * 0.7)

    def _get_existing_notes_metadata(self):
        notes_meta = {}
        if not os.path.exists(self.notes_folder):
            return notes_meta

        for filename in os.listdir(self.notes_folder):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(self.notes_folder, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
                aliases = []
                title = filename.replace(".md", "").replace("_", " ")

                if frontmatter_match:
                    try:
                        fm = yaml.safe_load(frontmatter_match.group(1)) or {}
                        raw_aliases = fm.get('aliases', [])
                        if isinstance(raw_aliases, str):
                            raw_aliases = [raw_aliases]
                        aliases = [a for a in raw_aliases if a]
                    except yaml.YAMLError:
                        pass

                stem = filename.replace(".md", "")
                if stem not in aliases:
                    aliases.append(stem)

                notes_meta[filename] = {
                    "path": filepath,
                    "aliases": [a.lower() for a in aliases],
                    "title": title
                }
            except Exception as e:
                logger.error(f"Error reading note {filename}: {e}")

        return notes_meta

    def prune_and_graft(self, new_papers):
        logger.info("Knowledge Gardener started pruning and grafting...")

        existing_notes = self._get_existing_notes_metadata()
        if not existing_notes:
            logger.info("No existing notes to link back to.")
            return

        updates_count = 0
        provider_cfg = self.config.get(self.provider, self.config.get('doubao', {}))
        threshold = provider_cfg.get('threshold_score', 7)

        for new_paper in new_papers:
            if new_paper.get('score', 0) < threshold:
                continue

            new_title = new_paper.get('title', '')
            new_abstract = new_paper.get('abstract', '')
            new_innovation = new_paper.get('innovation', '')
            new_note_filename = new_paper.get('short_title', '') or new_title
            safe_new_filename = "".join(
                [c for c in new_note_filename if c.isalpha() or c.isdigit() or c in (' ', '_')]
            ).strip()
            safe_new_filename = re.sub(r'\s+', ' ', safe_new_filename)[:100]

            search_text = (new_title + " " + new_abstract + " " + new_innovation).lower()

            for note_file, note_data in existing_notes.items():
                if note_file == f"{safe_new_filename}.md":
                    continue

                matched_alias = None
                for alias in note_data['aliases']:
                    if self._is_match(alias, search_text):
                        matched_alias = alias
                        break

                if matched_alias:
                    self._append_backlink(note_data['path'], new_paper, safe_new_filename, matched_alias)
                    updates_count += 1

        logger.info(f"Gardening complete. Updated {updates_count} existing notes with backlinks.")

    def _append_backlink(self, target_note_path, source_paper, source_filename, matched_concept):
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            backlink_text = (
                f"\n- [ ] **{today_str}**: New paper [[{source_filename}]] discusses "
                f"*{matched_concept}*. Innovation: \"{source_paper.get('innovation', 'No summary')}\""
            )

            with open(target_note_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if f"[[{source_filename}]]" in content:
                return

            header = "## Related Work Updates"
            with open(target_note_path, 'a', encoding='utf-8') as f:
                if header in content:
                    f.write(backlink_text)
                else:
                    f.write(f"\n\n{header}{backlink_text}")

            logger.info(f"  -> Linked '{source_paper['title'][:40]}' to '{os.path.basename(target_note_path)}'")

        except Exception as e:
            logger.error(f"Failed to update backlink in {target_note_path}: {e}")
