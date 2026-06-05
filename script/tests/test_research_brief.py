import shutil
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.research_brief import MANUAL_END, MANUAL_START, ResearchBriefGenerator, resolve_period  # noqa: E402


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

    def test_resolve_period_from_mode_and_date(self):
        start, end, label, brief_type = resolve_period(mode="week", date_value="2026-06-03")
        self.assertEqual(start.isoformat(), "2026-06-01")
        self.assertEqual(end.isoformat(), "2026-06-07")
        self.assertEqual(label, "2026-W23")
        self.assertEqual(brief_type, "week")

        start, end, label, brief_type = resolve_period(mode="month", date_value="2026-06-03")
        self.assertEqual(start.isoformat(), "2026-06-01")
        self.assertEqual(end.isoformat(), "2026-06-30")
        self.assertEqual(label, "2026-06")
        self.assertEqual(brief_type, "month")

    def test_generate_range_brief(self):
        generator = ResearchBriefGenerator(self.config)
        path = generator.generate("2026-06-01", "2026-06-07", "2026-W23", "week")
        text = Path(path).read_text(encoding="utf-8")
        self.assertIn("# Research Brief: 2026-W23", text)
        self.assertIn("## 1. Executive Summary", text)
        self.assertIn("## 8. Open Research Questions", text)
        self.assertIn("## 9. Manual Notes", text)
        self.assertIn(MANUAL_START, text)
        self.assertIn(MANUAL_END, text)
        self.assertIn("[[AHEAD]]", text)
        self.assertIn("Shanghai AI Lab", text)
        self.assertIn("paper_count: 2", text)

    def test_generate_brief_includes_daily_digest_entries(self):
        daily_dir = Path(self.tmp) / "Daily_Papers"
        daily_dir.mkdir(parents=True, exist_ok=True)
        (daily_dir / "2026-06-03-PaperDigest.md").write_text(
            """# 2026-06-03 - Paper Digest
## Summary
Total Papers: 1 | High Impact: 1

## Papers List
### Digest Only Robot Paper (Score: 8.1/10)
- **Innovation**: A digest-only planning method improves robot manipulation.
- **Limitations**: Evaluation is narrow.
- **Link**: [Web Link](http://arxiv.org/abs/2606.05015v1)
- **Authors**: Ada Lovelace
- **Institutions**: Digest Lab
- **Tags**: #domain/world_model #method/planning #task/manipulation #type/method

---
""",
            encoding="utf-8",
        )

        generator = ResearchBriefGenerator(self.config)
        path = generator.generate("2026-06-01", "2026-06-07", "2026-W23", "week")
        text = Path(path).read_text(encoding="utf-8")

        self.assertIn("[[Digest Only Robot Paper]]", text)
        self.assertIn("Digest Lab", text)
        self.assertIn("paper_count: 3", text)

    def test_daily_digest_wikilink_merges_with_existing_note_name(self):
        daily_dir = Path(self.tmp) / "Daily_Papers"
        daily_dir.mkdir(parents=True, exist_ok=True)
        (daily_dir / "2026-06-01-PaperDigest.md").write_text(
            """# 2026-06-01 - Paper Digest
## Summary
Total Papers: 1 | High Impact: 1

## Papers List
### AHEAD: Different Official Digest Title (Score: 8.9/10)
- **Innovation**: The daily digest uses a longer display title than the local note.
- **Limitations**: Evaluation is narrow.
- **Link**: [[AHEAD]]
- **Authors**: Ada Lovelace
- **Institutions**: Digest Lab
- **Tags**: #domain/vla #domain/world_model #method/latent_world_model #type/method

---
""",
            encoding="utf-8",
        )

        generator = ResearchBriefGenerator(self.config)
        path = generator.generate("2026-06-01", "2026-06-07", "2026-W23", "week")
        text = Path(path).read_text(encoding="utf-8")

        self.assertIn("paper_count: 2", text)
        self.assertIn("| 1 | [[AHEAD]] | 8.9 |", text)
        self.assertNotIn("[[AHEAD Different Official Digest Title]]", text)
        self.assertNotIn("[[AHEAD Latent World Model]]", text)
        self.assertIn("**[[AHEAD]]**:", text)

    def test_manual_notes_are_preserved_on_regeneration(self):
        generator = ResearchBriefGenerator(self.config)
        path = Path(generator.generate("2026-06-01", "2026-06-07", "2026-W23", "week"))
        original = path.read_text(encoding="utf-8")
        manual_body = "- Keep this hand-written synthesis."
        path.write_text(
            original.replace(
                f"{MANUAL_START}\n{MANUAL_END}",
                f"{MANUAL_START}\n{manual_body}\n{MANUAL_END}",
            ),
            encoding="utf-8",
        )

        generator.generate("2026-06-01", "2026-06-07", "2026-W23", "week")
        regenerated = path.read_text(encoding="utf-8")

        self.assertIn(f"{MANUAL_START}\n{manual_body}\n{MANUAL_END}", regenerated)


if __name__ == "__main__":
    unittest.main()
