import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import run_control  # noqa: E402


class RunControlTest(unittest.TestCase):
    def test_pipeline_lock_blocks_second_active_owner_and_releases(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self._config(tmp)
            first = run_control.PipelineLock(config, command="run", provider="openrouter").acquire()
            try:
                with self.assertRaises(run_control.RunAlreadyActive):
                    run_control.PipelineLock(config, command="digest", provider="openrouter").acquire()
                self.assertTrue(run_control.lock_path(config).exists())
            finally:
                first.release()

            self.assertFalse(run_control.lock_path(config).exists())

    def test_cancel_request_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self._config(tmp)
            path, payload = run_control.request_cancel(config, reason="test")

            self.assertTrue(path.exists())
            self.assertEqual(payload["reason"], "test")
            with self.assertRaises(run_control.RunCancelled):
                run_control.raise_if_cancelled(config)

            run_control.clear_cancel_request(config)
            run_control.raise_if_cancelled(config)

    @staticmethod
    def _config(tmp):
        return {
            "obsidian": {
                "vault_path": tmp,
                "daily_digest_folder": "Daily_Papers",
                "detailed_notes_folder": "Research_Notes",
                "research_index_folder": "Research_Index",
                "research_brief_folder": "Research_Briefs",
                "pdf_storage_folder": "PDFs",
            }
        }


if __name__ == "__main__":
    unittest.main()
