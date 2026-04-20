import feedparser
import requests
from datetime import datetime, timedelta
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup

class PaperScraper:
    def __init__(self, config):
        self.config = config
        self.keywords = config['search']['keywords']
        self.categories = config['search']['arxiv_categories']
        self.max_results = config['search'].get('max_results', 50)
        self.arxiv_user_agent = config.get(
            'search', {}
        ).get(
            'arxiv_user_agent',
            'PaperBrain/1.0 (Academic paper metadata fetcher; contact: local-user)'
        )
        self.arxiv_timeout = int(config.get('search', {}).get('arxiv_timeout_seconds', 20))
        self.arxiv_max_attempts = int(config.get('search', {}).get('arxiv_max_attempts', 4))

    def _clean_html(self, text):
        return BeautifulSoup(text, "html.parser").get_text()

    def _extract_arxiv_id(self, url_or_id):
        if not url_or_id:
            return ""
        value = str(url_or_id).strip()
        if "arxiv.org" in value:
            value = value.split("/")[-1]
        value = value.replace(".pdf", "")
        value = value.split("?")[0]
        return value

    def _build_arxiv_query(self, target_date=None):
        cat_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        if target_date:
            start_str = target_date.strftime("%Y%m%d") + "0000"
            end_str = target_date.strftime("%Y%m%d") + "2359"
            date_query = f"submittedDate:[{start_str} TO {end_str}]"
            logger.info(f"  [INFO] Using date query: {date_query}")
            return f"({cat_query}) AND {date_query}"
        return cat_query

    def _request_arxiv_feed(self, params):
        url = "https://export.arxiv.org/api/query"
        headers = {"User-Agent": self.arxiv_user_agent}
        last_error = None

        for attempt in range(1, self.arxiv_max_attempts + 1):
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.arxiv_timeout,
                )
                if response.status_code == 200:
                    return response.text

                if response.status_code in (429, 403, 503):
                    last_error = RuntimeError(f"HTTP {response.status_code} from arXiv API")
                    if attempt < self.arxiv_max_attempts:
                        base_delay = 5 * (2 ** (attempt - 1))
                        jitter = random.uniform(0.0, 1.5)
                        sleep_s = min(base_delay + jitter, 45.0)
                        logger.warning(
                            f"[WARN] arXiv API returned HTTP {response.status_code}. "
                            f"Backing off {sleep_s:.1f}s before retry ({attempt}/{self.arxiv_max_attempts})..."
                        )
                        time.sleep(sleep_s)
                        continue
                    raise last_error

                response.raise_for_status()
            except requests.RequestException as e:
                last_error = e
                if attempt < self.arxiv_max_attempts:
                    base_delay = 5 * (2 ** (attempt - 1))
                    jitter = random.uniform(0.0, 1.5)
                    sleep_s = min(base_delay + jitter, 45.0)
                    logger.warning(
                        f"[WARN] arXiv request failed ({e}). Backing off {sleep_s:.1f}s "
                        f"before retry ({attempt}/{self.arxiv_max_attempts})..."
                    )
                    time.sleep(sleep_s)
                    continue
                raise

        if last_error:
            raise last_error
        raise RuntimeError("Unknown arXiv API error")

    def _extract_pdf_url(self, entry, entry_id):
        for link in entry.get("links", []):
            href = link.get("href", "")
            if link.get("title") == "pdf" or link.get("type") == "application/pdf":
                return href
        arxiv_id = self._extract_arxiv_id(entry_id)
        if arxiv_id:
            return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        return ""

    def _entry_to_paper(self, entry, source, published_override=None):
        entry_id = entry.get("id", "")
        published = published_override
        published_parsed = entry.get("published_parsed")
        if published is None and published_parsed:
            published = datetime(*published_parsed[:6])

        authors = []
        for author in entry.get("authors", []):
            if isinstance(author, dict):
                name = author.get("name", "")
            else:
                name = getattr(author, "name", "")
            if name:
                authors.append(name)

        return {
            'title': self._clean_html(entry.get("title", "")).strip(),
            'abstract': self._clean_html(entry.get("summary", "")).strip(),
            'url': entry_id,
            'pdf_url': self._extract_pdf_url(entry, entry_id),
            'published': published,
            'source': source,
            'authors': authors
        }

    def fetch_arxiv_papers(self, target_date=None):
        """Fetches papers from arXiv based on keywords and categories."""
        logger.info(f"[INFO] Searching arXiv for categories: {self.categories}...")

        query = self._build_arxiv_query(target_date)
        params = {
            "search_query": query,
            "id_list": "",
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": 0,
            "max_results": self.max_results,
        }

        papers = []
        try:
            raw_feed = self._request_arxiv_feed(params)
            results = feedparser.parse(raw_feed).entries or []
            logger.info(f"  [INFO] Fetched {len(results)} candidates from arXiv. Filtering by keywords...")

            for entry in results:
                paper = self._entry_to_paper(entry, 'arXiv')
                published = paper.get('published')
                if target_date and published and published.date() != target_date:
                    continue

                text_content = (paper['title'] + " " + paper['abstract']).lower()
                if any(k.lower() in text_content for k in self.keywords):
                    papers.append(paper)
        except Exception as e:
            msg = str(e)
            if "429" in msg or "Rate exceeded" in msg:
                logger.error(
                    "[ERR] arXiv API rate-limited this network/IP (HTTP 429 / Rate exceeded). "
                    "Custom User-Agent and exponential backoff were attempted, but the endpoint is still refusing requests. "
                    "Skipping arXiv for this run."
                )
                return []
            logger.error(f"[ERR] Error fetching arXiv: {e}")
            return []

        logger.info(f"  [INFO] Found {len(papers)} relevant papers from arXiv.")
        return papers

    def fetch_hf_daily_papers(self, target_date=None):
        """Fetches papers from Hugging Face Daily Papers API."""
        logger.info("Fetching from Hugging Face Daily Papers...")
        
        # If no target_date, default to yesterday
        if not target_date:
             target_date = datetime.now().date() - timedelta(days=1)
        
        date_str = target_date.strftime("%Y-%m-%d")
        api_url = f"https://huggingface.co/api/daily_papers?date={date_str}"
        
        papers = []
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                # data is a list of objects like [{"paper": {...}}, ...]
                
                for item in data:
                    paper_info = item.get('paper', {})
                    if not paper_info:
                        continue
                        
                    title = paper_info.get('title', '')
                    summary = paper_info.get('summary', '')
                    paper_id = paper_info.get('id', '') # e.g. "2602.10388"
                    
                    # Filter by keywords
                    text_content = (title + " " + summary).lower()
                    if any(k.lower() in text_content for k in self.keywords):
                        papers.append({
                            'title': title,
                            'abstract': summary,
                            'url': f"https://huggingface.co/papers/{paper_id}",
                            'pdf_url': f"https://arxiv.org/pdf/{paper_id}.pdf", # Construct arXiv PDF link
                            'published': target_date, # Since we queried by date
                            'source': 'HuggingFace',
                            'authors': [a.get('name') for a in paper_info.get('authors', [])]
                        })
            else:
                logger.warning(f"Failed to fetch HF papers: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching HF papers: {e}")
        
        logger.info(f"Found {len(papers)} relevant papers from Hugging Face.")
        return papers

    def get_all_papers(self, target_date=None):
        try:
            arxiv_papers = self.fetch_arxiv_papers(target_date)
        except Exception as e:
            logger.error(f"[ERR] Failed to fetch arXiv papers. Skipping arXiv for this run. {e}")
            arxiv_papers = []
        try:
            hf_papers = self.fetch_hf_daily_papers(target_date)
        except Exception as e:
            logger.error(f"[ERR] Failed to fetch Hugging Face papers. {e}")
            hf_papers = []
        
        # Deduplicate by title
        seen_titles = set()
        unique_papers = []
        
        for p in arxiv_papers + hf_papers:
            # Normalize title
            norm_title = p['title'].lower().strip()
            if norm_title not in seen_titles:
                seen_titles.add(norm_title)
                unique_papers.append(p)
                
        return unique_papers

    def fetch_single_arxiv_paper(self, arxiv_url_or_id):
        arxiv_id = self._extract_arxiv_id(arxiv_url_or_id)
        if not arxiv_id:
            return None
        try:
            raw_feed = self._request_arxiv_feed({
                "search_query": "",
                "id_list": arxiv_id,
                "start": 0,
                "max_results": 1,
            })
            results = feedparser.parse(raw_feed).entries or []
        except Exception as e:
            logger.error(f"[ERR] Failed to fetch arXiv paper {arxiv_id}: {e}")
            return None
        if not results:
            logger.error(f"[ERR] No arXiv paper found for id: {arxiv_id}")
            return None
        return self._entry_to_paper(results[0], 'arXiv')
