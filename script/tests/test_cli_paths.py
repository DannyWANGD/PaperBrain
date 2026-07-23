import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from importlib import resources
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import cli  # noqa: E402
from src.paths import PaperBrainPaths, _relative_base  # noqa: E402


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
        self.assertEqual(payload["backend_version"], "0.3.1")
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

    def test_failed_pipeline_payload_uses_llm_exit_code(self):
        class FailedPipeline(FakePipeline):
            def job(self, **kwargs):
                self.calls.append(kwargs)
                return {
                    "ok": False,
                    "stage": "failed",
                    "errors": [{"code": "llm_coarse_screening_failed", "message": "model unavailable"}],
                }

        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with patch("src.cli.load_config", return_value=self._config(tmp)), contextlib.redirect_stdout(stdout):
                code = cli.main(
                    ["run", "--date", "2026-06-01", "--provider", "openrouter", "--no-podcast"],
                    pipeline_module=FailedPipeline(),
                )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, int(cli.ExitCode.LLM_FAILURE))
        self.assertEqual(payload["exit_code"], int(cli.ExitCode.LLM_FAILURE))

    def test_failed_payload_classifies_pdf_network_and_cancel(self):
        self.assertEqual(
            cli._exit_code_for_failed_payload({"errors": [{"code": "pdf_unavailable"}]}, "run"),
            cli.ExitCode.PDF_UNAVAILABLE,
        )
        self.assertEqual(
            cli._exit_code_for_failed_payload({"error": {"code": "network_unavailable"}}, "run"),
            cli.ExitCode.NETWORK_UNAVAILABLE,
        )
        self.assertEqual(
            cli._exit_code_for_failed_payload({"cancelled": True}, "run"),
            cli.ExitCode.CANCELLED,
        )
        self.assertEqual(
            cli._exit_code_for_failed_payload(
                {"errors": [{"code": "pdf_network_error", "message": "network timeout"}]},
                "run",
            ),
            cli.ExitCode.PDF_UNAVAILABLE,
        )
        self.assertEqual(
            cli._exit_code_for_failed_payload(
                {"errors": [{"code": "single_paper_identity_mismatch", "message": "configuration looks valid"}]},
                "run",
            ),
            cli.ExitCode.NETWORK_UNAVAILABLE,
        )

    def test_exception_payload_preserves_structured_error_code(self):
        class TypedFailure(RuntimeError):
            code = "single_paper_not_found"
            retryable = False

        class FailedPipeline(FakePipeline):
            def job(self, **kwargs):
                raise TypedFailure("requested paper was not found")

        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with patch("src.cli.load_config", return_value=self._config(tmp)), \
                 contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
                code = cli.main(
                    ["run", "--date", "2026-06-01", "--arxiv-url", "2606.02486", "--no-podcast"],
                    pipeline_module=FailedPipeline(),
                )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, int(cli.ExitCode.NETWORK_UNAVAILABLE))
        self.assertEqual(payload["error"]["code"], "single_paper_not_found")
        self.assertFalse(payload["error"]["retryable"])

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

    def test_vault_environment_override_has_priority_over_config(self):
        with tempfile.TemporaryDirectory() as configured, tempfile.TemporaryDirectory() as overridden:
            config = {"obsidian": {"vault_path": configured}}
            with patch.dict(os.environ, {"PAPERBRAIN_VAULT_PATH": overridden}, clear=False):
                paths = PaperBrainPaths.from_config(config)

            self.assertEqual(paths.vault_path, Path(overridden).resolve())

    def test_config_path_environment_override_and_explicit_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / "from-env.yaml"
            explicit_path = Path(tmp) / "explicit.yaml"
            env_path.write_text("search: {}\n", encoding="utf-8")
            explicit_path.write_text("search: {}\n", encoding="utf-8")

            with patch.dict(os.environ, {"PAPERBRAIN_CONFIG_PATH": str(env_path)}, clear=False):
                self.assertEqual(PaperBrainPaths.resolve_config_path(), env_path.resolve())
                self.assertEqual(
                    PaperBrainPaths.resolve_config_path(explicit_path),
                    explicit_path.resolve(),
                )

    def test_default_config_files_are_packaged_resources(self):
        source_config = Path(__file__).resolve().parents[1] / "config"
        with tempfile.TemporaryDirectory() as tmp:
            installed_root = Path(tmp)
            shutil.copytree(source_config, installed_root / "paperbrain_config")
            sys.path.insert(0, str(installed_root))
            sys.modules.pop("paperbrain_config", None)
            try:
                package_root = resources.files("paperbrain_config")
                for filename in ("config.yaml", "prompts.yaml", "tags.yaml", ".env.example"):
                    with self.subTest(filename=filename):
                        self.assertTrue(package_root.joinpath(filename).is_file())
            finally:
                sys.modules.pop("paperbrain_config", None)
                sys.path.remove(str(installed_root))

        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        text = pyproject.read_text(encoding="utf-8")
        self.assertIn('packages = ["src", "tools", "paperbrain_config"]', text)
        self.assertIn('paperbrain_config = "script/config"', text)
        self.assertNotIn('include = ["src*", "tools*", "config*"]', text)
        self.assertEqual(cli.REQUIRED_DEPENDENCIES["PIL"], "Pillow")
        self.assertEqual(cli.REQUIRED_DEPENDENCIES["urllib3"], "urllib3")

    def test_installed_layout_uses_cwd_for_repo_vault_and_cache(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as cwd:
            package_root = Path(tmp) / "Lib"
            script_dir = package_root / "site-packages"
            config_dir = script_dir / "paperbrain_config"
            config_dir.mkdir(parents=True)
            (config_dir / "config.yaml").write_text("obsidian:\n  vault_path: .\n", encoding="utf-8")
            (config_dir / "prompts.yaml").write_text("{}\n", encoding="utf-8")

            with patch("src.paths.Path.cwd", return_value=Path(cwd)):
                runtime_root = _relative_base(package_root, script_dir)
                vault = PaperBrainPaths.resolve_vault_path(
                    {"obsidian": {"vault_path": "."}},
                    repo_root=package_root,
                )
            paths = PaperBrainPaths.from_roots(
                runtime_root,
                script_dir,
                config_dir / "config.yaml",
                config_dir / "prompts.yaml",
                vault,
                {"obsidian": {"vault_path": "."}},
            )

        self.assertEqual(paths.repo_root, Path(cwd).resolve())
        self.assertEqual(paths.vault_path, Path(cwd).resolve())
        self.assertTrue(paths.cache_dir.is_relative_to(Path(cwd).resolve()))
        self.assertFalse(paths.cache_dir.is_relative_to(script_dir.resolve()))

    def test_d2l_compatibility_requirements_pin_only_the_overlay(self):
        root = Path(__file__).resolve().parents[2]
        overlay = (root / "script" / "requirements-d2l.txt").read_text(encoding="utf-8")
        requirements = (root / "script" / "requirements.txt").read_text(encoding="utf-8")
        pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")

        self.assertIn("-r requirements.txt", overlay)
        self.assertIn("requests==2.31.0", overlay)
        self.assertIn("arxiv==2.1.0", overlay)
        self.assertIn("feedparser==6.0.10", overlay)
        self.assertIn("arxiv>=2.1.0", requirements)
        self.assertIn('version = "0.3.1"', pyproject)
        self.assertIn('"urllib3>=1.26.18,<3"', pyproject)

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
