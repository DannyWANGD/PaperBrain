import sys
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from src.analyser import DeepAnalysisError, PaperAnalyser  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    PaperAnalyser = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


@unittest.skipIf(PaperAnalyser is None, f"analyser dependencies unavailable: {IMPORT_ERROR}")
class AnalyserContentNormalizationTest(unittest.TestCase):
    @staticmethod
    def _screening_analyser(response_text):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.provider = "doubao"
        analyser.config = {"search": {"keywords": ["robot"]}, "analysis": {}}
        analyser.prompts = {}
        analyser.tags_taxonomy = []
        analyser.model_flash = "flash"
        analyser.model_screening_pro = "pro"
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=response_text))]
        )
        analyser._chat_with_fallback = lambda **kwargs: (response, kwargs["models"][0])
        return analyser

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

    def test_all_openrouter_model_routes_filter_disallowed_families(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.provider = "openrouter"
        analyser.config = {
            "openrouter": {
                f"{kind}_fallbacks": [
                    "anthropic/claude-sonnet-5",
                    "openai/gpt-5",
                    "~google/gemini-3-pro",
                    "qwen/qwen3.7-max",
                ]
                for kind in (
                    "model_flash",
                    "model_screening_pro",
                    "model_pro",
                    "model_learning_resources",
                    "model_vision",
                )
            }
        }
        analyser._openrouter_banned_authors = set()

        for kind in analyser.config["openrouter"]:
            route = kind.removesuffix("_fallbacks")
            with self.subTest(route=route):
                models = analyser._openrouter_model_candidates("openai/gpt-5", route)
                lowered = " ".join(models).lower()
                self.assertNotIn("claude", lowered)
                self.assertNotIn("openai", lowered)
                self.assertNotIn("gpt", lowered)
                self.assertNotIn("gemini", lowered)
                self.assertIn("qwen/qwen3.7-max", models)

    def test_learning_resource_params_add_scoped_openrouter_web_search(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.provider = "openrouter"
        analyser.config = {
            "analysis": {
                "learning_resources_web_search_enabled": True,
            }
        }
        base = {
            "extra_headers": {"X-Title": "PaperBrain"},
            "extra_body": {"provider": {"sort": "throughput"}},
        }

        params = analyser._learning_resource_extra_params(base)

        self.assertNotIn("tools", base["extra_body"])
        self.assertEqual(params["extra_body"]["provider"], {"sort": "throughput"})
        self.assertEqual(params["extra_body"]["max_tool_calls"], 3)
        self.assertEqual(params["max_tokens"], 12000)
        tool = params["extra_body"]["tools"][0]
        self.assertEqual(tool["type"], "openrouter:web_search")
        self.assertEqual(tool["parameters"]["max_results"], 6)
        self.assertEqual(tool["parameters"]["max_total_results"], 18)
        self.assertEqual(tool["parameters"]["search_context_size"], "medium")
        self.assertNotIn("engine", tool["parameters"])

    def test_learning_resource_web_search_is_opt_in_outside_shipped_config(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.provider = "openrouter"
        analyser.config = {"analysis": {}}
        base = {"extra_body": {"provider": {"sort": "throughput"}}}

        self.assertEqual(analyser._learning_resource_extra_params(base), base)

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
            return SimpleNamespace(status_code=status, headers={}, close=lambda: None)

        with patch("src.analyser.request_public_url", side_effect=fake_request):
            cleaned, info = analyser._validate_learning_resource_links(text)

        self.assertIn("[good tutorial](https://example.com/good)", cleaned)
        self.assertNotIn("https://example.com/missing", cleaned)
        self.assertIn("bad tutorial (link removed: validation failed)", cleaned)
        self.assertEqual(info["checked"], 2)
        self.assertEqual(info["valid"], 1)
        self.assertEqual(len(info["invalid"]), 1)

    def test_private_resource_url_is_rejected_before_request(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        with patch("src.network_safety.requests.request") as request:
            self.assertEqual(analyser._url_is_reachable("http://127.0.0.1/admin"), (False, "unsafe_url"))
        request.assert_not_called()

    def test_screening_fallback_is_structured_as_retryable_error(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        result = analyser._screening_fallback_payload(
            {"title": "Paper"},
            RuntimeError("provider unavailable"),
            stage="coarse",
        )

        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["screening_error"]["code"], "llm_coarse_screening_failed")
        self.assertEqual(result["screening_error"]["exception"], "RuntimeError")
        self.assertTrue(result["screening_error"]["retryable"])

    def test_coarse_screening_rejects_empty_missing_and_nonfinite_json(self):
        valid = {
            "coarse_score": 8.0,
            "relevance": 8.0,
            "evidence": 7.0,
            "method_completeness": 7.0,
            "should_rescreen": True,
            "reason": "Relevant and sufficiently supported.",
        }
        invalid_payloads = [
            {},
            {key: value for key, value in valid.items() if key != "evidence"},
            {**valid, "coarse_score": float("nan")},
            {**valid, "relevance": float("inf")},
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                analyser = self._screening_analyser(json.dumps(payload))
                result = analyser.coarse_screen_paper({"title": "Paper", "abstract": "Robot method."})
                self.assertEqual(result["screening_error"]["code"], "llm_coarse_screening_failed")

    def test_detailed_screening_rejects_missing_and_nonfinite_required_fields(self):
        valid = {
            "score": 8.0,
            "relevance": 8.0,
            "novelty": 8.0,
            "rigor": 8.0,
            "evidence": 8.0,
            "reproducibility": 8.0,
            "confidence": 8.0,
            "red_flags": [],
            "innovation": "Introduces a concrete method.",
            "limitations": "Evaluation is limited in scope.",
            "reason": "The evidence supports detailed review.",
            "tags": ["Robot_Learning"],
            "short_title": "Paper",
        }
        invalid_payloads = [
            {},
            {key: value for key, value in valid.items() if key != "limitations"},
            {**valid, "score": float("nan")},
            {**valid, "confidence": float("inf")},
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                analyser = self._screening_analyser(json.dumps(payload))
                result = analyser.screen_paper({"title": "Paper", "abstract": "Robot method."})
                self.assertEqual(result["screening_error"]["code"], "llm_detailed_screening_failed")

    def test_deep_analysis_raises_when_all_round_one_models_fail(self):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.provider = "doubao"
        analyser.config = {"analysis": {"max_iterations": 1}}
        analyser.prompts = {}
        analyser.model_pro = "fake-model"

        with patch.object(analyser, "_extract_text_from_pdf_fitz", return_value="paper text " * 30), \
             patch.object(analyser, "_extract_figures_from_pdf", return_value=[]), \
             patch.object(analyser, "_run_with_model_fallback", return_value=(None, None)):
            with self.assertRaises(DeepAnalysisError):
                analyser.analyze_full_paper_iterative(
                    {"title": "Paper"},
                    "paper.pdf",
                    [],
                )


if __name__ == "__main__":
    unittest.main()
