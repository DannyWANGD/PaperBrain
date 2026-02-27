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

    def fetch_arxiv_papers(self, target_date=None):
        """Fetches papers from arXiv based on keywords and categories."""
        logger.info(f"[INFO] Searching arXiv for categories: {self.categories}...")
        
        # Build query parts
        cat_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        
        # If target_date is provided, add submittedDate range
        if target_date:
            # arXiv uses YYYYMMDDHHMMSS format for dates in queries
            # To get papers for a specific date, we look for submittedDate in [target_date, target_date+1]
            start_str = target_date.strftime("%Y%m%d") + "0000"
            # End is end of the target date
            end_str = target_date.strftime("%Y%m%d") + "2359"
            
            date_query = f"submittedDate:[{start_str} TO {end_str}]"
            query = f"({cat_query}) AND {date_query}"
            logger.info(f"  [INFO] Using date query: {date_query}")
        else:
            query = cat_query
            
        # Sort by submittedDate
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=self.max_results, # We can use normal limit now since query is specific
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers = []
        try:
            results = list(client.results(search))
            logger.info(f"  [INFO] Fetched {len(results)} candidates from arXiv. Filtering by keywords...")
            
            for result in results:
                # Double check date if target_date provided (API sometimes is approximate)
                if target_date:
                    if result.published.date() != target_date:
                        continue
                
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
        arxiv_papers = self.fetch_arxiv_papers(target_date)
        hf_papers = self.fetch_hf_daily_papers(target_date)
        
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
