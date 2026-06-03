import yaml
import schedule
import time
import requests
import os
import logging
from src.config_loader import load_config, load_prompts
from src.scraper import PaperScraper
from src.analyser import PaperAnalyser
from src.obsidian_writer import ObsidianWriter
from src.gardener import KnowledgeGardener

from src.knowledge_base import KnowledgeBase
from src.podcaster import Podcaster
from src.research_indexer import ResearchIndexer
from src import scoring as scoring_utils
from src.paper_identity import canonical_arxiv_id, normalize_paper_identity
from src.run_state import RunState
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

# def load_config(path=None): ... REMOVED, imported from src.config_loader

import shutil

def download_pdf(url, title, destination_folder=None, retries=3):
    """Downloads PDF to a file with retries and robust headers."""
    # Security Check: Validate URL scheme and domain whitelist
    if not url.startswith(('http://', 'https://')):
        logger.warning(f"[SECURITY] Skipped unsafe URL scheme: {url}")
        return None
        
    # Optional: strict domain checking (commented out to allow flexibility, but recommended for strict security)
    # trusted_domains = ['arxiv.org', 'huggingface.co', 'aclweb.org', 'openreview.net']
    # if not any(domain in url for domain in trusted_domains):
    #     logger.warning(f"[SECURITY] URL not in trusted domains: {url}")
    #     # return None # Uncomment to enforce

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://arxiv.org/'
    }
    
    urls_to_try = [url]
    if 'arxiv.org/pdf/' in url or 'arxiv.org/abs/' in url:
        arxiv_id = url.split('/')[-1].replace('.pdf', '')
        if arxiv_id:
            base_id = arxiv_id
            if 'v' in arxiv_id and arxiv_id.split('v')[-1].isdigit():
                base_id = arxiv_id.rsplit('v', 1)[0]
            urls_to_try.extend([
                f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                f"https://export.arxiv.org/pdf/{arxiv_id}.pdf",
                f"https://arxiv.org/pdf/{arxiv_id}",
                f"https://arxiv.org/pdf/{base_id}.pdf",
                f"https://export.arxiv.org/pdf/{base_id}.pdf",
                f"https://arxiv.org/pdf/{base_id}",
            ])
    
    seen = set()
    deduped_urls = []
    for u in urls_to_try:
        if u not in seen:
            seen.add(u)
            deduped_urls.append(u)

    for attempt in range(retries):
        for target_url in deduped_urls:
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

def _extract_arxiv_id(raw_url):
    if not raw_url:
        return ""
    value = raw_url.strip().replace(".pdf", "")
    value = value.split("/")[-1]
    value = value.split("?")[0]
    return value

def _quality_priority(p):
    return scoring_utils.quality_priority(p)

def _coarse_priority(p):
    score = float(p.get('coarse_score', p.get('score', 0)) or 0)
    rel = float(p.get('coarse_relevance', p.get('relevance', 0)) or 0)
    evd = float(p.get('coarse_evidence', p.get('evidence', 0)) or 0)
    comp = float(p.get('coarse_method_completeness', 0) or 0)
    should_rescreen = 1 if p.get('should_rescreen', False) else 0
    return (should_rescreen, score, rel, evd, comp)

def _apply_final_screen_result(paper, result):
    paper['score'] = _safe_float(result.get('score', 0), 0.0)
    paper['innovation'] = result.get('innovation', '')
    paper['limitations'] = result.get('limitations', '')
    paper['reason'] = result.get('reason', '')
    paper['tags'] = result.get('tags', [])
    paper['short_title'] = result.get('short_title', '')
    paper['relevance'] = _safe_float(result.get('relevance', 0), 0.0)
    paper['novelty'] = _safe_float(result.get('novelty', 0), 0.0)
    paper['rigor'] = _safe_float(result.get('rigor', 0), 0.0)
    paper['evidence'] = _safe_float(result.get('evidence', 0), 0.0)
    paper['reproducibility'] = _safe_float(result.get('reproducibility', 0), 0.0)
    paper['confidence'] = _safe_float(result.get('confidence', 0), 0.0)
    paper['red_flags'] = result.get('red_flags', [])
    paper['screening_stage'] = result.get('screening_stage', '')
    paper['screening_model'] = result.get('used_model', '')

