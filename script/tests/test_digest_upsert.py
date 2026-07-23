import re
import shutil
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.obsidian_writer import ObsidianWriter  # noqa: E402


class DailyDigestUpsertTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.config = {
            "openrouter": {"threshold_score": 7},
            "analysis": {"daily_digest_min_score": 7.0, "daily_digest_target_min_count": 5},
            "obsidian": {
                "vault_path": self.tmp,
                "daily_digest_folder": "Daily_Papers",
                "detailed_notes_folder": "Research_Notes",
                "pdf_storage_folder": "PDFs",
                "daily_digest_template": (
                    "# 📅 {{date}} - Paper Digest\n"
                    "## Summary\n"
                    "Total Papers: {{total_count}} | High Impact: {{high_impact_count}}\n\n"
                    "## 📑 Papers List\n"
                    "{{content}}"
                ),
            },
        }
        self.writer = ObsidianWriter(self.config, provider="openrouter")
        digest = Path(self.tmp) / "Daily_Papers" / "2026-06-01-PaperDigest.md"
        digest.write_text(
            "# 📅 2026-06-01 - Paper Digest\n"
            "## Summary\n"
            "Total Papers: 1 | High Impact: 1\n\n"
            "## 📑 Papers List\n"
            "### ✨ Existing Paper (Score: 7.2/10)\n"
            "- **💡 Innovation**: Existing.\n"
            "- **⚠️ Limitations**: Existing.\n"
            "- **🔗 Link**: [Web Link](https://example.com)\n"
            "- **👥 Authors**: A\n\n"
            "---\n",
            encoding="utf-8",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_insert_sorted_and_skip_duplicate(self):
        paper = {
            "title": "AHEAD",
            "url": "https://arxiv.org/abs/2606.02486v1",
            "pdf_url": "https://arxiv.org/pdf/2606.02486v1",
            "published": date(2026, 6, 1),
            "score": 8.4,
            "innovation": "Predictive VLA wrapper.",
            "limitations": "Needs optical flow.",
            "authors": ["Author One"],
            "institutions": ["Shanghai AI Lab", "Tsinghua University"],
            "tags": ["domain/vla"],
        }
        path = self.writer.upsert_single_paper_digest_entry(paper)
        text = Path(path).read_text(encoding="utf-8")
        self.assertIn("Total Papers: 2 | High Impact: 2", text)
        self.assertIn("- **🏛️ Institutions**: Shanghai AI Lab, Tsinghua University", text)
        self.assertLess(text.index("AHEAD"), text.index("Existing Paper"))

        self.writer.upsert_single_paper_digest_entry({**paper, "title": "AHEAD Duplicate"})
        text_after = Path(path).read_text(encoding="utf-8")
        self.assertEqual(text_after.count("### 🔥 AHEAD"), 1)
        self.assertNotIn("AHEAD Duplicate", text_after)

    def test_detailed_note_prefers_pipeline_published_date_over_metadata_date(self):
        paper = {
            "title": "Date Priority Paper",
            "url": "https://arxiv.org/abs/2606.00001",
            "pdf_url": "https://arxiv.org/pdf/2606.00001",
            "published": datetime(2026, 6, 2, 17, 30),
            "score": 8.0,
            "authors": ["Author One"],
            "metadata": {
                "publication_date": "2026-05-31",
                "institutions": ["Test Lab"],
                "github": "None",
                "project_page": "None",
            },
        }
        path = self.writer.write_detailed_note(paper, "## Abstract\nShort.\n\n## Method\nClear.")
        text = Path(path).read_text(encoding="utf-8")
        match = re.match(r"^---\n([\s\S]*?)\n---\n", text)
        self.assertIsNotNone(match)
        frontmatter = yaml.safe_load(match.group(1))
        self.assertEqual(str(frontmatter["publication_date"]), "2026-06-02")
        self.assertEqual(str(frontmatter["metadata_publication_date"]), "2026-05-31")

    def test_detailed_note_serializes_untrusted_metadata_as_valid_yaml(self):
        paper = {
            "title": 'Quoted: "Paper"',
            "url": "https://arxiv.org/abs/2606.00009",
            "pdf_url": "https://arxiv.org/pdf/2606.00009",
            "score": 8.2,
            "authors": ['Doe, Jane: "JJ"', "Line One\nLine Two"],
            "ai_aliases": ['Alias: "quoted"'],
            "metadata": {"institutions": ['Lab: "A"', "Second\nLab"]},
        }

        path = self.writer.write_detailed_note(paper, "Analysis body.")
        text = Path(path).read_text(encoding="utf-8")
        match = re.match(r"^---\n([\s\S]*?)\n---\n", text)
        self.assertIsNotNone(match)
        frontmatter = yaml.safe_load(match.group(1))

        self.assertEqual(frontmatter["aliases"][1], 'Alias: "quoted"')
        self.assertEqual(frontmatter["authors"][1], "Line One\nLine Two")
        self.assertEqual(frontmatter["institutions"][0], 'Lab: "A"')

    def test_write_daily_digest_backfills_to_five_and_keeps_high_impact_count(self):
        papers = [
            self._paper("Hard Threshold", 7.5),
            self._paper("Backfill A", 6.8),
            self._paper("Backfill B", 6.6),
            self._paper("Backfill C", 6.4),
            self._paper("Backfill D", 6.2),
            self._paper("Left Out", 5.0, rigor=2.0, evidence=2.0),
        ]

        path = self.writer.write_daily_digest(papers, target_date=date(2026, 6, 2))
        text = Path(path).read_text(encoding="utf-8")

        self.assertIn("Total Papers: 5 | High Impact: 1", text)
        self.assertEqual(text.count("(Score:"), 5)
        self.assertIn("Hard Threshold", text)
        self.assertIn("Backfill D", text)
        self.assertNotIn("Left Out", text)

    def test_daily_digest_uses_local_run_history_for_missing_institutions(self):
        run_dir = Path(self.tmp) / "Run_Records" / "2026-05-30-openrouter"
        run_dir.mkdir(parents=True)
        (run_dir / "state.json").write_text(
            (
                '{"papers":[{"title":"History Paper","url":"https://arxiv.org/abs/2606.00002",'
                '"metadata":{"institutions":["History Lab"]}}]}'
            ),
            encoding="utf-8",
        )
        paper = self._paper("History Paper", 7.2)
        paper["url"] = "https://arxiv.org/abs/2606.00002"

        path = self.writer.write_daily_digest([paper], target_date=date(2026, 6, 3))
        text = Path(path).read_text(encoding="utf-8")

        self.assertIn("- **🏛️ Institutions**: History Lab", text)

    def test_write_daily_digest_forces_manual_paper_even_beyond_five(self):
        papers = [
            self._paper("High A", 8.0),
            self._paper("High B", 7.9),
            self._paper("High C", 7.8),
            self._paper("High D", 7.7),
            self._paper("High E", 7.6),
            {**self._paper("Manual Low", 3.2), "forced_deep": True, "manual_requested_at": "2026-06-04T10:00:00"},
        ]

        path = self.writer.write_daily_digest(papers, target_date=date(2026, 6, 4))
        text = Path(path).read_text(encoding="utf-8")

        self.assertIn("Total Papers: 6 | High Impact: 5", text)
        self.assertIn("Manual Low", text)
        self.assertEqual(text.count("(Score:"), 6)

    def test_write_daily_digest_includes_preserved_deep_even_beyond_five(self):
        papers = [
            self._paper("High A", 8.0),
            self._paper("High B", 7.9),
            self._paper("High C", 7.8),
            self._paper("High D", 7.7),
            self._paper("High E", 7.6),
            {**self._paper("Preserved Low", 3.1), "preserved_deep": True, "deep_analysis_completed": True},
        ]

        path = self.writer.write_daily_digest(papers, target_date=date(2026, 6, 5))
        text = Path(path).read_text(encoding="utf-8")

        self.assertIn("Total Papers: 6 | High Impact: 5", text)
        self.assertIn("Preserved Low", text)
        self.assertIn("preserved", text)
        self.assertEqual(text.count("(Score:"), 6)

    def test_write_daily_digest_dedupes_preserved_deep_identity(self):
        fresh = self._paper("Duplicate Fresh", 8.4)
        fresh["url"] = "https://arxiv.org/abs/2606.55555"
        preserved = self._paper("Duplicate Preserved", 3.1)
        preserved.update({
            "url": "https://arxiv.org/abs/2606.55555v2",
            "preserved_deep": True,
            "deep_analysis_completed": True,
        })

        path = self.writer.write_daily_digest([fresh, preserved], target_date=date(2026, 6, 6))
        text = Path(path).read_text(encoding="utf-8")

        self.assertEqual(text.count("(Score:"), 1)
        self.assertIn("Duplicate Fresh", text)
        self.assertNotIn("Duplicate Preserved", text)

    def test_forced_single_deep_supplements_existing_note_without_overwrite(self):
        notes = Path(self.tmp) / "Research_Notes"
        notes.mkdir(exist_ok=True)
        note = notes / "Existing.md"
        note.write_text(
            "---\n"
            "title: Existing\n"
            "arxiv_id: \"2606.02486\"\n"
            "---\n\n"
            "# Existing\n\n"
            "Manual paragraph stays.\n",
            encoding="utf-8",
        )
        paper = {
            "title": "Existing",
            "url": "https://arxiv.org/abs/2606.02486",
            "pdf_url": "https://arxiv.org/pdf/2606.02486",
            "score": 8.1,
            "forced_deep": True,
            "manual_deep_supplement_date": "2026-06-04",
        }

        path = self.writer.write_detailed_note(paper, "## New Analysis\nBetter explanation.")
        text = Path(path).read_text(encoding="utf-8")

        self.assertIn("Manual paragraph stays.", text)
        self.assertIn("## Single Deep Supplement (2026-06-04)", text)
        self.assertIn("Better explanation.", text)

        self.writer.write_detailed_note(paper, "Updated supplement.")
        updated = Path(path).read_text(encoding="utf-8")
        self.assertEqual(updated.count("Single Deep Supplement (2026-06-04)"), 1)
        self.assertIn("Updated supplement.", updated)
        self.assertNotIn("Better explanation.", updated)

    @staticmethod
    def _paper(title, score, novelty=8.0, rigor=8.0, evidence=8.0):
        return {
            "title": title,
            "url": f"https://example.com/{title.replace(' ', '-').lower()}",
            "score": score,
            "innovation": f"{title} innovation.",
            "limitations": f"{title} limitations.",
            "authors": ["Author One"],
            "novelty": novelty,
            "rigor": rigor,
            "evidence": evidence,
            "reproducibility": 7.0,
            "confidence": 8.0,
            "red_flags": [],
        }


if __name__ == "__main__":
    unittest.main()
