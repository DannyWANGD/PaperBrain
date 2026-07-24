import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.obsidian_writer import ObsidianWriter  # noqa: E402


class NoteIdentitySafetyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.writer = ObsidianWriter(
            {
                "openrouter": {"threshold_score": 7},
                "obsidian": {
                    "vault_path": str(self.tmp),
                    "daily_digest_folder": "Daily_Papers",
                    "detailed_notes_folder": "Research_Notes",
                    "pdf_storage_folder": "PDFs",
                },
            },
            provider="openrouter",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_regular_write_uses_arxiv_suffix_for_short_title_collision(self):
        first = self._arxiv_paper("First Full Title", "Shared Topic", "2606.00001")
        second = self._arxiv_paper("Second Full Title", "Shared Topic", "2606.00002")

        first_path = Path(self.writer.write_detailed_note(first, "First analysis."))
        first_original = first_path.read_text(encoding="utf-8")
        second_path = Path(self.writer.write_detailed_note(second, "Second analysis."))

        self.assertEqual(first_path.name, "Shared Topic.md")
        self.assertEqual(second_path.name, "Shared Topic - 2606.00002.md")
        self.assertNotEqual(first_path, second_path)
        self.assertEqual(first_path.read_text(encoding="utf-8"), first_original)
        self.assertEqual(self._frontmatter(first_path)["arxiv_id"], "2606.00001")
        self.assertEqual(self._frontmatter(second_path)["arxiv_id"], "2606.00002")
        self.assertIn("Second analysis.", second_path.read_text(encoding="utf-8"))

        repeated_path = Path(self.writer.write_detailed_note(second, "Replacement should be deduplicated."))
        self.assertEqual(repeated_path, second_path)
        self.assertEqual(len(list((self.tmp / "Research_Notes").glob("*.md"))), 2)

        first_repeated = Path(self.writer.write_detailed_note(first, "Must not overwrite the first note."))
        self.assertEqual(first_repeated, first_path)
        self.assertEqual(first_path.read_text(encoding="utf-8"), first_original)

    def test_forced_deep_never_supplements_different_identity_collision(self):
        first = self._arxiv_paper("First Full Title", "Shared Topic", "2606.00011")
        second = {
            **self._arxiv_paper("Second Full Title", "Shared Topic", "2606.00012"),
            "forced_deep": True,
            "manual_deep_supplement_date": "2026-07-22",
        }

        first_path = Path(self.writer.write_detailed_note(first, "First paper analysis."))
        first_original = first_path.read_text(encoding="utf-8")
        second_path = Path(self.writer.write_detailed_note(second, "Second paper analysis."))

        self.assertEqual(second_path.name, "Shared Topic - 2606.00012.md")
        self.assertEqual(first_path.read_text(encoding="utf-8"), first_original)
        self.assertNotIn("Single Deep Supplement", second_path.read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            self.writer._supplement_existing_note(first_path, second, "Wrong target.")
        self.assertEqual(first_path.read_text(encoding="utf-8"), first_original)

        supplemented_path = Path(self.writer.write_detailed_note(second, "Identity-safe supplement."))
        self.assertEqual(supplemented_path, second_path)
        self.assertEqual(first_path.read_text(encoding="utf-8"), first_original)
        supplemented = second_path.read_text(encoding="utf-8")
        self.assertIn("## Single Deep Supplement (2026-07-22)", supplemented)
        self.assertIn("Identity-safe supplement.", supplemented)

    def test_no_arxiv_id_collision_uses_stable_external_identity_hash(self):
        first = {
            "title": "Method: Alpha",
            "short_title": "Shared Topic",
            "url": "https://example.com/alpha",
            "score": 7.5,
        }
        second = {
            "title": "Method Alpha",
            "short_title": "Shared Topic",
            "url": "https://example.com/beta",
            "score": 7.6,
        }

        first_path = Path(self.writer.write_detailed_note(first, "Alpha analysis."))
        first_original = first_path.read_text(encoding="utf-8")
        second_path = Path(self.writer.write_detailed_note(second, "Beta analysis."))

        self.assertEqual(first_path.name, "Shared Topic.md")
        self.assertRegex(second_path.name, r"^Shared Topic - [0-9a-f]{12}\.md$")
        self.assertEqual(first_path.read_text(encoding="utf-8"), first_original)
        self.assertNotEqual(self._frontmatter(first_path)["paper_id"], self._frontmatter(second_path)["paper_id"])

        repeated_path = Path(self.writer.write_detailed_note(second, "Do not create a third note."))
        self.assertEqual(repeated_path, second_path)
        self.assertEqual(len(list((self.tmp / "Research_Notes").glob("*.md"))), 2)

    def test_identical_non_arxiv_titles_with_different_urls_never_collide(self):
        first = {
            "title": "An Identical Paper Title",
            "short_title": "Identical",
            "url": "https://publisher.example/papers/alpha",
            "score": 7.5,
        }
        second = {
            **first,
            "url": "https://publisher.example/papers/beta",
            "score": 7.8,
        }

        first_path = Path(self.writer.write_detailed_note(first, "Alpha analysis."))
        second_path = Path(self.writer.write_detailed_note(second, "Beta analysis."))

        self.assertEqual(first_path.name, "Identical.md")
        self.assertRegex(second_path.name, r"^Identical - [0-9a-f]{12}\.md$")
        self.assertNotEqual(first_path, second_path)
        self.assertIn("Alpha analysis.", first_path.read_text(encoding="utf-8"))
        self.assertIn("Beta analysis.", second_path.read_text(encoding="utf-8"))

    def test_forced_deep_reuses_renamed_note_with_same_canonical_identity(self):
        notes = self.tmp / "Research_Notes"
        existing = notes / "My Curated Reading Note.md"
        existing.write_text(
            "---\n"
            "paper_id: arxiv:2606.00021\n"
            "arxiv_id: '2606.00021'\n"
            "---\n\n"
            "# Curated title\n\n"
            "Keep this paragraph.\n",
            encoding="utf-8",
        )
        paper = {
            **self._arxiv_paper("Current Metadata Title", "Generated Name", "2606.00021"),
            "forced_deep": True,
            "manual_deep_supplement_date": "2026-07-22",
        }

        path = Path(self.writer.write_detailed_note(paper, "New canonical supplement."))

        self.assertTrue(os.path.samefile(path, existing))
        self.assertFalse((notes / "Generated Name.md").exists())
        text = existing.read_text(encoding="utf-8")
        self.assertIn("Keep this paragraph.", text)
        self.assertIn("New canonical supplement.", text)

    def test_visual_fallback_caption_is_written_without_markdown_injection(self):
        pdf_path = self.tmp / "PDFs" / "paper.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(b"%PDF-1.4")
        asset_path = Path(self.writer.assets_folder) / "paper_arch.png"
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        asset_path.write_bytes(b"image")
        paper = self._arxiv_paper("Visual Paper", "Visual Paper", "2606.00031")

        note_path = Path(
            self.writer.write_detailed_note(
                paper,
                "Analysis.",
                local_pdf_path=str(pdf_path),
                image_caption="Paper preview: *first page* (no architecture figure detected).",
            )
        )
        text = note_path.read_text(encoding="utf-8")

        self.assertIn("![[paper_arch.png]]", text)
        self.assertIn(
            "*Paper preview: first page (no architecture figure detected).*",
            text,
        )
        self.assertNotIn("**first page**", text)

    @staticmethod
    def _arxiv_paper(title, short_title, arxiv_id):
        return {
            "title": title,
            "short_title": short_title,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            "score": 8.0,
        }

    @staticmethod
    def _frontmatter(path):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n([\s\S]*?)\n---\n", text)
        if match is None:
            raise AssertionError(f"missing frontmatter: {path}")
        return yaml.safe_load(match.group(1))


if __name__ == "__main__":
    unittest.main()