def _apply_coarse_screen_result(paper, result):
    paper['coarse_score'] = _safe_float(result.get('coarse_score', result.get('score', 0)), 0.0)
    paper['coarse_relevance'] = _safe_float(result.get('relevance', 0), 0.0)
    paper['coarse_evidence'] = _safe_float(result.get('evidence', 0), 0.0)
    paper['coarse_method_completeness'] = _safe_float(result.get('method_completeness', 0), 0.0)
    paper['should_rescreen'] = bool(result.get('should_rescreen', False))
    paper['coarse_reason'] = result.get('reason', '')
    paper['coarse_model'] = result.get('used_model', '')
    if not paper.get('short_title'):
        paper['short_title'] = result.get('short_title', '')

def _apply_coarse_as_final_result(paper):
    score = min(round(float(paper.get('coarse_score', 0) or 0), 1), 6.4)
    paper['score'] = score
    paper['innovation'] = paper.get('coarse_reason', '') or "Filtered out by coarse screening."
    paper['limitations'] = "Not promoted to rigorous re-screening."
    paper['reason'] = paper.get('coarse_reason', '')
    paper['tags'] = paper.get('tags', [])
    paper['relevance'] = round(float(paper.get('coarse_relevance', 0) or 0), 1)
    paper['novelty'] = 0
    paper['rigor'] = round(float(paper.get('coarse_method_completeness', 0) or 0), 1)
    paper['evidence'] = round(float(paper.get('coarse_evidence', 0) or 0), 1)
    paper['reproducibility'] = 0
    paper['confidence'] = 0
    paper['red_flags'] = []
    paper['screening_stage'] = 'coarse_only'
    paper['screening_model'] = paper.get('coarse_model', '')

def _safe_int(value, default):
    try:
        return int(value)
    except Exception:
        return default

def _safe_float(value, default):
    try:
        return round(float(value), 1)
    except Exception:
        return default

def _passes_quality_gate(paper, gate):
    return scoring_utils.passes_quality_gate(paper, gate)

def _mark_digest_membership(papers, config):
    min_score = float(config.get('analysis', {}).get('daily_digest_min_score', 7.0))
    for paper in papers:
        paper['in_daily_digest'] = float(paper.get('score', 0) or 0) >= min_score

def _mark_deep_selection(papers, high_value_papers):
    selected_keys = {p.get('paper_id') for p in high_value_papers if p.get('paper_id')}
    selected_keys.update({p.get('title') for p in high_value_papers if p.get('title')})
    for paper in papers:
        paper['selected_for_deep_analysis'] = (
            (paper.get('paper_id') and paper.get('paper_id') in selected_keys)
            or paper.get('title') in selected_keys
        )

