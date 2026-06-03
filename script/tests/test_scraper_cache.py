import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from src.scraper import PaperScraper  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    PaperScraper = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


class FakeResponse:
    status_code = 200
    text = "<feed><entry></entry></feed>"
    headers = {}

    def raise_for_status(self):
        return None


@unittest.skipIf(PaperScraper is None, f"scraper dependencies unavailable: {IMPORT_ERROR}")
class ScraperCacheTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.config = {
            "obsidian": {"vault_path": self.tmp},
            "search": {
                "keywords": ["robot"],
                "arxiv_categories": ["cs.RO"],
                "max_results": 5,
                "arxiv_timeout_seconds": 5,
                "arxiv_max_attempts": 1,
                "arxiv_min_interval_seconds": 0,
                "arxiv_cache_enabled": True,
                "arxiv_cache_ttl_hours": 72,
            },
        }

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_request_uses_cache_for_identical_arxiv_params(self):
        scraper = PaperScraper(self.config)
        params = {"search_query": "cat:cs.RO", "start": 0, "max_results": 1}

        with patch("src.scraper.requests.get", return_value=FakeResponse()) as mocked_get:
            first = scraper._request_arxiv_feed(params)
            second = scraper._request_arxiv_feed(params)

        self.assertEqual(first, FakeResponse.text)
        self.assertEqual(second, FakeResponse.text)
        self.assertEqual(mocked_get.call_count, 1)
        self.assertTrue(any(Path(self.tmp).joinpath("Cache", "arxiv").glob("*.xml")))


if __name__ == "__main__":
    unittest.main()
