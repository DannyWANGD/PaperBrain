import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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

    def write_digest_from_state(self, **kwargs):
        self.calls.append({"digest": kwargs})
        return {
            "ok": True,
            "stage": "completed",
            "artifacts": {"daily_digest": "fake-digest.md"},
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

    def test_run_force_command_passes_force_to_pipeline(self):
        fake = FakePipeline()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            code = cli.main(
                [
                    "run",
                    "--date",
                    "2026-06-01",
                    "--provider",
                    "openrouter",
                    "--no-podcast",
                    "--force",
                ],
                pipeline_module=fake,
            )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertTrue(fake.calls[0]["force"])

    def test_legacy_main_args_translate_old_run_now_shape(self):
        translated = cli.legacy_main_args(["--run-now", "--provider", "openrouter", "--no-resume"])

        self.assertEqual(translated, ["run", "--provider", "openrouter", "--no-resume"])

    def test_digest_command_calls_digest_only_pipeline_entry(self):
        fake = FakePipeline()
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with patch("src.cli.load_config", return_value=self._config(tmp)), contextlib.redirect_stdout(stdout):
                code = cli.main(
                    ["digest", "--date", "2026-05-22", "--provider", "openrouter"],
                    pipeline_module=fake,
                )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "digest")
        self.assertEqual(fake.calls[0]["digest"]["provider"], "openrouter")

    def test_cancel_and_dry_run_use_control_files_without_running_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self._config(tmp)
            stdout = io.StringIO()

            with patch("src.cli.load_config", return_value=config), contextlib.redirect_stdout(stdout):
                cancel_code = cli.main(["cancel", "--reason", "test"])

            cancel_payload = json.loads(stdout.getvalue())
            self.assertEqual(cancel_code, 0)
            self.assertTrue(cancel_payload["cancel_requested"])
            self.assertTrue(Path(cancel_payload["artifacts"]["cancel_request"]).exists())

            stdout = io.StringIO()
            with patch("src.cli.load_config", return_value=config), contextlib.redirect_stdout(stdout):
                dry_code = cli.main(["dry-run", "--mode", "digest", "--date", "2026-05-22", "--provider", "openrouter"])

            dry_payload = json.loads(stdout.getvalue())
            self.assertEqual(dry_code, 0)
            self.assertTrue(dry_payload["ok"])
            self.assertFalse(dry_payload["network_or_llm_invoked"])
            self.assertIn("digest", dry_payload["would_run"])

    def test_dry_run_pipeline_preview_includes_force_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with patch("src.cli.load_config", return_value=self._config(tmp)), contextlib.redirect_stdout(stdout):
                code = cli.main(
                    [
                        "dry-run",
                        "--mode",
                        "screen",
                        "--date",
                        "2026-06-01",
                        "--provider",
                        "openrouter",
                        "--no-podcast",
                        "--force",
                    ]
                )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertIn("--force", payload["would_run"])
        self.assertIn("--no-podcast", payload["would_run"])

    def test_bridge_request_file_dispatches_to_digest(self):
        fake = FakePipeline()
        with tempfile.TemporaryDirectory() as tmp:
            request = Path(tmp) / "request.json"
            request.write_text(
                json.dumps({"command": "digest", "date": "2026-05-22", "provider": "openrouter"}),
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with patch("src.cli.load_config", return_value=self._config(tmp)), contextlib.redirect_stdout(stdout):
                code = cli.main(["bridge", "--request-file", str(request)], pipeline_module=fake)

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "digest")
        self.assertTrue(payload["bridge_request"].endswith("request.json"))

    def test_brief_command_generates_artifact_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with patch("src.cli.load_config", return_value=self._config(tmp)), contextlib.redirect_stdout(stdout):
                code = cli.main(["brief", "--week", "2026-W23"])

            payload = json.loads(stdout.getvalue())
            self.assertEqual(code, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "brief")
            self.assertEqual(payload["brief_type"], "week")
            self.assertEqual(payload["period_label"], "2026-W23")
            self.assertTrue(Path(payload["artifacts"]["research_brief"]).exists())

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
        self.assertEqual(paths.run_id("2026-06-01", "openrouter"), "2026-06-01")
        self.assertEqual(paths.run_dir("2026-06-01", "openrouter").name, "2026-06-01")
        self.assertEqual(paths.state_path("2026-06-01", "openrouter").name, "state.json")
        self.assertEqual(paths.screening_report_path("2026-06-01", "openrouter").name, "screening_report.md")

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
