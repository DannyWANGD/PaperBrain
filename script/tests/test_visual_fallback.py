import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analyser import PaperAnalyser  # noqa: E402


class _FakePixmap:
    def __init__(self, page_index):
        self.page_index = page_index

    def tobytes(self, _format):
        return f"page-{self.page_index}".encode("ascii")


class _FakePage:
    def __init__(self, page_index, text, fail_render=False):
        self.page_index = page_index
        self.text = text
        self.fail_render = fail_render

    def get_text(self):
        return self.text

    def get_pixmap(self, matrix=None):
        if self.fail_render:
            raise RuntimeError("render failed")
        return _FakePixmap(self.page_index)


class _FakeDocument:
    def __init__(self, page_texts, failed_pages=()):
        self.pages = [
            _FakePage(index, text, fail_render=index in failed_pages)
            for index, text in enumerate(page_texts)
        ]

    def __len__(self):
        return len(self.pages)

    def __getitem__(self, index):
        return self.pages[index]

    def load_page(self, index):
        return self.pages[index]


class VisualFallbackTest(unittest.TestCase):
    def _analyser(self, payload=None, vision_error=None):
        analyser = PaperAnalyser.__new__(PaperAnalyser)
        analyser.prompts = {"analysis": {"vision_select_user": "select a visual"}}
        analyser.provider = "doubao"
        analyser.model_pro = "fake-vision"
        analyser._openrouter_extra_params = lambda _kind: {}
        if vision_error is not None:
            def raise_error(**_kwargs):
                raise vision_error
            analyser._run_with_model_fallback = raise_error
        else:
            analyser._run_with_model_fallback = lambda **_kwargs: (object(), "fake-vision")
        analyser._message_content_text = lambda _response: json.dumps(payload)
        analyser._sanitize_json = lambda value: value
        return analyser

    def _extract(self, payload, page_texts, failed_pages=(), vision_error=None):
        analyser = self._analyser(payload=payload, vision_error=vision_error)
        document = _FakeDocument(page_texts, failed_pages=failed_pages)
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        with patch("src.analyser.fitz.open", return_value=document):
            saved_path, caption = analyser.extract_images_from_pdf(
                str(Path(temp_dir.name) / "paper.pdf"),
                temp_dir.name,
            )
        content = Path(saved_path).read_bytes() if saved_path else b""
        return content, caption

    def test_architecture_selection_has_an_explicit_architecture_label(self):
        content, caption = self._extract(
            {"index": 0, "caption": "Overall policy pipeline", "fallback_index": 1, "fallback_caption": "Task setup"},
            ["Title", "Figure 1 proposed method architecture", "Figure 2 task overview"],
        )

        self.assertEqual(content, b"page-1")
        self.assertEqual(caption, "Architecture diagram: Overall policy pipeline.")

    def test_representative_visual_is_used_when_architecture_is_absent(self):
        content, caption = self._extract(
            {"index": -1, "caption": "", "fallback_index": 1, "fallback_caption": "Robot task setup"},
            ["Title", "Figure 1 proposed method architecture", "Figure 2 task overview"],
        )

        self.assertEqual(content, b"page-2")
        self.assertEqual(
            caption,
            "Representative figure (no architecture diagram detected): Robot task setup.",
        )

    def test_first_page_is_used_and_labeled_when_no_useful_visual_exists(self):
        content, caption = self._extract(
            {"index": -1, "caption": "", "fallback_index": -1, "fallback_caption": ""},
            ["Paper title page", "Figure 1 proposed method architecture"],
        )

        self.assertEqual(content, b"page-0")
        self.assertEqual(
            caption,
            "Paper preview: first page (no architecture or representative figure detected).",
        )

    def test_cover_is_still_attempted_when_candidate_pages_cannot_render(self):
        content, caption = self._extract(
            {"index": -1, "fallback_index": -1},
            ["Paper title page", "Body", "More body"],
            failed_pages=(1, 2),
        )

        self.assertEqual(content, b"page-0")
        self.assertTrue(caption.startswith("Paper preview:"))

    def test_vision_failure_uses_a_labeled_ranked_candidate(self):
        content, caption = self._extract(
            None,
            ["Title", "Figure 1 proposed method architecture"],
            vision_error=RuntimeError("vision unavailable"),
        )

        self.assertEqual(content, b"page-1")
        self.assertEqual(
            caption,
            "Representative page: automatic fallback because visual selection was unavailable.",
        )


if __name__ == "__main__":
    unittest.main()
