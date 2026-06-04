import contextlib
import io
import json
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import cli  # noqa: E402


class CliDoctorTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
