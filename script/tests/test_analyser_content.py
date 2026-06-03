import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


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


if __name__ == "__main__":
    unittest.main()
