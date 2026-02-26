import arxiv
import feedparser
import requests
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup

class PaperScraper:
    def __init__(self, config):
        self.config = config
        self.keywords = config['search']['keywords']
        self.categories = config['search']['arxiv_categories']
        self.max_results = config['search'].get('max_results', 50)

    def _clean_html(self, text):
        return BeautifulSoup(text, "html.parser").get_text()

    def fetch_arxiv_papers(self):
        """Fetches papers from arXiv based on keywords and categories."""
        logger.info(f"[INFO] Searching arXiv for categories: {self.categories}...")
        
        # Broad query for categories
        cat_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        
        # Sort by submittedDate
        client = arxiv.Client()
        search = arxiv.Search(
            query=cat_query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers = []
        try:
            results = list(client.results(search))
            logger.info(f"  [INFO] Fetched {len(results)} candidates from arXiv. Filtering by keywords...")
            
            for result in results:
                # Filter by date (last 24 hours) to ensure freshness if run daily
                # But since we limit max_results, we might just take the latest.
                # Let's check if the abstract or title contains any keyword to filter noise
                text_content = (result.title + " " + result.summary).lower()
                if any(k.lower() in text_content for k in self.keywords):
                    papers.append({
                        'title': result.title,
                        'abstract': result.summary,
                        'url': result.entry_id,
                        'pdf_url': result.pdf_url,
                        'published': result.published,
                        'source': 'arXiv',
                        'authors': [a.name for a in result.authors]
                    })
        except Exception as e:
            logger.error(f"[ERR] Error fetching arXiv: {e}")

        logger.info(f"  [INFO] Found {len(papers)} relevant papers from arXiv.")
        return papers

    def fetch_hf_daily_papers(self):
        """Fetches papers from Hugging Face Daily Papers RSS."""
        logger.info("Fetching from Hugging Face Daily Papers...")
        rss_url = "https://rss.huggingface.co/papers"
        feed = feedparser.parse(rss_url)
        
        papers = []
        today = datetime.now().date()
        
        for entry in feed.entries:
            # Check if published today (or very recently)
            published_struct = entry.get('published_parsed')
            if published_struct:
                pub_date = datetime(*published_struct[:6]).date()
                if pub_date >= today - timedelta(days=1):
                    # Clean abstract
                    summary = self._clean_html(entry.summary)
                    
                    # Filter by keywords
                    text_content = (entry.title + " " + summary).lower()
                    if any(k.lower() in text_content for k in self.keywords):
                        papers.append({
                            'title': entry.title,
                            'abstract': summary,
                            'url': entry.link,
                            'pdf_url': entry.link.replace('huggingface.co/papers/', 'arxiv.org/pdf/') + ".pdf" if 'arxiv' in entry.link else None, # HF often links to arxiv
                            'published': pub_date,
                            'source': 'HuggingFace',
                            'authors': [] # RSS might not have authors easily parsed
                        })
        
        logger.info(f"Found {len(papers)} relevant papers from Hugging Face.")
        return papers

    def get_all_papers(self):
        arxiv_papers = self.fetch_arxiv_papers()
        hf_papers = self.fetch_hf_daily_papers()
        
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
