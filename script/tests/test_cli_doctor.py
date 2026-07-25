import contextlib
import copy
import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import cli  # noqa: E402


class CliDoctorTest(unittest.TestCase):
    def _config_checks(self, updates):
        config = copy.deepcopy(cli.load_config())
        config["search"].update(updates)
        paths = cli.PaperBrainPaths.from_config_dict(config)
        section = cli._doctor_config(config, cli.load_prompts(), paths)
        return {check["name"]: check for check in section["checks"]}

    def test_doctor_config_outputs_structured_json(self):
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            code = cli.main(["doctor", "config"])

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["scope"], "config")
        self.assertEqual(payload["sections"][0]["name"], "config")
        self.assertTrue(Path(payload["artifacts"]["diagnostics"]).exists())

    def test_doctor_arxiv_offline_skips_live_probe(self):
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            code = cli.main(["doctor", "arxiv"])

        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["scope"], "arxiv")
        names = {check["name"] for check in payload["checks"]}
        self.assertIn("arxiv_live_probe", names)

    def test_parser_accepts_doctor_llm_provider_and_check_lint_flags(self):
        parser = cli.build_parser()

        doctor_args = parser.parse_args(["doctor", "llm", "--provider", "openrouter"])
        check_args = parser.parse_args(["check", "--skip-tests", "--skip-lint"])

        self.assertEqual(doctor_args.doctor_command, "llm")
        self.assertEqual(doctor_args.provider, "openrouter")
        self.assertTrue(check_args.skip_tests)
        self.assertTrue(check_args.skip_lint)

    def test_parser_accepts_live_network_doctor(self):
        args = cli.build_parser().parse_args(["doctor", "network", "--live"])

        self.assertEqual(args.doctor_command, "network")
        self.assertTrue(args.live)

    def test_network_doctor_reports_presence_without_proxy_values(self):
        secret_proxy = "http://proxy-user:proxy-password@example.test:8080"
        with patch.dict(os.environ, {"HTTPS_PROXY": secret_proxy}, clear=True):
            section = cli._doctor_network({}, live=False)

        serialized = json.dumps(section)
        self.assertTrue(section["ok"])
        self.assertTrue(section["checks"][0]["data"]["HTTPS_PROXY"])
        self.assertNotIn(secret_proxy, serialized)
        self.assertNotIn("proxy-password", serialized)

    def test_live_network_doctor_runs_both_no_cost_probes(self):
        success_hf = cli._check("huggingface_live_probe", True, "error", "ok", category="network")
        success_arxiv = cli._check("network_arxiv_live_probe", True, "error", "ok", category="network")
        with patch("src.cli._live_huggingface_check", return_value=success_hf) as hf, \
             patch("src.cli._live_network_arxiv_check", return_value=success_arxiv) as arxiv:
            section = cli._doctor_network({}, live=True)

        self.assertTrue(section["ok"])
        hf.assert_called_once_with()
        arxiv.assert_called_once_with({})

    def test_discovery_config_requires_nonempty_keywords(self):
        checks = self._config_checks({"keywords": []})

        self.assertFalse(checks["search_keywords"]["ok"])

    def test_selected_category_mode_requires_official_category(self):
        empty = self._config_checks({"arxiv_category_mode": "selected", "arxiv_categories": []})
        invalid = self._config_checks({"arxiv_category_mode": "selected", "arxiv_categories": ["cs.NOT-REAL"]})

        self.assertFalse(empty["search_categories"]["ok"])
        self.assertFalse(invalid["search_categories"]["ok"])
        self.assertEqual(invalid["search_categories"]["data"]["invalid_categories"], ["cs.NOT-REAL"])

    def test_all_category_mode_allows_empty_category_list(self):
        checks = self._config_checks({"arxiv_category_mode": "all", "arxiv_categories": []})

        self.assertTrue(checks["search_categories"]["ok"])

    def test_page_size_must_be_an_integer_in_supported_range(self):
        too_large = self._config_checks({"arxiv_page_size": 2001})
        fractional = self._config_checks({"arxiv_page_size": 20.5})

        self.assertFalse(too_large["search_arxiv_page_size"]["ok"])
        self.assertFalse(fractional["search_arxiv_page_size"]["ok"])


if __name__ == "__main__":
    unittest.main()
