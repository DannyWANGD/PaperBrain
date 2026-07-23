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
        self.assertEqual(state.run_id, "2026-06-01")
        self.assertEqual(Path(state.run_dir).name, "2026-06-01")
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
        self.assertTrue(data["logs"])
        self.assertIn("event_type", data["logs"][-1])
        self.assertIn("status", data["logs"][-1])
        self.assertIn("ts", data["logs"][-1])

    def test_resume_clears_retryable_errors_and_can_complete_successfully(self):
        state = RunState(self.config, date(2026, 6, 1), "openrouter")
        state.add_error(
            "llm_coarse_screening_failed",
            "provider unavailable",
            stage="coarse",
            paper_id="arxiv:2606.02486",
            retryable=True,
        )
        state.mark_stage("failed")

        resumed = RunState(self.config, date(2026, 6, 1), "openrouter")
        self.assertEqual(resumed.clear_retryable_errors(), 1)
        resumed.mark_stage("completed")

        self.assertEqual(resumed.data["errors"], [])
        self.assertTrue(resumed.summary()["ok"])
        self.assertEqual(resumed.summary()["stage"], "completed")

    def test_resume_keeps_non_retryable_errors_and_deduplicates_active_failure(self):
        state = RunState(self.config, date(2026, 6, 2), "openrouter")
        for _ in range(2):
            state.add_error(
                "invalid_config",
                "configuration is invalid",
                stage="initialized",
                retryable=False,
            )

        self.assertEqual(len(state.data["errors"]), 1)
        self.assertEqual(state.clear_retryable_errors(), 0)
        self.assertEqual(len(state.data["errors"]), 1)

    def test_resolve_errors_clears_only_the_operation_that_succeeded(self):
        state = RunState(self.config, date(2026, 6, 3), "openrouter")
        state.add_error(
            "llm_coarse_screening_failed",
            "first failure",
            stage="coarse",
            paper_id="arxiv:2606.00001",
            retryable=True,
        )
        state.add_error(
            "llm_coarse_screening_failed",
            "other paper failure",
            stage="coarse",
            paper_id="arxiv:2606.00002",
            retryable=True,
        )
        state.add_error(
            "source_degraded",
            "arXiv unavailable",
            stage="fetch",
            paper_id="source:arxiv",
            retryable=True,
        )

        removed = state.resolve_errors(
            code="llm_coarse_screening_failed",
            stage="coarse",
            paper_id="arxiv:2606.00001",
        )

        self.assertEqual(removed, 1)
        self.assertEqual(
            {(error["code"], error["paper_id"]) for error in state.data["errors"]},
            {
                ("llm_coarse_screening_failed", "arxiv:2606.00002"),
                ("source_degraded", "source:arxiv"),
            },
        )

    def test_repeated_failure_updates_active_error_instead_of_duplicating(self):
        state = RunState(self.config, date(2026, 6, 4), "openrouter")
        state.add_error("source_degraded", "timeout", stage="fetch", paper_id="source:arxiv", retryable=True)
        state.add_error("source_degraded", "HTTP 503", stage="fetch", paper_id="source:arxiv", retryable=True)

        self.assertEqual(len(state.data["errors"]), 1)
        self.assertEqual(state.data["errors"][0]["message"], "HTTP 503")

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
        self.assertFalse(legacy_path.exists())
        self.assertTrue((legacy_dir / "_legacy" / "2026-06-01" / legacy_path.name).exists())

    def test_single_and_daily_states_share_canonical_daily_directory(self):
        daily = RunState(self.config, date(2026, 6, 2), "openrouter")
        single = RunState(self.config, date(2026, 6, 2), "openrouter", single_paper=True)

        self.assertEqual(daily.path, single.path)
        self.assertEqual(Path(single.run_dir).name, "2026-06-02")
        self.assertIn("daily", single.data["run_modes"])
        self.assertIn("single", single.data["run_modes"])

    def test_same_date_full_run_preserves_single_forced_flags_without_cross_date_merge(self):
        single = RunState(self.config, date(2026, 6, 4), "openrouter", single_paper=True)
        single.merge_paper(
            {"title": "Manual AHEAD", "url": "https://arxiv.org/abs/2606.02486", "score": 7.1},
            mode="single",
            forced_deep=True,
        )

        daily = RunState(self.config, date(2026, 6, 4), "openrouter")
        daily.set_papers(
            [{"title": "Daily AHEAD", "url": "https://arxiv.org/abs/2606.02486v2", "score": 8.0}],
            stage="fetched",
        )

        papers = daily.papers()
        self.assertEqual(len(papers), 1)
        self.assertTrue(papers[0]["forced_deep"])
        self.assertTrue(papers[0]["forced_digest"])
        self.assertIn("single", papers[0]["paper_sources"])
        self.assertIn("daily", papers[0]["paper_sources"])

        other_day = RunState(self.config, date(2026, 6, 5), "openrouter")
        self.assertEqual(other_day.papers(), [])

    def test_merges_legacy_provider_and_single_dirs_by_identity(self):
        run_records = Path(self.tmp) / "Run_Records"
        provider_dir = run_records / "2026-06-03-openrouter"
        single_dir = run_records / "2026-06-03-single"
        provider_dir.mkdir(parents=True)
        single_dir.mkdir(parents=True)
        (provider_dir / "state.json").write_text(
            json.dumps(
                {
                    "date": "2026-06-03",
                    "provider": "openrouter",
                    "single_paper": False,
                    "stage": "screened",
                    "papers": [{"title": "AHEAD Daily", "url": "https://arxiv.org/abs/2606.02486", "score": 7.3}],
                }
            ),
            encoding="utf-8",
        )
        (single_dir / "state.json").write_text(
            json.dumps(
                {
                    "date": "2026-06-03",
                    "provider": "openrouter",
                    "single_paper": True,
                    "stage": "screened",
                    "papers": [{"title": "AHEAD Single", "url": "https://arxiv.org/abs/2606.02486v1", "score": 7.1}],
                }
            ),
            encoding="utf-8",
        )

        state = RunState(self.config, date(2026, 6, 3), "openrouter")
        papers = state.papers()

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["score"], 7.3)
        self.assertTrue(papers[0]["forced_deep"])
        self.assertIn("daily", papers[0]["paper_sources"])
        self.assertIn("single", papers[0]["paper_sources"])
        self.assertTrue((run_records / "_legacy" / "2026-06-03" / "2026-06-03-openrouter").exists())
        self.assertTrue((run_records / "_legacy" / "2026-06-03" / "2026-06-03-single").exists())


if __name__ == "__main__":
    unittest.main()
