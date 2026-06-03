import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.scoring import (  # noqa: E402
    calibrated_screening_score,
    coarse_screening_score,
    dynamic_stage2_top_k,
    passes_quality_gate,
    select_deep_analysis_papers,
)


class ScreeningScoreCalibrationTest(unittest.TestCase):
    def test_high_quality_paper_keeps_high_decimal_score(self):
        score = calibrated_screening_score(
            relevance=9.2,
            novelty=8.8,
            rigor=9.0,
            evidence=8.7,
            reproducibility=7.8,
            confidence=8.0,
            red_flags=[],
        )
        self.assertIsInstance(score, float)
        self.assertEqual(score, round(score, 1))
        self.assertGreaterEqual(score, 8.6)

    def test_low_relevance_caps_score(self):
        score = calibrated_screening_score(
            relevance=3.8,
            novelty=9.5,
            rigor=9.0,
            evidence=9.0,
            reproducibility=8.0,
            confidence=8.0,
            red_flags=[],
        )
        self.assertLessEqual(score, 6.0)

    def test_weak_rigor_or_evidence_caps_score(self):
        score = calibrated_screening_score(
            relevance=9.0,
            novelty=9.0,
            rigor=3.9,
            evidence=8.5,
            reproducibility=8.0,
            confidence=8.0,
            red_flags=[],
        )
        self.assertLessEqual(score, 7.0)

    def test_confidence_and_red_flags_make_score_conservative(self):
        clean = calibrated_screening_score(
            relevance=8.8,
            novelty=8.6,
            rigor=8.4,
            evidence=8.3,
            reproducibility=7.2,
            confidence=8.0,
            red_flags=[],
        )
        risky = calibrated_screening_score(
            relevance=8.8,
            novelty=8.6,
            rigor=8.4,
            evidence=8.3,
            reproducibility=7.2,
            confidence=3.8,
            red_flags=["missing baselines", "unclear task setup"],
        )
        self.assertLess(risky, clean)
        self.assertLessEqual(risky, 7.0)

    def test_coarse_score_filters_empty_or_off_topic_abstracts(self):
        off_topic = coarse_screening_score(
            relevance=3.0,
            evidence=9.0,
            method_completeness=9.0,
        )
        vague = coarse_screening_score(
            relevance=7.0,
            evidence=3.5,
            method_completeness=3.8,
        )
        self.assertLessEqual(off_topic, 5.0)
        self.assertLessEqual(vague, 5.0)


class ScreeningSelectionTest(unittest.TestCase):
    def test_dynamic_stage2_top_k_is_recall_oriented_but_bounded(self):
        self.assertEqual(dynamic_stage2_top_k(0), 0)
        self.assertEqual(dynamic_stage2_top_k(5, min_k=10, ratio=0.25, max_k=20), 5)
        self.assertEqual(dynamic_stage2_top_k(50, min_k=10, ratio=0.25, max_k=20), 13)
        self.assertEqual(dynamic_stage2_top_k(200, min_k=10, ratio=0.25, max_k=20), 20)

    def test_quality_gate_rejects_red_flag_heavy_papers(self):
        paper = {
            "score": 8.9,
            "relevance": 8.0,
            "rigor": 8.0,
            "evidence": 8.0,
            "confidence": 8.0,
            "red_flags": ["weak baseline", "unclear protocol", "possible leakage"],
        }
        self.assertFalse(passes_quality_gate(paper, {"red_flags_max": 2}))

    def test_deep_analysis_selection_uses_lower_and_upper_thresholds(self):
        cfg = {
            "daily_deep_analysis_min": 1,
            "daily_deep_analysis_base_max": 2,
            "deep_analysis_lower_threshold": 7.5,
            "deep_analysis_extra_threshold": 8.8,
            "deep_analysis_quality_gate": {
                "relevance": 6.0,
                "rigor": 6.0,
                "evidence": 6.0,
                "confidence": 4.0,
                "red_flags_max": 2,
            },
        }
        papers = [
            self._paper("A", 9.2),
            self._paper("B", 9.0),
            self._paper("C", 8.9),
            self._paper("D", 8.7),
            self._paper("E", 7.4),
            self._paper("F", 9.4, relevance=5.9),
        ]
        selected, diagnostics = select_deep_analysis_papers(papers, cfg, provider_threshold=7.0)
        self.assertEqual([paper["title"] for paper in selected], ["A", "B", "C"])
        self.assertEqual(diagnostics["candidate_count"], 5)
        self.assertEqual(diagnostics["quality_passed_count"], 4)
        self.assertEqual(diagnostics["extra_count"], 1)

    def test_no_deep_analysis_when_all_scores_below_lower_threshold(self):
        cfg = {
            "daily_deep_analysis_min": 1,
            "daily_deep_analysis_base_max": 2,
            "deep_analysis_lower_threshold": 7.5,
            "deep_analysis_extra_threshold": 8.8,
            "deep_analysis_quality_gate": {"relevance": 6.0, "rigor": 6.0, "evidence": 6.0},
        }
        selected, diagnostics = select_deep_analysis_papers(
            [self._paper("A", 7.4), self._paper("B", 7.2)],
            cfg,
            provider_threshold=7.0,
        )
        self.assertEqual(selected, [])
        self.assertEqual(diagnostics["candidate_count"], 0)

    @staticmethod
    def _paper(title, score, relevance=8.0):
        return {
            "title": title,
            "score": score,
            "relevance": relevance,
            "novelty": 8.0,
            "rigor": 8.0,
            "evidence": 8.0,
            "reproducibility": 7.0,
            "confidence": 8.0,
            "red_flags": [],
        }


if __name__ == "__main__":
    unittest.main()
