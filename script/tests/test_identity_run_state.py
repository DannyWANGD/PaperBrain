import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.paper_identity import (  # noqa: E402
    canonical_arxiv_id,
    identity_key,
    normalize_paper_identity,
    paper_id_from_metadata,
)
from src.run_state import RunState  # noqa: E402


class PaperIdentityTest(unittest.TestCase):
    def test_canonical_arxiv_id_strips_version_and_pdf(self):
        self.assertEqual(canonical_arxiv_id("https://arxiv.org/pdf/2606.02486v1.pdf"), "2606.02486")
        self.assertEqual(canonical_arxiv_id("https://huggingface.co/papers/2605.30011"), "2605.30011")
        self.assertEqual(canonical_arxiv_id("2603.19199v2"), "2603.19199")

    def test_paper_id_prefers_arxiv_identity(self):
        metadata = {
            "title": "Some Paper",
            "url": "https://huggingface.co/papers/2603.19199",
        }
        self.assertEqual(paper_id_from_metadata(metadata), "arxiv:2603.19199")
        self.assertEqual(identity_key(metadata), "arxiv:2603.19199")

    def test_normalize_paper_identity(self):
        paper = normalize_paper_identity({
            "title": "AHEAD",
            "pdf_url": "https://arxiv.org/pdf/2606.02486v1",
        })
        self.assertEqual(paper["arxiv_id"], "2606.02486")
        self.assertEqual(paper["paper_id"], "arxiv:2606.02486")


class RunStateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.config = {
            "obsidian": {
                "vault_path": self.tmp,
                "detailed_notes_folder": "Research_Notes",
            }
        }

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_save_reload_and_report(self):
        state = RunState(self.config, date(2026, 6, 1), "openrouter")
        state.set_papers([
            {
                "title": "AHEAD",
                "url": "https://arxiv.org/abs/2606.02486v1",
                "score": 8.4,
                "screening_stage": "detailed",
                "in_daily_digest": True,
                "selected_for_deep_analysis": True,
            }
        ], stage="screened")

        reloaded = RunState(self.config, date(2026, 6, 1), "openrouter")
        self.assertEqual(reloaded.data["stage"], "screened")
        self.assertEqual(reloaded.papers()[0]["paper_id"], "arxiv:2606.02486")

        report = reloaded.write_screening_report()
        self.assertTrue(Path(report).exists())
        self.assertEqual(Path(report).name, "screening_report.md")
        self.assertEqual(Path(reloaded.path).name, "state.json")
        self.assertTrue(Path(reloaded.log_summary_path).exists())
        self.assertTrue(Path(reloaded.errors_path).exists())
        raw = Path(reloaded.path).read_text(encoding="utf-8")
        data = json.loads(raw)
        self.assertEqual(data["papers"][0]["score"], 8.4)
        self.assertEqual(data["paths"]["state"], reloaded.path)

    def test_loads_legacy_state_and_writes_new_state_json(self):
        legacy_dir = Path(self.tmp) / "Run_Records"
        legacy_dir.mkdir()
        legacy_path = legacy_dir / "2026-06-01-openrouter-run-state.json"
        legacy_path.write_text(
            json.dumps(
                {
                    "date": "2026-06-01",
                    "provider": "openrouter",
                    "stage": "screened",
                    "papers": [{"title": "Legacy", "url": "https://arxiv.org/abs/2606.02486"}],
                }
            ),
            encoding="utf-8",
        )

        state = RunState(self.config, date(2026, 6, 1), "openrouter")

        self.assertEqual(state.data["stage"], "screened")
        self.assertEqual(state.papers()[0]["paper_id"], "arxiv:2606.02486")
        self.assertTrue(Path(state.path).exists())
        self.assertEqual(Path(state.path).name, "state.json")


if __name__ == "__main__":
    unittest.main()
