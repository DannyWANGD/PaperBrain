import shutil
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.obsidian_writer import ObsidianWriter  # noqa: E402


class DailyDigestUpsertTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.config = {
            "openrouter": {"threshold_score": 7},
            "analysis": {"daily_digest_min_score": 7.0},
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
        self.assertIn("- **Institutions**: Shanghai AI Lab, Tsinghua University", text)
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
        self.assertIn('publication_date: "2026-06-02"', text)
        self.assertIn('metadata_publication_date: "2026-05-31"', text)


if __name__ == "__main__":
    unittest.main()
