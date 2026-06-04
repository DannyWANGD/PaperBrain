import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main as pipeline  # noqa: E402


class FakeScraper:
    def __init__(self):
        self.target_date = None
        self.single_url = None

    def get_all_papers(self, target_date=None):
        self.target_date = target_date
        return [{"title": "Fetched Paper", "url": "https://arxiv.org/abs/2606.02486"}]

    def fetch_single_arxiv_paper(self, arxiv_url):
        self.single_url = arxiv_url
        return {"title": "Single Paper", "url": arxiv_url}


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
        self.data = {"stage": stage, "papers": papers or []}
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

    def mark_stage(self, stage):
        self.data["stage"] = stage
        self.marked.append(stage)


class MainPipelineHelperTest(unittest.TestCase):
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

    def test_drop_screening_excerpts_removes_temporary_context(self):
        papers = [{"title": "A", "screening_document_excerpt": "temporary"}, {"title": "B"}]

        pipeline._drop_screening_excerpts(papers)

        self.assertNotIn("screening_document_excerpt", papers[0])
        self.assertNotIn("screening_document_excerpt", papers[1])

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

            def fake_download(url, title, destination_folder=None):
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

            def fake_download(url, title, destination_folder=None):
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


if __name__ == "__main__":
    unittest.main()
