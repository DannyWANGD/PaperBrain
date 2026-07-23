import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.file_io import atomic_write_text  # noqa: E402
from src.research_indexer import ResearchIndexer  # noqa: E402


class DataIntegrityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_atomic_write_preserves_existing_file_when_replace_fails(self):
        destination = self.tmp / "note.md"
        destination.write_text("original", encoding="utf-8")

        with mock.patch("src.file_io.os.replace", side_effect=OSError("replace failed")):
            with self.assertRaises(OSError):
                atomic_write_text(destination, "new content")

        self.assertEqual(destination.read_text(encoding="utf-8"), "original")
        self.assertEqual(list(self.tmp.glob(".note.md.*.tmp")), [])

    def test_index_build_never_rewrites_malformed_frontmatter(self):
        notes_dir = self.tmp / "Research_Notes"
        notes_dir.mkdir()
        note = notes_dir / "Malformed.md"
        original = "---\naliases: [unterminated\n---\n\n# Keep me\n\nPersonal text.\n"
        note.write_text(original, encoding="utf-8")
        indexer = ResearchIndexer(
            {
                "obsidian": {
                    "vault_path": str(self.tmp),
                    "detailed_notes_folder": "Research_Notes",
                    "research_index_folder": "Research_Index",
                }
            }
        )

        notes = indexer.build(update_notes=True)

        self.assertEqual(notes, [])
        self.assertEqual(note.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
