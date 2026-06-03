import shutil
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.research_brief import ResearchBriefGenerator, resolve_period  # noqa: E402


class ResearchBriefGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        notes_dir = Path(self.tmp) / "Research_Notes"
        notes_dir.mkdir(parents=True, exist_ok=True)
        self.config = {
            "obsidian": {
                "vault_path": self.tmp,
                "detailed_notes_folder": "Research_Notes",
                "research_index_folder": "Research_Index",
                "research_brief_folder": "Research_Briefs",
            }
        }
        (notes_dir / "AHEAD.md").write_text(
            """---
tags:
  - paper
aliases:
  - "AHEAD Latent World Model"
paper_id: "arxiv:2606.02486"
arxiv_id: "2606.02486"
publication_date: "2026-06-01"
score: 8.4
institutions:
  - "Shanghai AI Lab"
github: "https://github.com/example/ahead"
project_page: "None"
---

# AHEAD Latent World Model

## 📌 Abstract
A latent world model improves dynamic VLA manipulation by predicting future interaction states.

## Core Contribution
The paper adds a predictive latent dynamics layer that helps a VLA policy reason about moving objects.

## Limitations
The method still depends on reliable perception and task-specific evaluation.
""",
            encoding="utf-8",
        )
        (notes_dir / "Baseline.md").write_text(
            """---
tags:
  - paper
aliases:
  - "Baseline"
paper_id: "arxiv:2606.00001"
arxiv_id: "2606.00001"
publication_date: "2026-06-02"
score: 7.6
institutions:
  - "CMU"
github: "None"
project_page: "https://example.com"
---

# Baseline

## 📌 Abstract
This benchmark studies robot manipulation in simulation with several baselines and ablations.
""",
            encoding="utf-8",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_resolve_week_period(self):
        start, end, label, brief_type = resolve_period(week="2026-W23")
        self.assertEqual(start.isoformat(), "2026-06-01")
        self.assertEqual(end.isoformat(), "2026-06-07")
        self.assertEqual(label, "2026-W23")
        self.assertEqual(brief_type, "week")

    def test_generate_range_brief(self):
        generator = ResearchBriefGenerator(self.config)
        path = generator.generate("2026-06-01", "2026-06-07", "2026-W23", "week")
        text = Path(path).read_text(encoding="utf-8")
        self.assertIn("# Research Brief: 2026-W23", text)
        self.assertIn("## 1. Executive Summary", text)
        self.assertIn("## 8. Open Research Questions", text)
        self.assertIn("[[AHEAD]]", text)
        self.assertIn("Shanghai AI Lab", text)
        self.assertIn("paper_count: 2", text)


if __name__ == "__main__":
    unittest.main()
