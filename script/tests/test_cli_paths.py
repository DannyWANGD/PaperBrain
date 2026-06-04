import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import cli  # noqa: E402
from src.paths import PaperBrainPaths  # noqa: E402


class FakePipeline:
    def __init__(self):
        self.calls = []

    def job(self, **kwargs):
        self.calls.append(kwargs)
        return {
            "ok": True,
            "stage": "fetched",
            "state_path": "fake-state.json",
            "run_dir": "fake-run",
        }


class CliAndPathsTest(unittest.TestCase):
    def test_fetch_command_maps_to_pipeline_stop_after_fetch_and_json_stdout(self):
        fake = FakePipeline()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            code = cli.main(
                [
                    "fetch",
                    "--date",
                    "2026-06-01",
                    "--provider",
                    "openrouter",
                    "--no-podcast",
                    "--no-resume",
                ],
                pipeline_module=fake,
            )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "fetch")
        self.assertEqual(payload["stop_after"], "fetch")
        self.assertFalse(fake.calls[0]["generate_podcast"])
        self.assertFalse(fake.calls[0]["resume"])
        self.assertEqual(fake.calls[0]["provider"], "openrouter")

    def test_legacy_main_args_translate_old_run_now_shape(self):
        translated = cli.legacy_main_args(["--run-now", "--provider", "openrouter", "--no-resume"])

        self.assertEqual(translated, ["run", "--provider", "openrouter", "--no-resume"])

    def test_paths_resolve_repo_relative_vault_and_run_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = {
                "obsidian": {
                    "vault_path": tmp,
                    "daily_digest_folder": "Daily_Papers",
                    "detailed_notes_folder": "Research_Notes",
                    "research_index_folder": "Research_Index",
                    "research_brief_folder": "Research_Briefs",
                    "pdf_storage_folder": "PDFs",
                }
            }

            paths = PaperBrainPaths.from_config(config)

        self.assertEqual(paths.vault_path, Path(tmp).resolve())
        self.assertEqual(paths.state_path("2026-06-01", "openrouter").name, "state.json")
        self.assertEqual(paths.screening_report_path("2026-06-01", "openrouter").name, "screening_report.md")


if __name__ == "__main__":
    unittest.main()
