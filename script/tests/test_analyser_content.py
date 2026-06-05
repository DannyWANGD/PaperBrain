import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from src.analyser import PaperAnalyser  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    PaperAnalyser = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


@unittest.skipIf(PaperAnalyser is None, f"analyser dependencies unavailable: {IMPORT_ERROR}")
class AnalyserContentNormalizationTest(unittest.TestCase):
    def test_openrouter_structured_content_is_flattened_to_text(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=[
                            {"type": "text", "text": "## Abstract\nA"},
                            {"type": "text", "text": "## Method\nB"},
                        ]
                    )
                )
            ]
        )

        self.assertEqual(analyser._message_content_text(response), "## Abstract\nA\n## Method\nB")

    def test_learning_resource_models_filter_disallowed_families(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.provider = "openrouter"
        analyser.config = {
            "openrouter": {
                "model_learning_resources_fallbacks": [
                    "anthropic/claude-sonnet-5",
                    "openai/gpt-5",
                    "google/gemini-3-pro",
                    "qwen/qwen3.7-max",
                ],
            }
        }
        analyser._openrouter_banned_authors = set()

        models = analyser._openrouter_model_candidates("openai/gpt-5", "model_learning_resources")

        lowered = " ".join(models).lower()
        self.assertNotIn("claude", lowered)
        self.assertNotIn("openai", lowered)
        self.assertNotIn("gpt", lowered)
        self.assertNotIn("gemini", lowered)
        self.assertIn("qwen/qwen3.7-max", models)
        self.assertIn("deepseek/deepseek-v4-pro", models)

    def test_learning_resource_link_validation_removes_unreachable_links(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.config = {
            "analysis": {
                "learning_resources_validate_links": True,
                "learning_resources_link_timeout_seconds": 1,
                "learning_resources_max_links_to_validate": 10,
            }
        }
        text = (
            "Read [good tutorial](https://example.com/good) and "
            "[bad tutorial](https://example.com/missing)."
        )

        def fake_request(method, url, **kwargs):
            status = 200 if url.endswith("/good") else 404
            return SimpleNamespace(status_code=status, close=lambda: None)

        with patch("src.analyser.requests.request", side_effect=fake_request):
            cleaned, info = analyser._validate_learning_resource_links(text)

        self.assertIn("[good tutorial](https://example.com/good)", cleaned)
        self.assertNotIn("https://example.com/missing", cleaned)
        self.assertIn("bad tutorial (link removed: validation failed)", cleaned)
        self.assertEqual(info["checked"], 2)
        self.assertEqual(info["valid"], 1)
        self.assertEqual(len(info["invalid"]), 1)


if __name__ == "__main__":
    unittest.main()
