import yaml
import schedule
import time
import requests
import os
import logging
from src.scraper import PaperScraper
from src.analyser import PaperAnalyser
from src.obsidian_writer import ObsidianWriter
from src.gardener import KnowledgeGardener
from src.notifier import Notifier
from src.knowledge_base import KnowledgeBase
from src.podcaster import Podcaster
from datetime import datetime, timedelta
from tqdm import tqdm # Import tqdm for progress bars
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', # Simplified format for console
    handlers=[
        logging.FileHandler("paperbrain.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config(path=None):
    if path is None:
        # Default to config.yaml in the same directory as this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "config.yaml")
        
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

import shutil

def download_pdf(url, title, destination_folder=None, retries=3):
    """Downloads PDF to a file with retries and robust headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://arxiv.org/'
    }
    
    # Try different URL formats for arXiv
    urls_to_try = [url]
    if 'arxiv.org/pdf/' in url:
        # Add export.arxiv.org mirror which is often more stable for bots
        arxiv_id = url.split('/')[-1].replace('.pdf', '')
        urls_to_try.append(f"https://export.arxiv.org/pdf/{arxiv_id}.pdf")
        urls_to_try.append(f"https://arxiv.org/pdf/{arxiv_id}")
    
    for attempt in range(retries):
        for target_url in urls_to_try:
            try:
                # logger.info(f"Downloading from {target_url} (Attempt {attempt+1})...")
                response = requests.get(target_url, headers=headers, stream=True, timeout=60) # Increased timeout
                
                if response.status_code == 200:
                    # Sanitize filename - MUST match obsidian_writer logic
                    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()
                    filename = f"{safe_title[:100]}.pdf"
                    
                    if destination_folder:
                        folder = destination_folder
                    else:
                        folder = "temp_pdfs"
                        
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                        
                    filepath = os.path.join(folder, filename)
                    
                    with open(filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    return filepath
                else:
                    logger.warning(f"[WARN] Failed to download from {target_url} (Status: {response.status_code})")
                    
            except Exception as e:
                logger.warning(f"[WARN] Connection error on {target_url}: {e}")
                time.sleep(2) # Backoff
        
        time.sleep(5) # Wait longer between retry sets

    logger.error(f"[ERR] All download attempts failed for {title}")
    return None

def job(target_date=None, provider='doubao'):
    logger.info("Starting Daily PaperBrain Job...")
    
    # Determine target date
    if target_date is None:
        # Default to yesterday
        target_date = datetime.now().date() - timedelta(days=1)
    
    logger.info(f"[INFO] Target Date for search: {target_date}")
    logger.info(f"[INFO] AI Provider: {provider}")
    
    config = load_config()
    
    scraper = PaperScraper(config)
    analyser = PaperAnalyser(config, provider=provider)
    obsidian_writer = ObsidianWriter(config)
    gardener = KnowledgeGardener(config)
    notifier = Notifier(config)
    knowledge_base = KnowledgeBase(config, provider=provider)
    podcaster = Podcaster(config, provider=provider)
    
    # 1. Scrape (pass target_date)
    papers = scraper.get_all_papers(target_date=target_date)
    if not papers:
        logger.info(f"No papers found for date {target_date}.")
        return

    # 2. Screen with Flash
    screened_papers = []
    logger.info(f"[INFO] Starting screening for {len(papers)} papers...")
    
    # Use tqdm for progress bar with ascii=True to prevent mojibake
    for p in tqdm(papers, desc="Screening Papers", unit="paper", ascii=True):
        # logger.info(f"Screening: {p['title']}") # Reduced noise, tqdm handles it
        result = analyser.screen_paper(p)
        p['score'] = result.get('score', 0)
        # Store detailed analysis fields
        p['innovation'] = result.get('innovation', '')
        p['limitations'] = result.get('limitations', '')
        p['reason'] = result.get('reason', '')
        p['tags'] = result.get('tags', [])
        p['short_title'] = result.get('short_title', '')
        screened_papers.append(p)
    
    # Sort by score descending
    screened_papers.sort(key=lambda x: x.get('score', 0), reverse=True)
    logger.info("[INFO] Screening complete. Generating Daily Digest...")
    
    # 3. Write Daily Digest (Keep Obsidian Sync) - pass target_date
    obsidian_writer.write_daily_digest(screened_papers, target_date=target_date)
    
    # 4. Deep Analysis for High Value Papers
    threshold = config['doubao'].get('threshold_score', 8)
    existing_notes = obsidian_writer.scan_existing_notes()
    
    # Dynamic Thresholding: Ensure at least 1 and at most 3 papers are analyzed
    # Filter by initial threshold first
    candidates = [p for p in screened_papers if p.get('score', 0) >= threshold]
    
    if len(candidates) == 0:
        # If no papers meet strict threshold, take the top 1 (if score >= 5 to avoid garbage)
        top_paper = screened_papers[0] if screened_papers else None
        if top_paper and top_paper.get('score', 0) >= 5:
            logger.info(f"[INFO] No papers met threshold {threshold}. Relaxing to analyze top 1 paper (Score: {top_paper['score']}).")
            high_value_papers = [top_paper]
        else:
             high_value_papers = []
    elif len(candidates) > 3:
        # If too many papers, take top 3
        logger.info(f"[INFO] Found {len(candidates)} high-value papers. Limiting to top 3.")
        high_value_papers = candidates[:3]
    else:
        # 1-3 papers found, keep them all
        high_value_papers = candidates
    
    highest_scoring_paper = None
    highest_score = -1
    highest_analysis_content = ""
    highest_rag_context = ""

    if not high_value_papers:
        logger.info("[INFO] No suitable papers found for deep analysis even after relaxing criteria.")
    else:
        logger.info(f"[INFO] Starting Deep Analysis for {len(high_value_papers)} high-value papers...")
        
        for i, p in enumerate(high_value_papers):
            logger.info(f"[{i+1}/{len(high_value_papers)}] Analyzing: {p['title']} (Score: {p['score']})")
            
            if not p.get('pdf_url'):
                logger.warning(f"[WARN] No PDF URL for {p['title']}, skipping.")
                continue
            
            # Context-Aware RAG Retrieval
            logger.info(f"  [STEP] Retrieving Context from Knowledge Base...")
            rag_context = knowledge_base.retrieve_context(p['title'], p['abstract'])
                
            # Download PDF
            logger.info(f"  [STEP] Downloading PDF...")
            pdf_path = download_pdf(p['pdf_url'], p['title'], destination_folder=obsidian_writer.pdf_folder)
            
            if pdf_path:
                # Extract images
                logger.info(f"  [STEP] Extracting Architecture Images...")
                _, img_caption = analyser.extract_images_from_pdf(pdf_path, obsidian_writer.assets_folder)
                
                # Analyze text iteratively (WITH RAG CONTEXT)
                logger.info(f"  [STEP] Performing Deep AI Analysis (This may take a minute)...")
                analysis_text = analyser.analyze_full_paper_iterative(p, pdf_path, existing_notes, rag_context=rag_context)
                
                # Track best paper for podcast
                if p.get('score', 0) > highest_score:
                    highest_score = p.get('score', 0)
                    highest_scoring_paper = p
                    highest_analysis_content = analysis_text
                    highest_rag_context = rag_context

                # Try to extract the Academic Rating from the analysis text
                import re
                rating_match = re.search(r"Academic Rating\*\*:.*?(\d+(?:\.\d+)?)/10", analysis_text, re.IGNORECASE)
                if rating_match:
                    ai_rating = rating_match.group(1)
                    logger.info(f"  [SCORE] AI Academic Rating: {ai_rating}/10")
                
                # Save to Obsidian
                obsidian_writer.write_detailed_note(p, analysis_text, local_pdf_path=pdf_path, image_caption=None)
                
                logger.info(f"  [DONE] Analysis complete and saved.")
            else:
                logger.error(f"  [ERR] Failed to download PDF.")

    # 5. Knowledge Gardening (Backlinking)
    if high_value_papers:
        logger.info("[INFO] Starting Knowledge Gardening (Backlinking)...")
        gardener.prune_and_graft(high_value_papers)
        
        # 6. Notification
        logger.info("[INFO] Sending Notifications...")
        notifier.send_daily_summary(high_value_papers)

    # 7. Generate Podcast for the BEST paper
    if highest_scoring_paper:
        logger.info(f"[INFO] Generating Podcast for Top Paper: {highest_scoring_paper['title']}...")
        podcaster.create_podcast(highest_scoring_paper['title'], highest_analysis_content, highest_rag_context)

    logger.info("[SUCCESS] Job completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaperBrain Daily Job")
    parser.add_argument("--run-now", action="store_true", help="Run the job immediately")
    parser.add_argument("--date", type=str, help="Target date in YYYY-MM-DD format (default: yesterday)")
    parser.add_argument("--provider", type=str, default="doubao", choices=["doubao", "openrouter"], help="AI Provider (default: doubao)")
    
    args = parser.parse_args()
    
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Invalid date format. Please use YYYY-MM-DD.")
            exit(1)
    
    if args.run_now:
        job(target_date, provider=args.provider)
    else:
        config = load_config()
        schedule_time = config['schedule'].get('time', "08:00")
        logger.info(f"Scheduler started. Job set for {schedule_time} daily. Provider: {args.provider}")
        
        # Define a wrapper to always calculate yesterday dynamically
        def scheduled_job():
            job(target_date=None, provider=args.provider) # Will default to yesterday inside job()
            
        schedule.every().day.at(schedule_time).do(scheduled_job)
        
        while True:
            schedule.run_pending()
            time.sleep(60)
