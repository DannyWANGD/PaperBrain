import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.search_matching import keyword_matches, matched_keywords, paper_matches_keywords  # noqa: E402


class SearchMatchingTest(unittest.TestCase):
    def test_matching_is_case_and_separator_insensitive(self):
        text = "A Vision-Language_Action policy for ROBOT manipulation"
        self.assertTrue(keyword_matches(text, "vision language action"))
        self.assertTrue(keyword_matches(text, "robot manipulation"))

    def test_unicode_normalization_and_dash_variants_match(self):
        self.assertTrue(keyword_matches("Ｖｉｓｉｏｎ—Language–Action", "vision language action"))
        self.assertTrue(keyword_matches("World−Model control", "world-model"))

    def test_short_keyword_requires_word_boundaries(self):
        self.assertTrue(keyword_matches("A VLA policy", "VLA"))
        self.assertFalse(keyword_matches("A svlam optimizer", "VLA"))

    def test_punctuation_keyword_remains_searchable(self):
        self.assertTrue(keyword_matches("Static analysis for C++ programs", "C++"))

    def test_duplicate_keywords_are_reported_once(self):
        matches = matched_keywords("World-model learning", "", ["World Model", "world-model", ""])
        self.assertEqual(matches, ["World Model"])

    def test_title_and_abstract_are_both_checked(self):
        self.assertTrue(paper_matches_keywords("Unrelated title", "Diffusion model for control", ["diffusion model"]))


if __name__ == "__main__":
    unittest.main()