def job(
    target_date=None,
    provider='doubao',
    generate_podcast=True,
    podcast_minutes=5,
    arxiv_url=None,
    resume=True,
    force=False,
    stop_after=None,
):
    logger.info("Starting Daily PaperBrain Job...")

    # Determine target date
    if target_date is None:
        target_date = datetime.now().date() - timedelta(days=1)

    logger.info(f"[INFO] Target Date for search: {target_date}")
    logger.info(f"[INFO] AI Provider: {provider}")
    logger.info(f"[INFO] Podcast Generation: {'Enabled' if generate_podcast else 'Disabled'}")
    logger.info(f"[INFO] Podcast Duration: ~{podcast_minutes} minutes")
    if arxiv_url:
        logger.info(f"[INFO] Single-paper mode enabled for: {arxiv_url}")

    config = load_config()
    prompts = load_prompts()
    run_state = RunState(config, target_date, provider, single_paper=bool(arxiv_url))
    if force:
        logger.info("[INFO] Force mode enabled: resetting run state.")
        run_state.reset()

    scraper = PaperScraper(config)
    analyser = PaperAnalyser(config, provider=provider, prompts=prompts)
    obsidian_writer = ObsidianWriter(config, provider=provider)
    gardener = KnowledgeGardener(config, provider=provider)
    knowledge_base = KnowledgeBase(config, provider=provider, prompts=prompts)
    podcaster = Podcaster(config, provider=provider, prompts=prompts)
    research_indexer = ResearchIndexer(config)
    
    if resume and not force and run_state.data.get("stage") in (
        "fetched",
        "coarse_screened",
        "screened",
        "digest_written",
        "deep_analyzed",
        "completed",
    ):
        papers = run_state.papers()
        logger.info(f"[RESUME] Loaded {len(papers)} papers from {run_state.path}")
    elif arxiv_url:
        single_paper = scraper.fetch_single_arxiv_paper(arxiv_url)
        papers = [single_paper] if single_paper else []
    else:
        papers = scraper.get_all_papers(target_date=target_date)
    papers = [normalize_paper_identity(p) for p in papers if p]
    if not papers:
        logger.info(f"No papers found for date {target_date}.")
        return
    if run_state.data.get("stage") == "initialized" or not resume or force:
        run_state.set_papers(papers, stage="fetched")
    if stop_after == "fetch":
        logger.info("[STOP] stop_after=fetch")
        return

    # 2. Two-stage screening
    screened_papers = run_state.papers() if resume and run_state.data.get("stage") in (
        "coarse_screened",
        "screened",
        "digest_written",
        "deep_analyzed",
        "completed",
    ) else []

    if screened_papers:
        logger.info(f"[RESUME] Using cached coarse-screened papers: {len(screened_papers)}")
    else:
        logger.info(f"[INFO] Starting stage-1 coarse screening for {len(papers)} papers with {analyser.model_flash}...")
        for p in tqdm(papers, desc="Coarse Screening", unit="paper", ascii=True):
            coarse_result = analyser.coarse_screen_paper(p)
            _apply_coarse_screen_result(p, coarse_result)
            p = normalize_paper_identity(p)
            screened_papers.append(p)
            run_state.update_paper(p)
        run_state.mark_stage("coarse_screened")
    if stop_after == "coarse":
        logger.info("[STOP] stop_after=coarse")
        return

    analysis_cfg = config.get('analysis', {})
    stage2_min_k = int(analysis_cfg.get('screening_second_stage_top_k', 10))
    stage2_ratio = float(analysis_cfg.get('screening_second_stage_ratio', 0.25))
    stage2_max_k = int(analysis_cfg.get('screening_second_stage_max_k', 20))
    stage2_top_k = scoring_utils.dynamic_stage2_top_k(
        len(screened_papers),
        min_k=stage2_min_k,
        ratio=stage2_ratio,
        max_k=stage2_max_k,
    )
    rescreen_true = sorted([p for p in screened_papers if p.get('should_rescreen')], key=_coarse_priority, reverse=True)
    rescreen_false = sorted([p for p in screened_papers if not p.get('should_rescreen')], key=_coarse_priority, reverse=True)
    rescreen_pool = rescreen_true[:stage2_top_k]
    if len(rescreen_pool) < stage2_top_k:
        rescreen_pool.extend(rescreen_false[:stage2_top_k - len(rescreen_pool)])
    rescreen_ids = {id(p) for p in rescreen_pool}

    logger.info(
        f"[INFO] Stage-1 complete. Promoting {len(rescreen_pool)} papers to stage-2 rigorous screening "
        f"with {analyser.model_screening_pro}."
    )

    use_pdf_context = bool(analysis_cfg.get('screening_second_stage_use_pdf_context', True))
    pdf_context_pages = max(1, _safe_int(analysis_cfg.get('screening_second_stage_pdf_context_pages', 3), 3))
    pdf_context_max_chars = max(500, _safe_int(analysis_cfg.get('screening_second_stage_pdf_context_max_chars', 5000), 5000))

    for p in screened_papers:
        if id(p) not in rescreen_ids:
            _apply_coarse_as_final_result(p)

    if resume and run_state.data.get("stage") in ("screened", "digest_written", "deep_analyzed", "completed"):
        logger.info(f"[RESUME] Using cached rigorous screening results: {len(screened_papers)}")
    else:
        for p in tqdm(rescreen_pool, desc="Rigorous Re-Screen", unit="paper", ascii=True):
            if use_pdf_context:
                p.pop('screening_document_excerpt', None)
                if p.get('pdf_url'):
                    logger.info(f"  [CTX] Building stage-2 document excerpt: {p['title']}")
                    tmp_pdf_path = download_pdf(p['pdf_url'], p['title'], destination_folder="temp_pdfs")
                    if tmp_pdf_path:
                        try:
                            excerpt_text = analyser._extract_text_from_pdf_fitz(tmp_pdf_path, max_pages=pdf_context_pages)
                            if not excerpt_text:
                                excerpt_text = analyser.extract_text_from_pdf(tmp_pdf_path)
                            excerpt_text = (excerpt_text or "").strip()
                            if excerpt_text:
                                p['screening_document_excerpt'] = excerpt_text[:pdf_context_max_chars]
                        except Exception as e:
                            logger.warning(f"[WARN] Failed to prepare stage-2 document excerpt for '{p['title']}': {e}")
                        finally:
                            try:
                                os.remove(tmp_pdf_path)
                            except Exception:
                                pass

            result = analyser.screen_paper(p)
            _apply_final_screen_result(p, result)
            p = normalize_paper_identity(p)
            run_state.update_paper(p)
        run_state.mark_stage("screened")

    if stop_after == "screen":
        logger.info("[STOP] stop_after=screen")
        return

    for p in screened_papers:
        p.pop('screening_document_excerpt', None)

    # Clean up temp PDFs after screening
    if os.path.exists("temp_pdfs"):
        try:
            shutil.rmtree("temp_pdfs", ignore_errors=True)
            logger.info("[INFO] Cleaned up temporary PDF files from screening stage.")
        except Exception as e:
            logger.warning(f"[WARN] Failed to clean temp_pdfs: {e}")

    # Sort by score descending
    screened_papers.sort(key=lambda x: x.get('score', 0), reverse=True)
    logger.info("[INFO] Screening complete. Generating Daily Digest...")
    
    # 3. Deep Analysis for High Value Papers
    provider_cfg = config.get(provider, config.get('doubao', {}))
    threshold = float(analysis_cfg.get(
        'deep_analysis_lower_threshold',
        provider_cfg.get('threshold_score', config.get('doubao', {}).get('threshold_score', 8))
    ))
    existing_notes = obsidian_writer.scan_existing_notes()
    high_value_papers, selection_info = scoring_utils.select_deep_analysis_papers(
        screened_papers,
        analysis_cfg=analysis_cfg,
        provider_threshold=threshold,
    )
    _mark_deep_selection(screened_papers, high_value_papers)
    _mark_digest_membership(screened_papers, config)
    run_state.set_papers(screened_papers, stage="screened")
    run_state.update_selection(deep_analysis=selection_info)
    screening_report = run_state.write_screening_report()
    logger.info(f"[INFO] Full screening report written to {screening_report}")

    if not high_value_papers:
        logger.info(
            f"[INFO] No papers passed deep-analysis threshold. "
            f"lower_threshold={selection_info['lower_threshold']}, "
            f"extra_threshold={selection_info['extra_threshold']}, "
            f"quality_passed={selection_info['quality_passed_count']}/{selection_info['candidate_count']}"
        )
    else:
        logger.info(
            f"[INFO] Deep-analysis selection: base={selection_info['base_count']}, "
            f"extra_above_{selection_info['extra_threshold']}={selection_info['extra_count']}, "
            f"total={selection_info['selected_count']}."
        )
    
    highest_scoring_paper = None
    highest_score = -1
    highest_analysis_content = ""
    highest_rag_context = ""

    if not high_value_papers:
        logger.info("[INFO] No suitable papers found for deep analysis even after relaxing criteria.")
    elif resume and run_state.data.get("stage") in ("deep_analyzed", "completed"):
        logger.info("[RESUME] Deep analysis already completed in run state.")
    else:
        logger.info(f"[INFO] Starting Deep Analysis for {len(high_value_papers)} high-value papers...")
        
        for i, p in enumerate(high_value_papers):
            logger.info(f"[{i+1}/{len(high_value_papers)}] Analyzing: {p['title']} (Score: {p['score']})")
            
            if not p.get('pdf_url'):
                logger.warning(f"[WARN] No PDF URL for {p['title']}, skipping.")
                continue
            
            # Download PDF
            logger.info(f"  [STEP] Downloading PDF...")
            pdf_path = download_pdf(p['pdf_url'], p['title'], destination_folder=obsidian_writer.pdf_folder)
            if (not pdf_path) and p.get('url'):
                alt_url = p['url']
                if '/abs/' in alt_url:
                    alt_url = alt_url.replace('/abs/', '/pdf/')
                id_main = canonical_arxiv_id(p.get('pdf_url', ''))
                id_alt = canonical_arxiv_id(alt_url)
                if id_main != id_alt:
                    pdf_path = download_pdf(alt_url, p['title'], destination_folder=obsidian_writer.pdf_folder)
            
            if pdf_path:
                # Context-Aware RAG Retrieval (only after PDF is available to avoid unnecessary token usage)
                logger.info(f"  [STEP] Retrieving Context from Knowledge Base...")
                rag_context = knowledge_base.retrieve_context(p['title'], p['abstract'])

                # Extract images
                logger.info(f"  [STEP] Extracting Architecture Images...")
                _, img_caption = analyser.extract_images_from_pdf(pdf_path, obsidian_writer.assets_folder)
                
                # Analyze text iteratively (WITH RAG CONTEXT)
                logger.info(f"  [STEP] Performing Deep AI Analysis (This may take a minute)...")
                analysis_text = analyser.analyze_full_paper_iterative(p, pdf_path, existing_notes, rag_context=rag_context)

                # Generate AI aliases for gardener matching
                logger.info(f"  [STEP] Generating paper aliases...")
                ai_aliases = analyser.generate_paper_aliases(p, analysis_text)
                if ai_aliases:
                    p['ai_aliases'] = ai_aliases
                    logger.info(f"  [ALIASES] Generated {len(ai_aliases)} aliases: {ai_aliases[:5]}")
                
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
                note_path = obsidian_writer.write_detailed_note(p, analysis_text, local_pdf_path=pdf_path, image_caption=None)
                p["note_path"] = note_path
                run_state.update_paper(p)
                research_indexer.update_after_new_note(note_path)
                
                logger.info(f"  [DONE] Analysis complete and saved.")
            else:
                logger.error(f"  [ERR] PDF unavailable for '{p['title']}'. Skipping deep analysis to avoid extra token cost.")
        run_state.mark_stage("deep_analyzed")

    if stop_after == "deep":
        logger.info("[STOP] stop_after=deep")
        return

    # 4. Write Daily Digest — skip in single-paper mode (arxiv_url provided)
    if not arxiv_url:
        digest_path = obsidian_writer.write_daily_digest(screened_papers, target_date=target_date)
        run_state.update_artifacts(daily_digest=digest_path)
        run_state.mark_stage("digest_written")
    else:
        single_digest_path = None
        for paper in high_value_papers or screened_papers:
            single_digest_path = obsidian_writer.upsert_single_paper_digest_entry(paper)
        if single_digest_path:
            run_state.update_artifacts(daily_digest=single_digest_path)
        logger.info("[INFO] Single-paper mode: daily digest checked/updated.")

    # 5. Knowledge Gardening (Backlinking)
    if high_value_papers:
        logger.info("[INFO] Starting Knowledge Gardening (Backlinking)...")
        gardener.prune_and_graft(high_value_papers)
        research_indexer.build(update_notes=True)

    # 6. Generate Podcast for the BEST paper
    if generate_podcast and highest_scoring_paper:
        logger.info(f"[INFO] Generating Podcast for Top Paper: {highest_scoring_paper['title']}...")
        audio_path = podcaster.create_podcast(
            highest_scoring_paper['title'],
            highest_analysis_content,
            highest_rag_context,
            duration_minutes=podcast_minutes
        )
        run_state.update_artifacts(podcast=audio_path)

    run_state.mark_stage("completed")
    logger.info("[SUCCESS] Job completed successfully.")
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PaperBrain Daily Job")
    parser.add_argument("--run-now", action="store_true", help="Run the job immediately")
    parser.add_argument("--date", type=str, help="Target date in YYYY-MM-DD format (default: yesterday)")
    parser.add_argument("--provider", type=str, default="doubao", choices=["doubao", "openrouter"], help="AI Provider (default: doubao)")
    parser.add_argument("--no-podcast", action="store_true", help="Disable podcast generation")
    parser.add_argument("--podcast-minutes", type=int, default=5, help="Target podcast duration in minutes (default: 5)")
    parser.add_argument("--arxiv-url", type=str, help="Analyze a specific arXiv URL or ID directly")
    parser.add_argument("--force", action="store_true", help="Reset saved run state and recompute all stages")
    parser.add_argument("--no-resume", action="store_true", help="Ignore saved run state without deleting it")
    parser.add_argument(
        "--stop-after",
        choices=["fetch", "coarse", "screen", "deep"],
        help="Stop after a pipeline stage; useful for checkpointed runs",
    )
    
    args = parser.parse_args()
    
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Invalid date format. Please use YYYY-MM-DD.")
            exit(1)
            
    generate_podcast = not args.no_podcast
    podcast_minutes = max(1, args.podcast_minutes)
    
    if args.run_now:
        job(
            target_date,
            provider=args.provider,
            generate_podcast=generate_podcast,
            podcast_minutes=podcast_minutes,
            arxiv_url=args.arxiv_url,
            resume=not args.no_resume,
            force=args.force,
            stop_after=args.stop_after,
        )
    else:
        config = load_config()
        schedule_time = config['schedule'].get('time', "08:00")
        logger.info(f"Scheduler started. Job set for {schedule_time} daily. Provider: {args.provider}. Podcast: {'Enabled' if generate_podcast else 'Disabled'}. Duration: ~{podcast_minutes} minutes")
        
        # Define a wrapper to always calculate yesterday dynamically
        def scheduled_job():
            job(target_date=None, provider=args.provider, generate_podcast=generate_podcast, podcast_minutes=podcast_minutes) # Will default to yesterday inside job()
            
        schedule.every().day.at(schedule_time).do(scheduled_job)
        
        while True:
            schedule.run_pending()
            time.sleep(60)
