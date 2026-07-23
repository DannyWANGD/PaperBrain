import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main as pipeline  # noqa: E402


class FakeScraper:
    def __init__(self, single_paper=None):
        self.target_date = None
        self.single_url = None
        self.single_paper = single_paper

    def get_all_papers(self, target_date=None):
        self.target_date = target_date
        return [{"title": "Fetched Paper", "url": "https://arxiv.org/abs/2606.02486"}]

    def fetch_single_arxiv_paper(self, arxiv_url):
        self.single_url = arxiv_url
        return self.single_paper or {"title": "Single Paper", "url": arxiv_url}


class FakeAnalyser:
    model_flash = "fake-flash"
    model_screening_pro = "fake-pro"

    def __init__(self):
        self.screened_titles = []

    def coarse_screen_paper(self, paper):
        return {
            "coarse_score": 8.0,
            "relevance": 8.0,
            "evidence": 7.0,
            "method_completeness": 7.5,
            "should_rescreen": True,
            "reason": f"coarse {paper['title']}",
            "used_model": "fake-flash",
            "short_title": paper["title"],
        }

    def screen_paper(self, paper):
        self.screened_titles.append(paper["title"])
        return {
            "score": 8.6,
            "innovation": "solid method",
            "limitations": "sim only",
            "reason": "high relevance",
            "tags": ["domain/vla"],
            "short_title": paper["title"],
            "relevance": 9.0,
            "novelty": 8.0,
            "rigor": 8.0,
            "evidence": 8.0,
            "reproducibility": 7.0,
            "confidence": 8.0,
            "red_flags": [],
            "screening_stage": "detailed",
            "used_model": "fake-pro",
        }


class FakeRunState:
    path = "fake-run-state.json"

    def __init__(self, stage="initialized", papers=None):
        self.data = {"stage": stage, "papers": papers or [], "selection": {}, "logs": [], "errors": []}
        self.set_calls = []
        self.updated = []
        self.marked = []

    def papers(self):
        return list(self.data.get("papers", []))

    def set_papers(self, papers, stage):
        self.data["papers"] = list(papers)
        self.data["stage"] = stage
        self.set_calls.append((stage, list(papers)))

    def update_paper(self, paper):
        self.updated.append(dict(paper))
        key = paper.get("paper_id") or paper.get("url") or paper.get("title")
        for index, existing in enumerate(self.data.setdefault("papers", [])):
            existing_key = existing.get("paper_id") or existing.get("url") or existing.get("title")
            if existing_key == key:
                self.data["papers"][index] = dict(paper)
                break
        else:
            self.data.setdefault("papers", []).append(dict(paper))

    def merge_paper(self, paper, mode=None, forced_deep=False):
        merged = dict(paper)
        if forced_deep:
            merged["forced_deep"] = True
            merged["forced_digest"] = True
            merged["selected_for_deep_analysis"] = True
            merged["in_daily_digest"] = True
        sources = list(merged.get("paper_sources", []))
        if mode and mode not in sources:
            sources.append(mode)
        merged["paper_sources"] = sources
        self.update_paper(merged)
        return merged

    def mark_stage(self, stage):
        self.data["stage"] = stage
        self.marked.append(stage)

    def update_selection(self, **kwargs):
        self.data.setdefault("selection", {}).update(kwargs)

    def add_log_event(self, **kwargs):
        self.data.setdefault("logs", []).append(kwargs)

    def add_error(
        self,
        code,
        message,
        suggestion="",
        stage="",
        paper_id="",
        title="",
        exception="",
        retryable=False,
        **kwargs,
    ):
        self.data.setdefault("errors", []).append({
            "code": code,
            "message": message,
            "suggestion": suggestion,
            "stage": stage,
            "paper_id": paper_id,
            "title": title,
            "exception": exception,
            "retryable": retryable,
        })

    def resolve_errors(self, **filters):
        errors = list(self.data.get("errors", []))
        self.data["errors"] = [
            error
            for error in errors
            if not all(value is None or error.get(key) == value for key, value in filters.items())
        ]
        return len(errors) - len(self.data["errors"])

    def summary(self):
        return {
            "ok": not self.data.get("errors"),
            "stage": self.data.get("stage", ""),
            "errors": list(self.data.get("errors", [])),
        }


