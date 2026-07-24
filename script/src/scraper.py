import feedparser
import requests
from datetime import datetime, timedelta
import logging
import time
import random
import hashlib
import os
import json
import re
import xml.etree.ElementTree as ET
from src.paper_identity import canonical_arxiv_id, identity_key, normalize_paper_identity
from src.paths import PaperBrainPaths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup


class PaperSourceError(RuntimeError):
    """Raised when one configured paper source cannot be queried."""

    code = "source_unavailable"
    retryable = True


class NetworkUnavailableError(RuntimeError):
    """Raised when all configured paper sources are unavailable."""

    code = "network_unavailable"
    retryable = True


class SinglePaperFetchError(PaperSourceError):
    """Raised when an explicitly requested arXiv paper cannot be identified."""

    def __init__(self, code, message, retryable=False):
        super().__init__(message)
        self.code = str(code)
        self.retryable = bool(retryable)


def _date_key(value):
    if value is None:
        return ""
    if hasattr(value, "date"):
        return value.date().isoformat()
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, str) and len(value) >= 10:
        return value[:10]
    return ""


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
        self.arxiv_min_interval = float(config.get('search', {}).get('arxiv_min_interval_seconds', 3.2))
        endpoints = config.get('search', {}).get('arxiv_api_endpoints') or [
            "https://export.arxiv.org/api/query",
            "https://arxiv.org/api/query",
        ]
        self.arxiv_api_endpoints = [str(endpoint).strip() for endpoint in endpoints if str(endpoint).strip()]
        self.arxiv_cache_enabled = bool(config.get('search', {}).get('arxiv_cache_enabled', True))
        self.arxiv_cache_ttl_hours = float(config.get('search', {}).get('arxiv_cache_ttl_hours', 72))
        self.arxiv_rate_limit_cooldown_minutes = float(
            config.get('search', {}).get('arxiv_rate_limit_cooldown_minutes', 60)
        )
        self.hf_user_agent = config.get(
            'search', {}
        ).get(
            'hf_user_agent',
            self.arxiv_user_agent
        )
        self.hf_connect_timeout = float(config.get('search', {}).get('hf_connect_timeout_seconds', 15))
        self.hf_read_timeout = float(
            config.get('search', {}).get(
                'hf_read_timeout_seconds',
                config.get('search', {}).get('hf_timeout_seconds', 15)
            )
        )
        self.hf_max_attempts = int(config.get('search', {}).get('hf_max_attempts', 2))
        self.hf_min_interval = float(config.get('search', {}).get('hf_min_interval_seconds', 1.0))
        self.hf_daily_papers_endpoints = ["https://huggingface.co/api/daily_papers"]
        self.hf_cache_enabled = bool(config.get('search', {}).get('hf_cache_enabled', True))
        self.hf_cache_ttl_hours = float(config.get('search', {}).get('hf_cache_ttl_hours', 72))
        self.hf_failure_cooldown_minutes = float(
            config.get('search', {}).get('hf_failure_cooldown_minutes', 20)
        )
        paths = PaperBrainPaths.from_config_dict(config)
        self.cache_dir = str(paths.arxiv_cache_dir)
        self.cooldown_path = os.path.join(self.cache_dir, "rate_limit_cooldown.json")
        self.hf_cache_dir = str(paths.huggingface_cache_dir)
        self.hf_cooldown_path = os.path.join(self.hf_cache_dir, "failure_cooldown.json")
        self.last_arxiv_request_at = 0.0
        self.last_hf_request_at = 0.0
        self.last_source_report = {"sources": {}, "warnings": []}
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.hf_cache_dir, exist_ok=True)

    @staticmethod
    def _validate_arxiv_feed_payload(raw_feed):
        if not isinstance(raw_feed, str) or not raw_feed.strip():
            raise ValueError("arXiv returned an empty or non-text HTTP 200 payload")
        try:
            root = ET.fromstring(raw_feed)
        except ET.ParseError as exc:
            raise ValueError("arXiv returned malformed XML in an HTTP 200 response") from exc
        root_name = str(root.tag).rsplit("}", 1)[-1].lower()
        if root_name != "feed":
            raise ValueError(f"arXiv returned unexpected HTTP 200 payload root: {root_name or 'unknown'}")
        return raw_feed

    @staticmethod
    def _validate_hf_payload(data):
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ("papers", "daily_papers", "results"):
                if key in data:
                    value = data[key]
                    if isinstance(value, list):
                        return data
                    raise ValueError(f"Hugging Face HTTP 200 field '{key}' is not a list")
        raise ValueError("Hugging Face returned an unexpected HTTP 200 JSON payload")

    def _clean_html(self, text):
        return BeautifulSoup(text, "html.parser").get_text()

    def _extract_arxiv_id(self, url_or_id):
        return canonical_arxiv_id(url_or_id)

    def _build_arxiv_query(self, target_date=None):
        cat_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        if target_date:
            start_str = target_date.strftime("%Y%m%d") + "0000"
            end_str = target_date.strftime("%Y%m%d") + "2359"
            date_query = f"submittedDate:[{start_str} TO {end_str}]"
            logger.info(f"  [INFO] Using date query: {date_query}")
            return f"({cat_query}) AND {date_query}"
        return cat_query

    def _cache_key(self, params):
        encoded = json.dumps(params, sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(encoded.encode("utf-8")).hexdigest()

    def _cache_path(self, params):
        return os.path.join(self.cache_dir, f"{self._cache_key(params)}.xml")

    def _read_cached_feed(self, params, allow_expired=False):
        if not self.arxiv_cache_enabled:
            return None
        path = self._cache_path(params)
        if not os.path.exists(path):
            return None
        age_hours = (time.time() - os.path.getmtime(path)) / 3600
        if not allow_expired and age_hours > self.arxiv_cache_ttl_hours:
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            logger.info(
                "  [CACHE] Using %s arXiv feed cache (%s, age %.1fh).",
                "expired" if age_hours > self.arxiv_cache_ttl_hours else "fresh",
                os.path.basename(path),
                age_hours,
            )
            return raw
        except Exception:
            return None

    def _write_cached_feed(self, params, raw_feed):
        if not self.arxiv_cache_enabled or not raw_feed:
            return
        try:
            with open(self._cache_path(params), "w", encoding="utf-8") as f:
                f.write(raw_feed)
        except Exception as e:
            logger.debug("Failed to write arXiv cache: %s", e)

    def _hf_cache_key(self, params):
        encoded = json.dumps(params, sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(encoded.encode("utf-8")).hexdigest()

    def _hf_cache_path(self, params):
        return os.path.join(self.hf_cache_dir, f"{self._hf_cache_key(params)}.json")

    def _read_cached_hf_daily_papers(self, params, allow_expired=False):
        if not self.hf_cache_enabled:
            return None
        path = self._hf_cache_path(params)
        if not os.path.exists(path):
            return None
        age_hours = (time.time() - os.path.getmtime(path)) / 3600
        if not allow_expired and age_hours > self.hf_cache_ttl_hours:
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(
                "  [CACHE] Using %s Hugging Face daily papers cache (%s, age %.1fh).",
                "expired" if age_hours > self.hf_cache_ttl_hours else "fresh",
                os.path.basename(path),
                age_hours,
            )
            return data
        except Exception:
            return None

    def _write_cached_hf_daily_papers(self, params, data):
        if not self.hf_cache_enabled or data is None:
            return
        try:
            with open(self._hf_cache_path(params), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logger.debug("Failed to write Hugging Face daily papers cache: %s", e)

    def _cooldown_remaining_seconds(self):
        if not os.path.exists(self.cooldown_path):
            return 0.0
        try:
            with open(self.cooldown_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            until_ts = float(data.get("until", 0))
            return max(0.0, until_ts - time.time())
        except Exception:
            return 0.0

    def _mark_arxiv_cooldown(self, reason):
        until_ts = time.time() + self.arxiv_rate_limit_cooldown_minutes * 60
        try:
            with open(self.cooldown_path, "w", encoding="utf-8") as f:
                json.dump({"until": until_ts, "reason": reason, "created_at": datetime.now().isoformat()}, f, indent=2)
        except Exception:
            pass

    def _hf_cooldown_remaining_seconds(self):
        if not os.path.exists(self.hf_cooldown_path):
            return 0.0
        try:
            with open(self.hf_cooldown_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            until_ts = float(data.get("until", 0))
            return max(0.0, until_ts - time.time())
        except Exception:
            return 0.0

    def _mark_hf_cooldown(self, reason):
        until_ts = time.time() + self.hf_failure_cooldown_minutes * 60
        try:
            with open(self.hf_cooldown_path, "w", encoding="utf-8") as f:
                json.dump({"until": until_ts, "reason": reason, "created_at": datetime.now().isoformat()}, f, indent=2)
        except Exception:
            pass

    def _respect_arxiv_interval(self):
        elapsed = time.time() - self.last_arxiv_request_at
        wait_s = self.arxiv_min_interval - elapsed
        if wait_s > 0:
            time.sleep(wait_s)

    def _respect_hf_interval(self):
        elapsed = time.time() - self.last_hf_request_at
        wait_s = self.hf_min_interval - elapsed
        if wait_s > 0:
            time.sleep(wait_s)

    def _request_arxiv_feed(self, params):
        headers = {"User-Agent": self.arxiv_user_agent}
        last_error = None
        saw_429 = False

        cached = self._read_cached_feed(params, allow_expired=False)
        if cached:
            try:
                return self._validate_arxiv_feed_payload(cached)
            except ValueError as exc:
                logger.warning("[WARN] Ignoring invalid cached arXiv payload: %s", exc)

        cooldown_remaining = self._cooldown_remaining_seconds()
        if cooldown_remaining > 0:
            expired = self._read_cached_feed(params, allow_expired=True)
            if expired:
                try:
                    return self._validate_arxiv_feed_payload(expired)
                except ValueError as exc:
                    logger.warning("[WARN] Ignoring invalid expired arXiv payload: %s", exc)
            raise RuntimeError(
                f"arXiv API is in local cooldown for {cooldown_remaining / 60:.1f} more minutes after rate limiting."
            )

        for attempt in range(1, self.arxiv_max_attempts + 1):
            for url in self.arxiv_api_endpoints:
                try:
                    self._respect_arxiv_interval()
                    response = requests.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=self.arxiv_timeout,
                    )
                    self.last_arxiv_request_at = time.time()
                    if response.status_code == 200:
                        try:
                            raw_feed = self._validate_arxiv_feed_payload(response.text)
                        except ValueError as exc:
                            last_error = exc
                            logger.warning("[WARN] Invalid arXiv HTTP 200 payload from %s: %s", url, exc)
                            continue
                        self._write_cached_feed(params, raw_feed)
                        return raw_feed

                    if response.status_code in (429, 403, 503):
                        last_error = RuntimeError(f"HTTP {response.status_code} from arXiv API endpoint {url}")
                        saw_429 = saw_429 or response.status_code == 429
                        logger.warning(
                            f"[WARN] arXiv API endpoint {url} returned HTTP {response.status_code} "
                            f"({attempt}/{self.arxiv_max_attempts})."
                        )
                        continue

                    response.raise_for_status()
                except requests.RequestException as e:
                    last_error = e
                    logger.warning(f"[WARN] arXiv request failed via {url}: {e}")

            if attempt < self.arxiv_max_attempts:
                base_delay = max(15, 8 * (2 ** (attempt - 1))) if saw_429 else 8 * (2 ** (attempt - 1))
                jitter = random.uniform(1.0, 5.0)
                sleep_s = min(base_delay + jitter, 90.0)
                logger.warning(
                    f"[WARN] arXiv API endpoints failed. Backing off {sleep_s:.1f}s "
                    f"before retry ({attempt}/{self.arxiv_max_attempts})..."
                )
                time.sleep(sleep_s)
                continue

        if saw_429 and last_error:
            self._mark_arxiv_cooldown(str(last_error))
        expired = self._read_cached_feed(params, allow_expired=True)
        if expired:
            try:
                expired = self._validate_arxiv_feed_payload(expired)
            except ValueError as exc:
                logger.warning("[WARN] Ignoring invalid expired arXiv payload: %s", exc)
            else:
                logger.warning("[WARN] Live arXiv API failed; falling back to expired arXiv cache.")
                return expired
        if last_error:
            raise last_error
        raise RuntimeError("Unknown arXiv API error")

    def _request_hf_daily_papers(self, params):
        headers = {
            "User-Agent": self.hf_user_agent,
            "Accept": "application/json",
        }
        last_error = None

        cached = self._read_cached_hf_daily_papers(params, allow_expired=False)
        if cached is not None:
            try:
                return self._validate_hf_payload(cached)
            except ValueError as exc:
                logger.warning("[WARN] Ignoring invalid cached Hugging Face payload: %s", exc)

        cooldown_remaining = self._hf_cooldown_remaining_seconds()
        if cooldown_remaining > 0:
            expired = self._read_cached_hf_daily_papers(params, allow_expired=True)
            if expired is not None:
                try:
                    return self._validate_hf_payload(expired)
                except ValueError as exc:
                    logger.warning("[WARN] Ignoring invalid expired Hugging Face payload: %s", exc)
            raise RuntimeError(
                f"Hugging Face daily papers is in local cooldown for {cooldown_remaining / 60:.1f} more minutes."
            )

        for attempt in range(1, self.hf_max_attempts + 1):
            for url in self.hf_daily_papers_endpoints:
                try:
                    self._respect_hf_interval()
                    response = requests.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=(self.hf_connect_timeout, self.hf_read_timeout),
                    )
                    self.last_hf_request_at = time.time()
                    if response.status_code == 200:
                        try:
                            data = self._validate_hf_payload(response.json())
                        except (TypeError, ValueError) as exc:
                            last_error = exc
                            logger.warning("[WARN] Invalid Hugging Face HTTP 200 payload from %s: %s", url, exc)
                            continue
                        self._write_cached_hf_daily_papers(params, data)
                        return data

                    if response.status_code in (429, 403, 500, 502, 503, 504):
                        last_error = RuntimeError(f"HTTP {response.status_code} from Hugging Face endpoint {url}")
                        logger.warning(
                            f"[WARN] Hugging Face endpoint {url} returned HTTP {response.status_code} "
                            f"({attempt}/{self.hf_max_attempts})."
                        )
                        continue

                    response.raise_for_status()
                except (requests.RequestException, ValueError) as e:
                    last_error = e
                    logger.warning(f"[WARN] Hugging Face request failed via {url}: {e}")

            if attempt < self.hf_max_attempts:
                sleep_s = min(5 * (2 ** (attempt - 1)) + random.uniform(0.5, 3.0), 30.0)
                logger.warning(
                    f"[WARN] Hugging Face endpoints failed. Backing off {sleep_s:.1f}s "
                    f"before retry ({attempt}/{self.hf_max_attempts})..."
                )
                time.sleep(sleep_s)

        if last_error:
            self._mark_hf_cooldown(str(last_error))
        expired = self._read_cached_hf_daily_papers(params, allow_expired=True)
        if expired is not None:
            try:
                expired = self._validate_hf_payload(expired)
            except ValueError as exc:
                logger.warning("[WARN] Ignoring invalid expired Hugging Face payload: %s", exc)
            else:
                logger.warning("[WARN] Live Hugging Face daily papers failed; falling back to expired cache.")
                return expired
        if last_error:
            raise last_error
        raise RuntimeError("Unknown Hugging Face daily papers error")

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
        updated = None
        updated_parsed = entry.get("updated_parsed")
        if updated_parsed:
            updated = datetime(*updated_parsed[:6])

        authors = []
        for author in entry.get("authors", []):
            if isinstance(author, dict):
                name = author.get("name", "")
            else:
                name = getattr(author, "name", "")
            if name:
                authors.append(name)

        return normalize_paper_identity({
            'title': self._clean_html(entry.get("title", "")).strip(),
            'abstract': self._clean_html(entry.get("summary", "")).strip(),
            'url': entry_id,
            'pdf_url': self._extract_pdf_url(entry, entry_id),
            'published': published,
            'publication_date': _date_key(published),
            'arxiv_updated_at': updated.isoformat() if updated else "",
            'source': source,
            'authors': authors
        })

    def _single_arxiv_query_variants(self, arxiv_id):
        base = {
            "start": 0,
            "max_results": 1,
        }
        return [
            {**base, "search_query": "", "id_list": arxiv_id},
            {**base, "search_query": f"id:{arxiv_id}", "id_list": ""},
            {**base, "search_query": f"all:{arxiv_id}", "id_list": ""},
        ]

    def _fetch_single_arxiv_abs_page(self, arxiv_id):
        url = f"https://arxiv.org/abs/{arxiv_id}"
        try:
            response = requests.get(
                url,
                headers={"User-Agent": self.arxiv_user_agent},
                timeout=self.arxiv_timeout,
            )
            if response.status_code != 200:
                logger.warning("arXiv abs fallback failed for %s: HTTP %s", arxiv_id, response.status_code)
                return None
            soup = BeautifulSoup(response.text, "html.parser")

            def clean_labeled(node, label):
                if not node:
                    return ""
                text = node.get_text(" ", strip=True)
                return text.replace(label, "", 1).strip()

            title = clean_labeled(soup.find("h1", class_="title"), "Title:")
            abstract = clean_labeled(soup.find("blockquote", class_="abstract"), "Abstract:")
            published = self._parse_abs_submitted_date(soup.find("div", class_="dateline"))
            authors_node = soup.find("div", class_="authors")
            authors = []
            if authors_node:
                authors = [a.get_text(" ", strip=True) for a in authors_node.find_all("a") if a.get_text(strip=True)]

            if not title:
                logger.warning("arXiv abs fallback found no title for %s", arxiv_id)
                return None

            return normalize_paper_identity({
                "title": title,
                "abstract": abstract,
                "url": url,
                "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                "published": published,
                "publication_date": _date_key(published),
                "source": "arXiv",
                "authors": authors,
            })
        except Exception as e:
            logger.error(f"[ERR] arXiv abs fallback failed for {arxiv_id}: {e}")
            return None

    def _parse_abs_submitted_date(self, node):
        if not node:
            return None
        text = node.get_text(" ", strip=True)
        match = re.search(r"Submitted\s+on\s+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})", text)
        if not match:
            return None
        raw = match.group(1)
        for fmt in ("%d %b %Y", "%d %B %Y"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        return None

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
                raise PaperSourceError(f"arXiv source unavailable: {e}") from e
            logger.error(f"[ERR] Error fetching arXiv: {e}")
            raise PaperSourceError(f"arXiv source unavailable: {e}") from e

        logger.info(f"  [INFO] Found {len(papers)} relevant papers from arXiv.")
        return papers

    def fetch_hf_daily_papers(self, target_date=None):
        """Fetches papers from Hugging Face Daily Papers API."""
        logger.info("Fetching from Hugging Face Daily Papers...")
        
        # If no target_date, default to yesterday
        if not target_date:
             target_date = datetime.now().date() - timedelta(days=1)
        
        date_str = target_date.strftime("%Y-%m-%d")
        params = {"date": date_str}
        
        papers = []
        try:
            data = self._validate_hf_payload(self._request_hf_daily_papers(params))
            if isinstance(data, dict):
                data = next(data[key] for key in ("papers", "daily_papers", "results") if key in data)
            # data is usually a list of objects like [{"paper": {...}}, ...].
            for item in data or []:
                paper_info = item.get('paper', item) if isinstance(item, dict) else {}
                if not paper_info:
                    continue
                    
                title = paper_info.get('title', '')
                summary = paper_info.get('summary', '') or paper_info.get('abstract', '')
                paper_id = paper_info.get('id', '') or paper_info.get('paper_id', '')
                arxiv_id = self._extract_arxiv_id(paper_id)
                if not arxiv_id:
                    arxiv_id = self._extract_arxiv_id(paper_info.get('url', '') or paper_info.get('arxiv_id', ''))
                if not arxiv_id:
                    continue
                
                authors = []
                for author in paper_info.get('authors', []):
                    if isinstance(author, dict):
                        name = author.get('name', '')
                    else:
                        name = str(author)
                    if name:
                        authors.append(name)

                # Filter by keywords
                text_content = (title + " " + summary).lower()
                if any(k.lower() in text_content for k in self.keywords):
                    papers.append(normalize_paper_identity({
                        'title': title,
                        'abstract': summary,
                        'url': f"https://arxiv.org/abs/{arxiv_id}",
                        'pdf_url': f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                        'published': target_date, # Since we queried by date
                        'publication_date': _date_key(target_date),
                        'source': 'HuggingFace',
                        'authors': authors
                    }))
        except Exception as e:
            logger.error(f"Error fetching HF papers: {e}")
            raise PaperSourceError(f"Hugging Face source unavailable: {e}") from e
        
        logger.info(f"Found {len(papers)} relevant papers from Hugging Face.")
        return papers

    def get_all_papers(self, target_date=None):
        self.last_source_report = {"sources": {}, "warnings": []}
        source_errors = []
        try:
            arxiv_papers = self.fetch_arxiv_papers(target_date)
        except Exception as e:
            logger.error(f"[ERR] Failed to fetch arXiv papers. Skipping arXiv for this run. {e}")
            arxiv_papers = []
            source_errors.append(str(e))
            warning = {
                "code": "source_degraded",
                "source": "arxiv",
                "message": str(e),
                "retryable": True,
            }
            self.last_source_report["sources"]["arxiv"] = {"ok": False, **warning}
            self.last_source_report["warnings"].append(warning)
        else:
            self.last_source_report["sources"]["arxiv"] = {
                "ok": True,
                "count": len(arxiv_papers),
            }
        try:
            hf_papers = self.fetch_hf_daily_papers(target_date)
        except Exception as e:
            logger.error(f"[ERR] Failed to fetch Hugging Face papers. {e}")
            hf_papers = []
            source_errors.append(str(e))
            warning = {
                "code": "source_degraded",
                "source": "huggingface",
                "message": str(e),
                "retryable": True,
            }
            self.last_source_report["sources"]["huggingface"] = {"ok": False, **warning}
            self.last_source_report["warnings"].append(warning)
        else:
            self.last_source_report["sources"]["huggingface"] = {
                "ok": True,
                "count": len(hf_papers),
            }

        if len(source_errors) == 2:
            raise NetworkUnavailableError("All paper sources are unavailable: " + " | ".join(source_errors))
        
        # Deduplicate by canonical paper identity, falling back to normalized title.
        seen_keys = set()
        unique_papers = []
        
        for p in arxiv_papers + hf_papers:
            p = normalize_paper_identity(p)
            key = identity_key(p)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_papers.append(p)
                
        return unique_papers

    def fetch_single_arxiv_paper(self, arxiv_url_or_id):
        arxiv_id = self._extract_arxiv_id(arxiv_url_or_id)
        if not arxiv_id:
            raise SinglePaperFetchError(
                "single_paper_invalid_id",
                f"The requested value does not contain a valid modern arXiv ID: {arxiv_url_or_id}",
                retryable=False,
            )
        last_error = None
        saw_empty_result = False
        mismatched_ids = []
        for params in self._single_arxiv_query_variants(arxiv_id):
            try:
                raw_feed = self._request_arxiv_feed(params)
                results = feedparser.parse(raw_feed).entries or []
            except Exception as e:
                last_error = e
                logger.warning(f"[WARN] Failed arXiv single-paper API query for {arxiv_id}: {e}")
                continue

            if results:
                for entry in results:
                    candidate = self._entry_to_paper(entry, 'arXiv')
                    candidate_id = canonical_arxiv_id(candidate.get("paper_id"))
                    if candidate_id == arxiv_id:
                        return candidate
                    if candidate_id:
                        mismatched_ids.append(candidate_id)
                logger.warning(
                    "[WARN] arXiv single-paper query for %s returned only mismatched identities: %s",
                    arxiv_id,
                    ", ".join(mismatched_ids[-len(results):]) or "unknown",
                )
                continue
            saw_empty_result = True

        if last_error:
            logger.error(f"[ERR] Failed to fetch arXiv paper {arxiv_id}: {last_error}")
        elif saw_empty_result:
            logger.error(f"[ERR] No arXiv paper found for id: {arxiv_id}")

        logger.info("[INFO] Trying arXiv abs page fallback for %s...", arxiv_id)
        fallback = self._fetch_single_arxiv_abs_page(arxiv_id)
        if fallback:
            fallback = normalize_paper_identity(fallback)
            fallback_id = canonical_arxiv_id(fallback.get("paper_id"))
            if fallback_id == arxiv_id:
                return fallback
            if fallback_id:
                mismatched_ids.append(fallback_id)

        if mismatched_ids:
            raise SinglePaperFetchError(
                "single_paper_identity_mismatch",
                f"arXiv returned {', '.join(sorted(set(mismatched_ids)))} while {arxiv_id} was requested",
                retryable=True,
            )
        if last_error and not saw_empty_result:
            raise SinglePaperFetchError(
                "single_paper_source_unavailable",
                f"Unable to fetch requested arXiv paper {arxiv_id}: {last_error}",
                retryable=True,
            ) from last_error
        raise SinglePaperFetchError(
            "single_paper_not_found",
            f"No arXiv paper was found for requested ID {arxiv_id}",
            retryable=False,
        )
