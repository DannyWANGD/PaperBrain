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
    from src.scraper import NetworkUnavailableError, PaperScraper, PaperSourceError, SinglePaperFetchError  # noqa: E402
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

    @staticmethod
    def _entry(arxiv_id, title="Robot paper", summary="Robot manipulation study"):
        return {
            "id": f"https://arxiv.org/abs/{arxiv_id}",
            "title": title,
            "summary": summary,
            "authors": [{"name": "Ada"}],
            "links": [],
            "published_parsed": (2026, 6, 1, 12, 0, 0, 0, 0, 0),
        }

    def test_arxiv_fetch_pages_through_every_daily_candidate(self):
        self.config["search"].update({"arxiv_page_size": 2, "max_results": 1})
        scraper = PaperScraper(self.config)
        pages = [
            types.SimpleNamespace(
                entries=[self._entry("2606.00001"), self._entry("2606.00002", title="Unrelated", summary="Other")],
                feed={"opensearch_totalresults": "3"},
            ),
            types.SimpleNamespace(
                entries=[self._entry("2606.00003")],
                feed={"opensearch_totalresults": "3"},
            ),
        ]

        with patch.object(scraper, "_request_arxiv_feed", side_effect=["page-1", "page-2"]) as request_feed, \
             patch("src.scraper.feedparser.parse", side_effect=pages):
            papers = scraper.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertEqual([paper["paper_id"] for paper in papers], ["arxiv:2606.00001", "arxiv:2606.00003"])
        self.assertEqual([call.args[0]["start"] for call in request_feed.call_args_list], [0, 2])
        self.assertTrue(scraper.last_arxiv_scan["complete"])
        self.assertEqual(scraper.last_arxiv_scan["candidates_fetched"], 3)
        self.assertEqual(scraper.last_arxiv_scan["keyword_matches"], 2)

    def test_arxiv_fetches_more_than_fifty_candidates_across_pages(self):
        self.config["search"]["arxiv_page_size"] = 20
        scraper = PaperScraper(self.config)
        entries = [self._entry(f"2606.{index:05d}") for index in range(1, 56)]
        pages = [
            types.SimpleNamespace(entries=entries[0:20], feed={"opensearch_totalresults": "55"}),
            types.SimpleNamespace(entries=entries[20:40], feed={"opensearch_totalresults": "55"}),
            types.SimpleNamespace(entries=entries[40:55], feed={"opensearch_totalresults": "55"}),
        ]

        with patch.object(scraper, "_request_arxiv_feed", side_effect=["page-1", "page-2", "page-3"]) as request_feed, \
             patch("src.scraper.feedparser.parse", side_effect=pages):
            papers = scraper.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertEqual(len(papers), 55)
        self.assertEqual([call.args[0]["start"] for call in request_feed.call_args_list], [0, 20, 40])
        self.assertNotIn("robot", request_feed.call_args_list[0].args[0]["search_query"].lower())

    def test_known_total_still_stops_on_short_final_page(self):
        self.config["search"]["arxiv_page_size"] = 2
        scraper = PaperScraper(self.config)
        parsed = types.SimpleNamespace(
            entries=[self._entry("2606.00001")],
            feed={"opensearch_totalresults": "99"},
        )
        with patch.object(scraper, "_request_arxiv_feed", return_value="page") as request_feed, \
             patch("src.scraper.feedparser.parse", return_value=parsed):
            papers = scraper.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertEqual(len(papers), 1)
        request_feed.assert_called_once()

    def test_cross_category_duplicate_arxiv_ids_are_deduplicated(self):
        self.config["search"].update({"arxiv_page_size": 2, "arxiv_categories": ["cs.RO", "cs.AI"]})
        scraper = PaperScraper(self.config)
        pages = [
            types.SimpleNamespace(
                entries=[self._entry("2606.00001"), self._entry("2606.00002")],
                feed={"opensearch_totalresults": "3"},
            ),
            types.SimpleNamespace(
                entries=[self._entry("2606.00001")],
                feed={"opensearch_totalresults": "3"},
            ),
        ]
        with patch.object(scraper, "_request_arxiv_feed", side_effect=["page-1", "page-2"]) as request_feed, \
             patch("src.scraper.feedparser.parse", side_effect=pages):
            papers = scraper.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertEqual([paper["paper_id"] for paper in papers], ["arxiv:2606.00001", "arxiv:2606.00002"])
        query = request_feed.call_args_list[0].args[0]["search_query"]
        self.assertIn("cat:cs.RO", query)
        self.assertIn("cat:cs.AI", query)
        self.assertEqual(scraper.last_arxiv_scan["duplicate_candidates"], 1)
        self.assertEqual(scraper.last_arxiv_scan["unique_candidates"], 2)

    def test_interrupted_scan_keeps_cached_pages_for_complete_retry(self):
        self.config["search"].update({"arxiv_page_size": 2, "arxiv_max_attempts": 1})
        page_one = types.SimpleNamespace(
            entries=[self._entry("2606.00001"), self._entry("2606.00002")],
            feed={"opensearch_totalresults": "3"},
        )
        page_two = types.SimpleNamespace(
            entries=[self._entry("2606.00003")],
            feed={"opensearch_totalresults": "3"},
        )
        first = PaperScraper(self.config)

        with patch("src.scraper.requests.get", side_effect=[
            FakeResponse(text="<feed></feed>"),
            FakeResponse(status_code=503, text="unavailable"),
        ]), patch("src.scraper.feedparser.parse", return_value=page_one):
            with self.assertRaises(PaperSourceError):
                first.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertFalse(first.last_arxiv_scan["complete"])
        self.assertEqual(first.last_arxiv_scan["pages_fetched"], 1)
        cached_pages = list(Path(self.tmp).joinpath("Cache", "arxiv").glob("*.xml"))
        self.assertEqual(len(cached_pages), 1)

        retry = PaperScraper(self.config)
        with patch("src.scraper.requests.get", return_value=FakeResponse(text="<feed></feed>")) as request, \
             patch("src.scraper.feedparser.parse", side_effect=[page_one, page_two]):
            papers = retry.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertEqual(len(papers), 3)
        self.assertTrue(retry.last_arxiv_scan["complete"])
        request.assert_called_once()

    def test_arxiv_fetch_without_total_results_stops_after_short_page(self):
        self.config["search"]["arxiv_page_size"] = 2
        scraper = PaperScraper(self.config)
        parsed = types.SimpleNamespace(entries=[self._entry("2606.00001")], feed={})
        with patch.object(scraper, "_request_arxiv_feed", return_value="page") as request_feed, \
             patch("src.scraper.feedparser.parse", return_value=parsed):
            papers = scraper.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertEqual(len(papers), 1)
        request_feed.assert_called_once()

    def test_repeated_arxiv_page_is_a_source_failure(self):
        self.config["search"]["arxiv_page_size"] = 1
        scraper = PaperScraper(self.config)
        parsed = types.SimpleNamespace(
            entries=[self._entry("2606.00001")],
            feed={"opensearch_totalresults": "2"},
        )
        with patch.object(scraper, "_request_arxiv_feed", side_effect=["page-1", "page-2"]), \
             patch("src.scraper.feedparser.parse", side_effect=[parsed, parsed]):
            with self.assertRaises(PaperSourceError):
                scraper.fetch_arxiv_papers(date(2026, 6, 1))

        self.assertFalse(scraper.last_arxiv_scan["complete"])
        self.assertIn("repeated", scraper.last_arxiv_scan["error"])

    def test_all_category_mode_omits_category_clause(self):
        self.config["search"]["arxiv_category_mode"] = "all"
        scraper = PaperScraper(self.config)
        query = scraper._build_arxiv_query(date(2026, 6, 1))
        self.assertEqual(query, "submittedDate:[202606010000 TO 202606012359]")

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

    def test_hf_daily_papers_uses_only_official_endpoint(self):
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

        with patch(
            "src.scraper.requests.get",
            return_value=FakeResponse(status_code=200, json_data=payload),
        ) as mocked_get:
            papers = scraper.fetch_hf_daily_papers(date(2026, 6, 3))

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["paper_id"], "arxiv:2605.25802")
        self.assertEqual(papers[0]["url"], "https://arxiv.org/abs/2605.25802")
        mocked_get.assert_called_once()
        self.assertEqual(mocked_get.call_args.args[0], "https://huggingface.co/api/daily_papers")
        self.assertEqual(mocked_get.call_args.kwargs["timeout"][0], 15)

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
          <div class="dateline">Submitted on 27 May 2026 (v1), last revised 29 May 2026</div>
          <div class="authors"><a>Ada</a><a>Lin</a></div>
          <blockquote class="abstract">Abstract: Robot manipulation abstract.</blockquote>
        </html>
        """

        with patch.object(scraper, "_request_arxiv_feed", side_effect=RuntimeError("api down")), \
             patch("src.scraper.requests.get", return_value=FakeResponse(status_code=200, text=html)):
            paper = scraper.fetch_single_arxiv_paper("2605.25802")

        self.assertEqual(paper["title"], "Fallback Robot Paper")
        self.assertEqual(paper["pdf_url"], "https://arxiv.org/pdf/2605.25802.pdf")
        self.assertEqual(paper["publication_date"], "2026-05-27")
        self.assertEqual(paper["authors"], ["Ada", "Lin"])

    def test_single_arxiv_feed_sets_publication_date_and_updated_metadata(self):
        self.config["search"]["arxiv_cache_enabled"] = False
        scraper = PaperScraper(self.config)
        entry = {
            "id": "https://arxiv.org/abs/2605.25802v1",
            "title": "Robot Foundation Model",
            "summary": "A robot manipulation paper.",
            "authors": [{"name": "Ada"}],
            "links": [],
            "published_parsed": (2026, 5, 27, 12, 30, 0, 0, 0, 0),
            "updated_parsed": (2026, 5, 29, 8, 15, 0, 0, 0, 0),
        }

        with patch.object(scraper, "_request_arxiv_feed", return_value="hit"), \
             patch("src.scraper.feedparser.parse", return_value=types.SimpleNamespace(entries=[entry])):
            paper = scraper.fetch_single_arxiv_paper("2605.25802")

        self.assertEqual(paper["publication_date"], "2026-05-27")
        self.assertEqual(paper["arxiv_updated_at"], "2026-05-29T08:15:00")
        self.assertEqual(paper["paper_id"], "arxiv:2605.25802")

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

    def test_arxiv_source_failure_is_not_converted_to_empty_success(self):
        scraper = PaperScraper(self.config)
        with patch.object(scraper, "_request_arxiv_feed", side_effect=RuntimeError("network down")):
            with self.assertRaises(PaperSourceError):
                scraper.fetch_arxiv_papers(date(2026, 6, 1))

    def test_all_source_failures_raise_network_unavailable(self):
        scraper = PaperScraper(self.config)
        with patch.object(scraper, "fetch_arxiv_papers", side_effect=PaperSourceError("arXiv down")), \
             patch.object(scraper, "fetch_hf_daily_papers", side_effect=PaperSourceError("HF down")):
            with self.assertRaises(NetworkUnavailableError):
                scraper.get_all_papers(date(2026, 6, 1))

    def test_one_source_failure_still_returns_other_source_results(self):
        scraper = PaperScraper(self.config)
        hf_paper = {
            "title": "Robot Paper",
            "url": "https://arxiv.org/abs/2606.02486",
            "abstract": "robot manipulation",
        }
        with patch.object(scraper, "fetch_arxiv_papers", side_effect=PaperSourceError("arXiv down")), \
             patch.object(scraper, "fetch_hf_daily_papers", return_value=[hf_paper]):
            papers = scraper.get_all_papers(date(2026, 6, 1))

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["paper_id"], "arxiv:2606.02486")

    def test_one_source_failure_exposes_structured_degraded_report(self):
        scraper = PaperScraper(self.config)
        paper = {"title": "Robot Paper", "url": "https://arxiv.org/abs/2605.25802"}
        with patch.object(scraper, "fetch_arxiv_papers", side_effect=PaperSourceError("arXiv down")), \
             patch.object(scraper, "fetch_hf_daily_papers", return_value=[paper]):
            scraper.get_all_papers(date(2026, 6, 1))

        warning = scraper.last_source_report["warnings"][0]
        self.assertEqual(warning["code"], "source_degraded")
        self.assertEqual(warning["source"], "arxiv")
        self.assertTrue(warning["retryable"])
        self.assertTrue(scraper.last_source_report["sources"]["huggingface"]["ok"])

    def test_arxiv_rejects_unexpected_http_200_payload(self):
        self.config["search"]["arxiv_cache_enabled"] = False
        scraper = PaperScraper(self.config)
        with patch("src.scraper.requests.get", return_value=FakeResponse(status_code=200, text="<html>error</html>")):
            with self.assertRaises(ValueError):
                scraper._request_arxiv_feed({"search_query": "cat:cs.RO", "start": 0, "max_results": 1})

    def test_hf_rejects_unexpected_http_200_payload(self):
        self.config["search"].update({"hf_cache_enabled": False, "hf_max_attempts": 1})
        scraper = PaperScraper(self.config)
        with patch("src.scraper.requests.get", return_value=FakeResponse(status_code=200, json_data={"error": "oops"})):
            with self.assertRaises(ValueError):
                scraper._request_hf_daily_papers({"date": "2026-06-01"})

    def test_single_paper_rejects_mismatched_feed_identity(self):
        scraper = PaperScraper(self.config)
        wrong_entry = {
            "id": "https://arxiv.org/abs/2605.99999",
            "title": "Wrong Paper",
            "summary": "Robot paper.",
            "links": [],
        }
        with patch.object(scraper, "_request_arxiv_feed", return_value="feed"), \
             patch("src.scraper.feedparser.parse", return_value=types.SimpleNamespace(entries=[wrong_entry])), \
             patch.object(scraper, "_fetch_single_arxiv_abs_page", return_value=None):
            with self.assertRaises(SinglePaperFetchError) as raised:
                scraper.fetch_single_arxiv_paper("2605.25802")

        self.assertEqual(raised.exception.code, "single_paper_identity_mismatch")

    def test_single_paper_empty_result_is_typed_failure(self):
        scraper = PaperScraper(self.config)
        with patch.object(scraper, "_request_arxiv_feed", return_value="feed"), \
             patch("src.scraper.feedparser.parse", return_value=types.SimpleNamespace(entries=[])), \
             patch.object(scraper, "_fetch_single_arxiv_abs_page", return_value=None):
            with self.assertRaises(SinglePaperFetchError) as raised:
                scraper.fetch_single_arxiv_paper("2605.25802")

        self.assertEqual(raised.exception.code, "single_paper_not_found")
        self.assertFalse(raised.exception.retryable)


if __name__ == "__main__":
    unittest.main()