class MainPipelineHelperTest(unittest.TestCase):
    def test_resolve_target_date_uses_arxiv_publication_when_date_omitted(self):
        scraper = FakeScraper({
            "title": "Single Paper",
            "url": "https://arxiv.org/abs/2606.02486",
            "publication_date": "2026-05-31",
        })

        target, source, paper, arxiv_publication_date, warning = pipeline._resolve_target_date_for_run(
            scraper,
            target_date=None,
            arxiv_url="https://arxiv.org/abs/2606.02486",
        )

        self.assertEqual(target, date(2026, 5, 31))
        self.assertEqual(source, "arxiv_v1")
        self.assertEqual(arxiv_publication_date, "2026-05-31")
        self.assertEqual(warning, "")
        self.assertEqual(paper["paper_id"], "arxiv:2606.02486")

    def test_resolve_target_date_keeps_explicit_manual_date(self):
        scraper = FakeScraper({
            "title": "Single Paper",
            "url": "https://arxiv.org/abs/2606.02486",
            "publication_date": "2026-05-31",
        })

        target, source, paper, arxiv_publication_date, warning = pipeline._resolve_target_date_for_run(
            scraper,
            target_date=date(2026, 6, 1),
            arxiv_url="https://arxiv.org/abs/2606.02486",
        )

        self.assertEqual(target, date(2026, 6, 1))
        self.assertEqual(source, "manual")
        self.assertIsNone(paper)
        self.assertEqual(arxiv_publication_date, "")
        self.assertEqual(warning, "")
        self.assertIsNone(scraper.single_url)

    def test_resolve_target_date_falls_back_when_arxiv_date_unknown(self):
        scraper = FakeScraper({"title": "Single Paper", "url": "https://arxiv.org/abs/2606.02486"})

        target, source, paper, arxiv_publication_date, warning = pipeline._resolve_target_date_for_run(
            scraper,
            target_date=None,
            arxiv_url="https://arxiv.org/abs/2606.02486",
        )

        self.assertIsInstance(target, date)
        self.assertEqual(source, "fallback_yesterday")
        self.assertEqual(paper["paper_id"], "arxiv:2606.02486")
        self.assertEqual(arxiv_publication_date, "")
        self.assertEqual(warning, "arxiv_publication_date_unavailable")

    def test_load_papers_fetches_and_persists_fresh_run(self):
        scraper = FakeScraper()
        state = FakeRunState()
        target = date(2026, 6, 1)

        papers = pipeline._load_papers_for_run(scraper, state, target, arxiv_url=None)

        self.assertEqual(scraper.target_date, target)
        self.assertEqual(papers[0]["paper_id"], "arxiv:2606.02486")
        self.assertEqual(state.set_calls[0][0], "fetched")

    def test_load_papers_uses_saved_state_when_resuming(self):
        saved = [{"title": "Saved Paper", "url": "https://arxiv.org/abs/2605.25802"}]
        scraper = FakeScraper()
        state = FakeRunState(stage="screened", papers=saved)

        papers = pipeline._load_papers_for_run(scraper, state, date(2026, 6, 1), arxiv_url=None)

        self.assertIsNone(scraper.target_date)
        self.assertEqual(papers[0]["paper_id"], "arxiv:2605.25802")
        self.assertEqual(state.set_calls, [])

    def test_failed_state_resume_keeps_saved_papers_without_clearing_failure(self):
        saved = [{"title": "Failed Paper", "url": "https://arxiv.org/abs/2605.25802"}]
        scraper = FakeScraper()
        state = FakeRunState(stage="failed", papers=saved)
        state.add_error(
            "llm_coarse_screening_failed",
            "provider unavailable",
            stage="coarse",
            paper_id="arxiv:2605.25802",
            retryable=True,
        )

        papers = pipeline._load_papers_for_run(scraper, state, date(2026, 6, 1), arxiv_url=None)

        self.assertEqual([paper["paper_id"] for paper in papers], ["arxiv:2605.25802"])
        self.assertIsNone(scraper.target_date)
        self.assertEqual(state.data["errors"][0]["code"], "llm_coarse_screening_failed")

    def test_source_retry_resolves_only_recovered_source_and_preserves_saved_papers(self):
        class ChangingSourceScraper(FakeScraper):
            def get_all_papers(self, target_date=None):
                self.target_date = target_date
                self.last_source_report = {
                    "sources": {
                        "arxiv": {"ok": True, "count": 1},
                        "huggingface": {
                            "ok": False,
                            "code": "source_degraded",
                            "message": "HF unavailable",
                            "retryable": True,
                        },
                    },
                    "warnings": [],
                }
                return [{"title": "Fresh", "url": "https://arxiv.org/abs/2606.00002"}]

        state = FakeRunState(
            stage="failed",
            papers=[{"title": "Saved", "url": "https://arxiv.org/abs/2606.00001"}],
        )
        state.add_error(
            "source_degraded",
            "arXiv unavailable",
            stage="fetch",
            paper_id="source:arxiv",
            title="arxiv",
            retryable=True,
        )

        papers = pipeline._load_papers_for_run(
            ChangingSourceScraper(),
            state,
            date(2026, 6, 1),
            arxiv_url=None,
        )

        self.assertEqual(
            {paper["paper_id"] for paper in papers},
            {"arxiv:2606.00001", "arxiv:2606.00002"},
        )
        self.assertEqual([(error["code"], error["paper_id"]) for error in state.data["errors"]], [
            ("source_degraded", "source:huggingface")
        ])

    def test_degraded_source_with_zero_results_finalizes_as_failed(self):
        scraper = FakeScraper()
        scraper.last_source_report = {
            "sources": {
                "arxiv": {
                    "ok": False,
                    "code": "source_degraded",
                    "message": "invalid HTTP 200 payload",
                    "retryable": True,
                },
                "huggingface": {"ok": True, "count": 0},
            }
        }
        state = FakeRunState()

        pipeline._record_source_report(state, scraper)
        summary = pipeline._finalize_run(state)

        self.assertFalse(summary["ok"])
        self.assertEqual(summary["stage"], "failed")
        self.assertEqual(summary["errors"][0]["code"], "source_degraded")

    def test_single_paper_none_never_reuses_other_saved_paper(self):
        class EmptySingleScraper(FakeScraper):
            def fetch_single_arxiv_paper(self, arxiv_url):
                self.single_url = arxiv_url
                return None

        state = FakeRunState(
            stage="completed",
            papers=[{"title": "Other", "url": "https://arxiv.org/abs/2605.00001", "score": 9.0}],
        )
        with self.assertRaisesRegex(Exception, "No metadata was returned") as raised:
            pipeline._load_papers_for_run(
                EmptySingleScraper(),
                state,
                date(2026, 6, 1),
                arxiv_url="https://arxiv.org/abs/2606.02486",
            )

        self.assertEqual(raised.exception.code, "single_paper_not_found")
        self.assertEqual(len(state.papers()), 1)

    def test_single_paper_identity_mismatch_is_typed_failure(self):
        scraper = FakeScraper({"title": "Wrong", "url": "https://arxiv.org/abs/2606.99999"})
        state = FakeRunState(stage="completed", papers=[])

        with self.assertRaises(Exception) as raised:
            pipeline._load_papers_for_run(
                scraper,
                state,
                date(2026, 6, 1),
                arxiv_url="https://arxiv.org/abs/2606.02486",
            )

        self.assertEqual(raised.exception.code, "single_paper_identity_mismatch")

    def test_successful_single_paper_retry_resolves_prior_fetch_errors(self):
        state = FakeRunState(stage="failed", papers=[])
        for code in (
            "single_paper_source_unavailable",
            "single_paper_identity_mismatch",
            "single_paper_not_found",
        ):
            state.add_error(code, "previous failure", stage="fetch", retryable=True)
        state.add_error("source_degraded", "HF down", stage="fetch", paper_id="source:huggingface", retryable=True)

        papers = pipeline._load_papers_for_run(
            FakeScraper({"title": "Requested", "url": "https://arxiv.org/abs/2606.02486"}),
            state,
            date(2026, 6, 1),
            arxiv_url="https://arxiv.org/abs/2606.02486",
        )

        self.assertEqual([paper["paper_id"] for paper in papers], ["arxiv:2606.02486"])
        self.assertEqual([(error["code"], error["paper_id"]) for error in state.data["errors"]], [
            ("source_degraded", "source:huggingface")
        ])

    def test_single_arxiv_injects_even_when_daily_state_completed(self):
        scraper = FakeScraper()
        state = FakeRunState(stage="completed", papers=[{"title": "Saved", "url": "https://arxiv.org/abs/2605.25802", "score": 8.0}])

        papers = pipeline._load_papers_for_run(
            scraper,
            state,
            date(2026, 6, 1),
            arxiv_url="https://arxiv.org/abs/2606.02486",
        )

        self.assertEqual(scraper.single_url, "https://arxiv.org/abs/2606.02486")
        injected = [p for p in papers if p["paper_id"] == "arxiv:2606.02486"][0]
        self.assertTrue(injected["forced_deep"])
        self.assertTrue(injected["in_daily_digest"])
        self.assertIn("single", injected["paper_sources"])

    def test_run_coarse_screening_updates_each_paper_and_stage(self):
        state = FakeRunState()
        analyser = FakeAnalyser()
        papers = [
            {"title": "A", "url": "https://arxiv.org/abs/2606.00001"},
            {"title": "B", "url": "https://arxiv.org/abs/2606.00002"},
        ]

        screened = pipeline._run_coarse_screening(papers, analyser, state, resume=True)

        self.assertEqual([p["coarse_score"] for p in screened], [8.0, 8.0])
        self.assertEqual(len(state.updated), 2)
        self.assertEqual(state.marked, ["coarse_screened"])

    def test_successful_coarse_retry_resolves_only_its_previous_error(self):
        paper = {"title": "A", "url": "https://arxiv.org/abs/2606.00001", "paper_id": "arxiv:2606.00001"}
        state = FakeRunState(stage="failed", papers=[paper])
        state.add_error(
            "llm_coarse_screening_failed",
            "provider unavailable",
            stage="coarse",
            paper_id="arxiv:2606.00001",
            title="A",
            retryable=True,
        )
        state.add_error(
            "source_degraded",
            "arXiv unavailable",
            stage="fetch",
            paper_id="source:arxiv",
            title="arxiv",
            retryable=True,
        )

        pipeline._run_coarse_screening([paper], FakeAnalyser(), state, resume=True)

        self.assertEqual([(error["code"], error["paper_id"]) for error in state.data["errors"]], [
            ("source_degraded", "source:arxiv")
        ])

    def test_coarse_screening_failure_is_recorded_and_final_run_is_not_ok(self):
        class FailingAnalyser(FakeAnalyser):
            def coarse_screen_paper(self, paper):
                return {
                    "coarse_score": 0.0,
                    "score": 0.0,
                    "relevance": 0.0,
                    "evidence": 0.0,
                    "method_completeness": 0.0,
                    "should_rescreen": False,
                    "reason": "provider unavailable",
                    "short_title": paper["title"],
                    "screening_error": {
                        "code": "llm_coarse_screening_failed",
                        "message": "provider unavailable",
                        "exception": "RuntimeError",
                        "retryable": True,
                    },
                }

        state = FakeRunState()
        papers = [{"title": "Paper", "url": "https://arxiv.org/abs/2606.02486"}]
        pipeline._run_coarse_screening(papers, FailingAnalyser(), state)

        self.assertEqual(state.data["errors"][0]["code"], "llm_coarse_screening_failed")
        self.assertTrue(state.data["errors"][0]["retryable"])
        summary = pipeline._finalize_run(state)
        self.assertFalse(summary["ok"])
        self.assertEqual(state.data["stage"], "failed")

    def test_pdf_failure_is_retryable_and_failed_run_keeps_cache(self):
        state = FakeRunState(stage="screened")
        paper = {
            "title": "Paper",
            "paper_id": "arxiv:2606.02486",
        }
        pipeline._record_deep_pdf_error(state, paper, "PDF download or validation failed.")

        with patch("main._cleanup_completed_run_pdf_cache") as cleanup:
            summary = pipeline._finish_run(state, cache_cleanup_day_start=123.0, cache_paths={"cached.pdf"})

        self.assertFalse(summary["ok"])
        self.assertEqual(summary["stage"], "failed")
        self.assertEqual(state.data["errors"][0]["code"], "pdf_unavailable")
        self.assertTrue(state.data["errors"][0]["retryable"])
        cleanup.assert_not_called()

    def test_build_rescreen_pool_prioritizes_true_then_fills_remaining_slots(self):
        papers = [
            self._coarse("true-low", True, 7.0),
            self._coarse("false-high", False, 9.5),
            self._coarse("true-high", True, 8.5),
            self._coarse("false-mid", False, 8.0),
        ]
        cfg = {
            "screening_second_stage_top_k": 3,
            "screening_second_stage_ratio": 1.0,
            "screening_second_stage_max_k": 3,
        }

        selected = pipeline._build_rescreen_pool(papers, cfg)

        self.assertEqual([p["title"] for p in selected], ["true-high", "true-low", "false-high"])

    def test_build_rescreen_pool_always_includes_forced_papers(self):
        forced = self._coarse("forced-low", False, 1.0)
        forced["forced_deep"] = True
        papers = [self._coarse("regular-high", True, 9.0), forced]

        selected = pipeline._build_rescreen_pool(
            papers,
            {"screening_second_stage_top_k": 1, "screening_second_stage_ratio": 0.1, "screening_second_stage_max_k": 1},
        )

        self.assertIn("forced-low", [p["title"] for p in selected])

    def test_drop_screening_excerpts_removes_temporary_context(self):
        papers = [{"title": "A", "screening_document_excerpt": "temporary"}, {"title": "B"}]

        pipeline._drop_screening_excerpts(papers)

        self.assertNotIn("screening_document_excerpt", papers[0])
        self.assertNotIn("screening_document_excerpt", papers[1])

    def test_mark_digest_membership_backfills_to_target_count(self):
        cfg = {
            "openrouter": {"threshold_score": 7},
            "analysis": {"daily_digest_min_score": 7.0, "daily_digest_target_min_count": 5},
        }
        papers = [
            self._screened("Hard Threshold", 7.4),
            self._screened("Backfill A", 6.8),
            self._screened("Backfill B", 6.6),
            self._screened("Backfill C", 6.4),
            self._screened("Backfill D", 6.2),
            self._screened("Left Out", 5.1, rigor=2.0, evidence=2.0),
        ]

        info = pipeline._mark_digest_membership(papers, cfg, provider="openrouter")

        selected = [paper["title"] for paper in papers if paper.get("in_daily_digest")]
        self.assertEqual(len(selected), 5)
        self.assertEqual(info["threshold_count"], 1)
        self.assertEqual(info["backfill_count"], 4)
        self.assertNotIn("Left Out", selected)

    def test_mark_digest_and_deep_membership_preserve_forced_paper(self):
        cfg = {
            "openrouter": {"threshold_score": 7},
            "analysis": {"daily_digest_min_score": 7.0, "daily_digest_target_min_count": 1},
        }
        forced = self._screened("Forced Low", 2.0)
        forced["forced_deep"] = True
        papers = [self._screened("Regular High", 8.0), forced]

        info = pipeline._mark_digest_membership(papers, cfg, provider="openrouter")
        pipeline._mark_deep_selection(papers, [papers[0]])

        self.assertTrue(forced["in_daily_digest"])
        self.assertTrue(forced["selected_for_deep_analysis"])
        self.assertGreaterEqual(info["forced_count"], 1)

    def test_collect_force_preserved_deep_keeps_completed_note_before_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "Research_Notes" / "Preserved.md"
            note.parent.mkdir()
            note.write_text("# Preserved Paper\n", encoding="utf-8")
            state = FakeRunState(
                stage="completed",
                papers=[{
                    "title": "Preserved Paper",
                    "url": "https://arxiv.org/abs/2606.11111",
                    "score": 8.2,
                    "selected_for_deep_analysis": True,
                    "note_path": str(note),
                    "provider_sources": ["openrouter"],
                }],
            )

            preserved = pipeline._collect_force_preserved_deep(
                state,
                self._config(tmp),
                date(2026, 6, 1),
            )

        self.assertEqual(len(preserved), 1)
        self.assertEqual(preserved[0]["paper_id"], "arxiv:2606.11111")
        self.assertTrue(preserved[0]["preserved_deep"])
        self.assertTrue(preserved[0]["deep_analysis_completed"])
        self.assertTrue(preserved[0]["selected_for_deep_analysis"])
        self.assertTrue(preserved[0]["in_daily_digest"])
        self.assertTrue(preserved[0]["note_path"].endswith("Preserved.md"))

    def test_collect_force_preserved_deep_ignores_incomplete_forced_without_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = FakeRunState(
                stage="screened",
                papers=[{
                    "title": "Missing Note",
                    "url": "https://arxiv.org/abs/2606.22222",
                    "score": 8.0,
                    "forced_deep": True,
                    "note_path": str(Path(tmp) / "Research_Notes" / "Missing.md"),
                }],
            )

            preserved = pipeline._collect_force_preserved_deep(
                state,
                self._config(tmp),
                date(2026, 6, 1),
            )

        self.assertEqual(preserved, [])

    def test_merge_preserved_deep_dedupes_and_keeps_note_metadata(self):
        fresh = self._screened("Fresh Score", 8.7)
        fresh["url"] = "https://arxiv.org/abs/2606.33333"
        fresh["provider_sources"] = ["openrouter"]
        fresh["tags"] = ["fresh"]
        preserved = self._screened("Fresh Score", 7.2)
        preserved.update({
            "url": "https://arxiv.org/abs/2606.33333",
            "note_path": "Research_Notes/Fresh Score.md",
            "manual_deep_completed_at": "2026-06-01T09:00:00",
            "preserved_deep": True,
            "deep_analysis_completed": True,
            "selected_for_deep_analysis": True,
            "in_daily_digest": True,
            "provider_sources": ["doubao"],
            "tags": ["preserved"],
        })

        merged = pipeline._merge_preserved_deep_papers([fresh], [preserved])

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["score"], 8.7)
        self.assertEqual(merged[0]["note_path"], "Research_Notes/Fresh Score.md")
        self.assertTrue(merged[0]["preserved_deep"])
        self.assertIn("openrouter", merged[0]["provider_sources"])
        self.assertIn("doubao", merged[0]["provider_sources"])
        self.assertIn("fresh", merged[0]["tags"])
        self.assertIn("preserved", merged[0]["tags"])

    def test_pending_deep_papers_skips_preserved_completed_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "Research_Notes" / "Already Done.md"
            note.parent.mkdir()
            note.write_text("# Already Done\n", encoding="utf-8")
            preserved = self._screened("Already Done", 8.1)
            preserved.update({
                "url": "https://arxiv.org/abs/2606.44444",
                "note_path": str(note),
                "preserved_deep": True,
                "deep_analysis_completed": True,
            })
            pending = self._screened("Needs Deep", 8.4)

            result = pipeline._pending_deep_papers(
                [preserved, pending],
                date(2026, 6, 1),
                config=self._config(tmp),
            )

        self.assertEqual([paper["title"] for paper in result], ["Needs Deep"])

    def test_mark_digest_membership_includes_preserved_deep(self):
        cfg = {
            "openrouter": {"threshold_score": 7},
            "analysis": {"daily_digest_min_score": 7.0, "daily_digest_target_min_count": 1},
        }
        preserved = self._screened("Preserved Low", 2.0)
        preserved["preserved_deep"] = True
        papers = [self._screened("Regular High", 8.0), preserved]

        info = pipeline._mark_digest_membership(papers, cfg, provider="openrouter")

        self.assertTrue(preserved["in_daily_digest"])
        self.assertGreaterEqual(info["forced_count"], 1)

    def test_paper_pdf_candidates_derive_arxiv_pdf_from_huggingface_url(self):
        candidates = pipeline._paper_pdf_url_candidates({
            "title": "Rethinking",
            "url": "https://huggingface.co/papers/2605.25802",
        })

        self.assertNotIn("https://huggingface.co/papers/2605.25802", candidates)
        self.assertIn("https://arxiv.org/pdf/2605.25802.pdf", candidates)

    def test_download_paper_pdf_uses_derived_candidate_and_requires_local_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            local_pdf = Path(tmp) / "paper.pdf"
            local_pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 2048)
            calls = []

            def fake_download(url, title, destination_folder=None, **kwargs):
                calls.append(url)
                if url == "https://arxiv.org/pdf/2605.25802.pdf":
                    return str(local_pdf)
                return None

            with patch("main.download_pdf", side_effect=fake_download):
                pdf_path = pipeline.download_paper_pdf(
                    {"title": "Rethinking", "url": "https://huggingface.co/papers/2605.25802"},
                    destination_folder=tmp,
                )

        self.assertEqual(pdf_path, str(local_pdf))
        self.assertNotIn("https://huggingface.co/papers/2605.25802", calls)
        self.assertIn("https://arxiv.org/pdf/2605.25802.pdf", calls)

    def test_download_paper_pdf_rejects_non_pdf_local_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_file = Path(tmp) / "not-a-pdf.pdf"
            bad_file.write_bytes(b"<html>" + b"x" * 2048)
            good_pdf = Path(tmp) / "paper.pdf"
            good_pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 2048)

            def fake_download(url, title, destination_folder=None, **kwargs):
                if url == "https://example.com/not-really.pdf":
                    return str(bad_file)
                if url == "https://arxiv.org/pdf/2605.25802.pdf":
                    return str(good_pdf)
                return None

            with patch("main.download_pdf", side_effect=fake_download):
                pdf_path = pipeline.download_paper_pdf(
                    {
                        "title": "Rethinking",
                        "pdf_url": "https://example.com/not-really.pdf",
                        "arxiv_id": "2605.25802",
                    },
                    destination_folder=tmp,
                )

        self.assertEqual(pdf_path, str(good_pdf))

    def test_pdf_download_404_is_permanent_typed_failure(self):
        response = SimpleNamespace(
            status_code=404,
            url="https://public.example/missing.pdf",
            headers={},
            close=lambda: None,
        )
        with tempfile.TemporaryDirectory() as tmp, \
             patch("main.request_public_url", return_value=response):
            with self.assertRaises(pipeline.PDFNotFoundError) as raised:
                pipeline.download_pdf(
                    "https://public.example/missing.pdf",
                    "Missing",
                    destination_folder=tmp,
                    retries=1,
                )

        self.assertEqual(raised.exception.code, "pdf_not_found")
        self.assertFalse(raised.exception.retryable)
        self.assertEqual(raised.exception.status_code, 404)

    def test_pdf_connection_failure_is_retryable_typed_failure(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch("main.request_public_url", side_effect=RuntimeError("timeout")):
            with self.assertRaises(pipeline.PDFNetworkError) as raised:
                pipeline.download_pdf(
                    "https://public.example/paper.pdf",
                    "Paper",
                    destination_folder=tmp,
                    retries=1,
                )

        self.assertEqual(raised.exception.code, "pdf_network_error")
        self.assertTrue(raised.exception.retryable)

    def test_pdf_destination_filename_uses_paper_identity(self):
        payload = b"%PDF-1.4\n" + b"x" * 2048

        def response():
            return SimpleNamespace(
                status_code=200,
                url="https://public.example/paper.pdf",
                headers={"Content-Length": str(len(payload))},
                iter_content=lambda chunk_size: [payload],
                close=lambda: None,
            )

        with tempfile.TemporaryDirectory() as tmp, \
             patch("main.request_public_url", side_effect=[response(), response()]):
            first = pipeline.download_pdf(
                "https://public.example/paper.pdf?one",
                "Same Title",
                destination_folder=tmp,
                retries=1,
                paper_identity="external:one",
            )
            second = pipeline.download_pdf(
                "https://public.example/paper.pdf?two",
                "Same Title",
                destination_folder=tmp,
                retries=1,
                paper_identity="external:two",
            )

        self.assertNotEqual(Path(first).name, Path(second).name)

    def test_non_arxiv_pdf_identity_uses_url_not_shared_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            local_pdf = Path(tmp) / "paper.pdf"
            local_pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 2048)
            identities = []

            def fake_download(url, title, **kwargs):
                identities.append(kwargs["paper_identity"])
                return str(local_pdf)

            with patch("main.download_pdf", side_effect=fake_download):
                pipeline.download_paper_pdf(
                    {"title": "Same", "pdf_url": "https://one.example/paper.pdf"},
                    destination_folder=tmp,
                )
                pipeline.download_paper_pdf(
                    {"title": "Same", "pdf_url": "https://two.example/paper.pdf"},
                    destination_folder=tmp,
                )

        self.assertNotEqual(identities[0], identities[1])
        self.assertIn("one.example", identities[0])
        self.assertIn("two.example", identities[1])

    def test_permanent_pdf_error_is_recorded_as_non_retryable(self):
        state = FakeRunState()
        paper = {"title": "Paper", "paper_id": "arxiv:2606.00001"}

        pipeline._record_deep_pdf_error(state, paper, pipeline.PDFUnsafeUrlError("private target"))

        self.assertEqual(state.data["errors"][0]["code"], "pdf_unsafe_url")
        self.assertFalse(state.data["errors"][0]["retryable"])

    def test_cleanup_completed_run_pdf_cache_removes_only_pdf_cache_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp) / "Cache" / "pdfs"
            cache_dir.mkdir(parents=True)
            today_pdf = cache_dir / "today.pdf"
            today_pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 2048)
            old_touched_pdf = cache_dir / "old-touched.pdf"
            old_touched_pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 2048)
            metadata = cache_dir / "arxiv_pdf_cooldown.json"
            metadata.write_text("{}", encoding="utf-8")
            outside_pdf = Path(tmp) / "outside.pdf"
            outside_pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 2048)

            day_start = today_pdf.stat().st_mtime - 1
            old_time = day_start - 86400
            import os
            os.utime(old_touched_pdf, (old_time, old_time))

            with patch("main.PDF_CACHE_DIR", str(cache_dir)):
                removed = pipeline._cleanup_completed_run_pdf_cache(
                    day_start,
                    cache_paths={str(old_touched_pdf), str(outside_pdf)},
                )

            self.assertEqual(removed, 2)
            self.assertFalse(today_pdf.exists())
            self.assertFalse(old_touched_pdf.exists())
            self.assertTrue(metadata.exists())
            self.assertTrue(outside_pdf.exists())

    def test_run_rigorous_screening_updates_promoted_and_marks_others_coarse_only(self):
        analyser = FakeAnalyser()
        state = FakeRunState(stage="coarse_screened")
        coarse_only = self._coarse("coarse-only", False, 6.9)
        promoted = self._coarse("promoted", True, 8.8)
        papers = [coarse_only, promoted]

        pipeline._run_rigorous_screening(
            papers,
            [promoted],
            analyser,
            state,
            {"screening_second_stage_use_pdf_context": False},
            resume=True,
        )

        self.assertEqual(coarse_only["screening_stage"], "coarse_only")
        self.assertEqual(promoted["screening_stage"], "detailed")
        self.assertEqual(promoted["score"], 8.6)
        self.assertEqual(analyser.screened_titles, ["promoted"])
        self.assertEqual(state.marked, ["screened"])

    def test_rigorous_screening_failure_is_recorded(self):
        class FailingAnalyser(FakeAnalyser):
            def screen_paper(self, paper):
                return {
                    "score": 0.0,
                    "reason": "provider unavailable",
                    "short_title": paper["title"],
                    "screening_stage": "detailed",
                    "screening_error": {
                        "code": "llm_detailed_screening_failed",
                        "message": "provider unavailable",
                        "exception": "RuntimeError",
                        "retryable": True,
                    },
                }

        state = FakeRunState(stage="coarse_screened")
        promoted = self._coarse("promoted", True, 8.8)
        pipeline._run_rigorous_screening(
            [promoted],
            [promoted],
            FailingAnalyser(),
            state,
            {"screening_second_stage_use_pdf_context": False},
            resume=False,
        )

        self.assertEqual(state.data["errors"][0]["code"], "llm_detailed_screening_failed")
        self.assertEqual(state.data["errors"][0]["stage"], "screen")
        self.assertFalse(pipeline._finalize_run(state)["ok"])

    @staticmethod
    def _coarse(title, should_rescreen, score):
        return {
            "title": title,
            "should_rescreen": should_rescreen,
            "coarse_score": score,
            "coarse_relevance": score,
            "coarse_evidence": score,
            "coarse_method_completeness": score,
        }

    @staticmethod
    def _screened(title, score, novelty=8.0, rigor=8.0, evidence=8.0):
        return {
            "title": title,
            "score": score,
            "novelty": novelty,
            "rigor": rigor,
            "evidence": evidence,
            "reproducibility": 7.0,
            "confidence": 8.0,
            "red_flags": [],
        }

    @staticmethod
    def _config(tmp):
        return {
            "openrouter": {"threshold_score": 7},
            "analysis": {"daily_digest_min_score": 7.0, "daily_digest_target_min_count": 5},
            "obsidian": {
                "vault_path": tmp,
                "daily_digest_folder": "Daily_Papers",
                "detailed_notes_folder": "Research_Notes",
                "research_index_folder": "Research_Index",
                "research_brief_folder": "Research_Briefs",
                "pdf_storage_folder": "PDFs",
            },
        }


if __name__ == "__main__":
    unittest.main()
