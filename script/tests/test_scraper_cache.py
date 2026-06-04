import shutil
import sys
import tempfile
import types
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import feedparser  # noqa: F401
except ModuleNotFoundError:
    sys.modules["feedparser"] = types.SimpleNamespace(parse=lambda raw: types.SimpleNamespace(entries=[]))

try:
    from src.scraper import PaperScraper  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - environment guard
    PaperScraper = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


DEFAULT_FEED = "<feed><entry></entry></feed>"


class FakeResponse:
    def __init__(self, status_code=200, text=DEFAULT_FEED, headers=None, json_data=None):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}
        self._json_data = json_data

    def raise_for_status(self):
        return None

    def json(self):
        return self._json_data


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
                "arxiv_api_endpoints": ["https://export.arxiv.org/api/query"],
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

        self.assertEqual(first, DEFAULT_FEED)
        self.assertEqual(second, DEFAULT_FEED)
        self.assertEqual(mocked_get.call_count, 1)
        self.assertTrue(any(Path(self.tmp).joinpath("Cache", "arxiv").glob("*.xml")))

    def test_request_falls_back_to_second_arxiv_endpoint(self):
        self.config["search"]["arxiv_cache_enabled"] = False
        self.config["search"]["arxiv_max_attempts"] = 1
        self.config["search"]["arxiv_api_endpoints"] = [
            "https://first.example/api/query",
            "https://second.example/api/query",
        ]
        scraper = PaperScraper(self.config)
        params = {"search_query": "cat:cs.RO", "start": 0, "max_results": 1}

        with patch("src.scraper.requests.get", side_effect=[
            FakeResponse(status_code=429, text="rate limited"),
            FakeResponse(status_code=200, text="<feed><entry><id>x</id></entry></feed>"),
        ]) as mocked_get:
            raw = scraper._request_arxiv_feed(params)

        self.assertIn("<feed>", raw)
        self.assertEqual(mocked_get.call_count, 2)
        self.assertEqual(mocked_get.call_args_list[0].args[0], "https://first.example/api/query")
        self.assertEqual(mocked_get.call_args_list[1].args[0], "https://second.example/api/query")

    def test_request_falls_back_to_expired_arxiv_cache_after_live_failure(self):
        self.config["search"]["arxiv_cache_ttl_hours"] = -1
        self.config["search"]["arxiv_max_attempts"] = 1
        scraper = PaperScraper(self.config)
        params = {"search_query": "cat:cs.RO", "start": 0, "max_results": 1}
        scraper._write_cached_feed(params, DEFAULT_FEED)

        with patch("src.scraper.requests.get", return_value=FakeResponse(status_code=503, text="down")):
            raw = scraper._request_arxiv_feed(params)

        self.assertEqual(raw, DEFAULT_FEED)

    def test_hf_daily_papers_falls_back_to_second_endpoint(self):
        self.config["search"]["hf_cache_enabled"] = False
        self.config["search"]["hf_max_attempts"] = 1
        self.config["search"]["hf_min_interval_seconds"] = 0
        self.config["search"]["hf_daily_papers_endpoints"] = [
            "https://first.example/api/daily_papers",
            "https://second.example/api/daily_papers",
        ]
        scraper = PaperScraper(self.config)
        payload = [{
            "paper": {
                "id": "2605.25802",
                "title": "Robot Manipulation Foundation Model",
                "summary": "A robot manipulation paper.",
                "authors": [{"name": "Ada"}],
            }
        }]

        with patch("src.scraper.requests.get", side_effect=[
            FakeResponse(status_code=503, text="down"),
            FakeResponse(status_code=200, json_data=payload),
        ]) as mocked_get:
            papers = scraper.fetch_hf_daily_papers(date(2026, 6, 3))

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["paper_id"], "arxiv:2605.25802")
        self.assertEqual(mocked_get.call_count, 2)
        self.assertEqual(mocked_get.call_args_list[0].args[0], "https://first.example/api/daily_papers")
        self.assertEqual(mocked_get.call_args_list[1].args[0], "https://second.example/api/daily_papers")

    def test_hf_daily_papers_uses_cache_for_identical_date(self):
        self.config["search"]["hf_min_interval_seconds"] = 0
        scraper = PaperScraper(self.config)
        payload = [{
            "paper": {
                "id": "2605.25802",
                "title": "Robot Manipulation Foundation Model",
                "summary": "A robot manipulation paper.",
                "authors": [{"name": "Ada"}],
            }
        }]

        with patch("src.scraper.requests.get", return_value=FakeResponse(status_code=200, json_data=payload)) as mocked_get:
            first = scraper.fetch_hf_daily_papers(date(2026, 6, 3))
            second = scraper.fetch_hf_daily_papers(date(2026, 6, 3))

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(mocked_get.call_count, 1)
        self.assertTrue(any(Path(self.tmp).joinpath("Cache", "huggingface").glob("*.json")))

    def test_single_arxiv_fetch_falls_back_to_abs_page(self):
        self.config["search"]["arxiv_cache_enabled"] = False
        self.config["search"]["arxiv_max_attempts"] = 1
        scraper = PaperScraper(self.config)
        html = """
        <html>
          <h1 class="title">Title: Fallback Robot Paper</h1>
          <div class="authors"><a>Ada</a><a>Lin</a></div>
          <blockquote class="abstract">Abstract: Robot manipulation abstract.</blockquote>
        </html>
        """

        with patch.object(scraper, "_request_arxiv_feed", side_effect=RuntimeError("api down")), \
             patch("src.scraper.requests.get", return_value=FakeResponse(status_code=200, text=html)):
            paper = scraper.fetch_single_arxiv_paper("2605.25802")

        self.assertEqual(paper["title"], "Fallback Robot Paper")
        self.assertEqual(paper["pdf_url"], "https://arxiv.org/pdf/2605.25802.pdf")
        self.assertEqual(paper["authors"], ["Ada", "Lin"])

    def test_single_arxiv_fetch_tries_search_query_when_id_list_is_empty(self):
        self.config["search"]["arxiv_cache_enabled"] = False
        scraper = PaperScraper(self.config)
        entry = {
            "id": "https://arxiv.org/abs/2605.25802",
            "title": "Robot Foundation Model",
            "summary": "A robot manipulation paper.",
            "authors": [{"name": "Ada"}],
            "links": [],
        }

        with patch.object(scraper, "_request_arxiv_feed", side_effect=["empty", "hit"]) as request_feed, \
             patch("src.scraper.feedparser.parse", side_effect=[
                 types.SimpleNamespace(entries=[]),
                 types.SimpleNamespace(entries=[entry]),
             ]):
            paper = scraper.fetch_single_arxiv_paper("2605.25802")

        self.assertEqual(paper["title"], "Robot Foundation Model")
        self.assertEqual(paper["pdf_url"], "https://arxiv.org/pdf/2605.25802.pdf")
        self.assertEqual(request_feed.call_count, 2)
        self.assertEqual(request_feed.call_args_list[0].args[0]["id_list"], "2605.25802")
        self.assertEqual(request_feed.call_args_list[1].args[0]["search_query"], "id:2605.25802")


if __name__ == "__main__":
    unittest.main()
