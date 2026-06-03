import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.fix_publication_dates import fix_dates  # noqa: E402


class FixPublicationDatesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        vault = Path(self.tmp)
        notes = vault / "Research_Notes"
        runs = vault / "Run_Records"
        notes.mkdir()
        runs.mkdir()
        self.note = notes / "Paper.md"
        self.note.write_text(
            """---
paper_id: arxiv:2606.00001
publication_date: "2026-05-31"
score: 8.0
---

# Paper
""",
            encoding="utf-8",
        )
        run = {
            "date": "2026-06-02",
            "provider": "openrouter",
            "papers": [
                {
                    "title": "Paper",
                    "paper_id": "arxiv:2606.00001",
                    "published": "2026-06-02T17:30:00",
                    "publication_date": None,
                    "metadata": {"publication_date": "2026-05-31"},
                    "note_path": str(self.note),
                }
            ],
        }
        (runs / "2026-06-02-openrouter-run-state.json").write_text(
            json.dumps(run, indent=2),
            encoding="utf-8",
        )
        self.config = {
            "obsidian": {
                "vault_path": self.tmp,
                "detailed_notes_folder": "Research_Notes",
            }
        }

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_fix_dates_prefers_run_state_published_date(self):
        with patch.dict(os.environ, {}, clear=False):
            with patch("tools.fix_publication_dates.load_config", return_value=self.config):
                changed_runs, changed_notes = fix_dates(["2026-06-02"])

        self.assertEqual(len(changed_runs), 1)
        self.assertEqual(len(changed_notes), 1)
        text = self.note.read_text(encoding="utf-8")
        self.assertIn("publication_date: '2026-06-02'", text)
        self.assertIn("metadata_publication_date: '2026-05-31'", text)


if __name__ == "__main__":
    unittest.main()
