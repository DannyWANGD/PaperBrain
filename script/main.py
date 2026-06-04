import yaml
import time
import requests
import os
import logging
from src.config_loader import load_config, load_prompts
from src import scoring as scoring_utils
from src.paper_identity import canonical_arxiv_id, normalize_paper_identity
from src.run_state import RunState
from datetime import datetime, timedelta
from tqdm import tqdm # Import tqdm for progress bars
import argparse
import json

try:
    import schedule
except ImportError:
    schedule = None

SAVED_PAPER_STAGES = (
    "fetched",
    "coarse_screened",
    "screened",
    "digest_written",
    "deep_analyzed",
    "completed",
)
COARSE_READY_STAGES = (
    "coarse_screened",
    "screened",
    "digest_written",
    "deep_analyzed",
    "completed",
)
SCREENED_READY_STAGES = ("screened", "digest_written", "deep_analyzed", "completed")
DEEP_READY_STAGES = ("deep_analyzed", "completed")

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

PDF_RATE_LIMIT_COOLDOWN_MINUTES = 60
PDF_CACHE_DIR = os.path.join("Cache", "pdfs")
PDF_COOLDOWN_PATH = os.path.join(PDF_CACHE_DIR, "arxiv_pdf_cooldown.json")

def _safe_pdf_filename(title):
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c == ' ']).strip()
    return f"{safe_title[:100]}.pdf"

def _looks_like_pdf_url(url):
    value = str(url or "").strip()
    if not value:
        return False
    lowered = value.split("?", 1)[0].split("#", 1)[0].lower()
    return lowered.endswith(".pdf") or lowered.endswith("/pdf") or "/pdf/" in lowered

def _is_usable_local_pdf(path):
    if not path or not os.path.exists(path):
        return False
    try:
        if os.path.getsize(path) <= 1024:
            return False
        with open(path, "rb") as f:
            header = f.read(1024)
        return b"%PDF-" in header
    except Exception:
        return False

def _pdf_cooldown_remaining_seconds():
    if not os.path.exists(PDF_COOLDOWN_PATH):
        return 0.0
    try:
        with open(PDF_COOLDOWN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return max(0.0, float(data.get("until", 0)) - time.time())
    except Exception:
        return 0.0

def _mark_pdf_cooldown(reason):
    os.makedirs(PDF_CACHE_DIR, exist_ok=True)
    try:
        with open(PDF_COOLDOWN_PATH, "w", encoding="utf-8") as f:
            json.dump(
                {"until": time.time() + PDF_RATE_LIMIT_COOLDOWN_MINUTES * 60, "reason": reason, "created_at": datetime.now().isoformat()},
                f,
                indent=2,
            )
    except Exception:
        pass

def _record_pdf_cache_path(path, cache_paths):
    if cache_paths is not None and path:
        cache_paths.add(os.path.abspath(path))

def _is_pdf_cache_file(path):
    if not path:
        return False
    try:
        cache_root = os.path.abspath(PDF_CACHE_DIR)
        target = os.path.abspath(path)
        return (
            os.path.commonpath([cache_root, target]) == cache_root
            and os.path.isfile(target)
            and target.lower().endswith(".pdf")
        )
    except Exception:
        return False

def _cleanup_completed_run_pdf_cache(day_start_ts, cache_paths=None):
    """Remove PDF cache files after a full successful run, preserving metadata/cooldown files."""
    if not os.path.isdir(PDF_CACHE_DIR):
        return 0

    candidates = set(cache_paths or [])
    try:
        for name in os.listdir(PDF_CACHE_DIR):
            path = os.path.join(PDF_CACHE_DIR, name)
            if _is_pdf_cache_file(path) and os.path.getmtime(path) >= day_start_ts:
                candidates.add(os.path.abspath(path))
    except Exception as e:
        logger.warning(f"[WARN] Failed to scan PDF cache for cleanup: {e}")

    removed = 0
    for path in sorted(candidates):
        if not _is_pdf_cache_file(path):
            continue
        try:
            os.remove(path)
            removed += 1
        except Exception as e:
            logger.warning(f"[WARN] Failed to remove cached PDF {path}: {e}")

    if removed:
        logger.info(f"[INFO] Removed {removed} completed-run cached PDF(s) from {PDF_CACHE_DIR}.")
    return removed

def _copy_pdf(src, dest_folder, filename):
    os.makedirs(dest_folder, exist_ok=True)
    dest = os.path.join(dest_folder, filename)
    if os.path.abspath(src) != os.path.abspath(dest):
        shutil.copy2(src, dest)
    return dest

def download_pdf(url, title, destination_folder=None, retries=3, cache_paths=None):
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

    folder = destination_folder or "temp_pdfs"
    filename = _safe_pdf_filename(title)
    direct_path = os.path.join(folder, filename)
    if _is_usable_local_pdf(direct_path):
        logger.info(f"  [CACHE] Reusing existing PDF: {direct_path}")
        return direct_path

    arxiv_id_for_cache = canonical_arxiv_id(url)
    if arxiv_id_for_cache:
        cache_path = os.path.join(PDF_CACHE_DIR, f"{arxiv_id_for_cache}.pdf")
        if _is_usable_local_pdf(cache_path):
            logger.info(f"  [CACHE] Reusing cached PDF for arXiv:{arxiv_id_for_cache}")
            _record_pdf_cache_path(cache_path, cache_paths)
            return _copy_pdf(cache_path, folder, filename)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://arxiv.org/'
    }
    
    urls_to_try = [url]
    arxiv_id = canonical_arxiv_id(url)
    if arxiv_id:
        urls_to_try.extend([
            f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            f"https://export.arxiv.org/pdf/{arxiv_id}.pdf",
            f"https://arxiv.org/pdf/{arxiv_id}",
            f"https://export.arxiv.org/pdf/{arxiv_id}",
        ])
    
    seen = set()
    deduped_urls = []
    for u in urls_to_try:
        if u not in seen:
            seen.add(u)
            deduped_urls.append(u)

    if arxiv_id_for_cache:
        cooldown_remaining = _pdf_cooldown_remaining_seconds()
        if cooldown_remaining > 0:
            logger.warning(
                f"[WARN] arXiv PDF downloads are in local cooldown for {cooldown_remaining / 60:.1f} more minutes. "
                f"Skipping network PDF download for {title}."
            )
            return None

    arxiv_429_url = ""
    for attempt in range(retries):
        for target_url in deduped_urls:
            try:
                # logger.info(f"Downloading from {target_url} (Attempt {attempt+1})...")
                response = requests.get(target_url, headers=headers, stream=True, timeout=60) # Increased timeout
                
                if response.status_code == 200:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                        
                    filepath = os.path.join(folder, filename)
                    
                    with open(filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                    if not _is_usable_local_pdf(filepath):
                        logger.warning(f"[WARN] Downloaded file from {target_url} is not a usable PDF.")
                        try:
                            os.remove(filepath)
                        except Exception:
                            pass
                        continue

                    if arxiv_id_for_cache:
                        os.makedirs(PDF_CACHE_DIR, exist_ok=True)
                        cache_path = os.path.join(PDF_CACHE_DIR, f"{arxiv_id_for_cache}.pdf")
                        shutil.copy2(filepath, cache_path)
                        _record_pdf_cache_path(cache_path, cache_paths)
                    
                    return filepath
                else:
                    logger.warning(f"[WARN] Failed to download from {target_url} (Status: {response.status_code})")
                    if response.status_code == 429 and canonical_arxiv_id(target_url):
                        arxiv_429_url = target_url
                        continue
                    
            except Exception as e:
                logger.warning(f"[WARN] Connection error on {target_url}: {e}")
                time.sleep(2) # Backoff

        if arxiv_429_url:
            _mark_pdf_cooldown(f"HTTP 429 while downloading {arxiv_429_url}")
            logger.warning("[WARN] arXiv PDF endpoint is rate-limited after trying PDF URL variants. Stopping arXiv PDF retries for now.")
            return None
        
        time.sleep(5) # Wait longer between retry sets

    logger.error(f"[ERR] All download attempts failed for {title}")
    return None

def _paper_pdf_url_candidates(paper):
    urls = []
    pdf_url = str(paper.get("pdf_url") or "").strip()
    if pdf_url:
        urls.append(pdf_url)

    page_or_pdf_url = str(paper.get("url") or "").strip()
    if page_or_pdf_url and _looks_like_pdf_url(page_or_pdf_url):
        urls.append(page_or_pdf_url)

    arxiv_id = ""
    for key in ("pdf_url", "url", "arxiv_id", "paper_id"):
        arxiv_id = canonical_arxiv_id(paper.get(key))
        if arxiv_id:
            break
    if arxiv_id:
        urls.extend([
            f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            f"https://export.arxiv.org/pdf/{arxiv_id}.pdf",
            f"https://arxiv.org/pdf/{arxiv_id}",
            f"https://export.arxiv.org/pdf/{arxiv_id}",
        ])

    deduped = []
    seen = set()
    for url in urls:
        if url and url not in seen:
            seen.add(url)
            deduped.append(url)
    return deduped

def download_paper_pdf(paper, destination_folder, cache_paths=None):
    """Download a paper PDF locally before any PDF-dependent analysis."""
    title = paper.get("title") or paper.get("short_title") or "paper"
    for url in _paper_pdf_url_candidates(paper):
        pdf_path = download_pdf(url, title, destination_folder=destination_folder, cache_paths=cache_paths)
        if _is_usable_local_pdf(pdf_path):
            return pdf_path
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

def _load_papers_for_run(scraper, run_state, target_date, arxiv_url, resume=True, force=False):
    if resume and not force and run_state.data.get("stage") in SAVED_PAPER_STAGES:
        papers = run_state.papers()
        logger.info(f"[RESUME] Loaded {len(papers)} papers from {run_state.path}")
    elif arxiv_url:
        single_paper = scraper.fetch_single_arxiv_paper(arxiv_url)
        papers = [single_paper] if single_paper else []
    else:
        papers = scraper.get_all_papers(target_date=target_date)

    papers = [normalize_paper_identity(p) for p in papers if p]
    if papers and (run_state.data.get("stage") == "initialized" or not resume or force):
        run_state.set_papers(papers, stage="fetched")
    return papers

def _run_coarse_screening(papers, analyser, run_state, resume=True):
    screened_papers = run_state.papers() if resume and run_state.data.get("stage") in COARSE_READY_STAGES else []
    if screened_papers:
        logger.info(f"[RESUME] Using cached coarse-screened papers: {len(screened_papers)}")
        return screened_papers

    logger.info(f"[INFO] Starting stage-1 coarse screening for {len(papers)} papers with {analyser.model_flash}...")
    for p in tqdm(papers, desc="Coarse Screening", unit="paper", ascii=True):
        coarse_result = analyser.coarse_screen_paper(p)
        _apply_coarse_screen_result(p, coarse_result)
        p = normalize_paper_identity(p)
        screened_papers.append(p)
        run_state.update_paper(p)
    run_state.mark_stage("coarse_screened")
    return screened_papers

def _build_rescreen_pool(screened_papers, analysis_cfg):
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
    return rescreen_pool

def _run_rigorous_screening(screened_papers, rescreen_pool, analyser, run_state, analysis_cfg, resume=True, cache_paths=None):
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

    if resume and run_state.data.get("stage") in SCREENED_READY_STAGES:
        logger.info(f"[RESUME] Using cached rigorous screening results: {len(screened_papers)}")
        return

    for p in tqdm(rescreen_pool, desc="Rigorous Re-Screen", unit="paper", ascii=True):
        if use_pdf_context:
            p.pop('screening_document_excerpt', None)
            if _paper_pdf_url_candidates(p):
                logger.info(f"  [CTX] Building stage-2 document excerpt: {p['title']}")
                tmp_pdf_path = download_paper_pdf(p, destination_folder="temp_pdfs", cache_paths=cache_paths)
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
                else:
                    logger.info("  [CTX] PDF unavailable or rate-limited; rigorous screening will use title/abstract only.")

        result = analyser.screen_paper(p)
        _apply_final_screen_result(p, result)
        p = normalize_paper_identity(p)
        run_state.update_paper(p)
    run_state.mark_stage("screened")

def _drop_screening_excerpts(papers):
    for p in papers:
        p.pop('screening_document_excerpt', None)

def _cleanup_temp_pdfs():
    if os.path.exists("temp_pdfs"):
        try:
            shutil.rmtree("temp_pdfs", ignore_errors=True)
            logger.info("[INFO] Cleaned up temporary PDF files from screening stage.")
        except Exception as e:
            logger.warning(f"[WARN] Failed to clean temp_pdfs: {e}")

def _select_and_record_deep_analysis(screened_papers, config, provider, analysis_cfg, obsidian_writer, run_state):
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
    return high_value_papers, selection_info, existing_notes

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
    run_pdf_cache_paths = set()
    cache_cleanup_day_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()

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
    from src.scraper import PaperScraper
    from src.analyser import PaperAnalyser
    from src.obsidian_writer import ObsidianWriter
    from src.gardener import KnowledgeGardener
    from src.knowledge_base import KnowledgeBase
    from src.podcaster import Podcaster
    from src.research_indexer import ResearchIndexer

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
    
    papers = _load_papers_for_run(
        scraper,
        run_state,
        target_date,
        arxiv_url,
        resume=resume,
        force=force,
    )
    if not papers:
        logger.info(f"No papers found for date {target_date}.")
        return
    if stop_after == "fetch":
        logger.info("[STOP] stop_after=fetch")
        return

    # 2. Two-stage screening
    screened_papers = _run_coarse_screening(papers, analyser, run_state, resume=resume)
    if stop_after == "coarse":
        logger.info("[STOP] stop_after=coarse")
        return

    analysis_cfg = config.get('analysis', {})
    rescreen_pool = _build_rescreen_pool(screened_papers, analysis_cfg)
    _run_rigorous_screening(
        screened_papers,
        rescreen_pool,
        analyser,
        run_state,
        analysis_cfg,
        resume=resume,
        cache_paths=run_pdf_cache_paths,
    )

    if stop_after == "screen":
        logger.info("[STOP] stop_after=screen")
        return

    _drop_screening_excerpts(screened_papers)

    # Clean up temp PDFs after screening
    _cleanup_temp_pdfs()

    # Sort by score descending
    screened_papers.sort(key=lambda x: x.get('score', 0), reverse=True)
    logger.info("[INFO] Screening complete. Generating Daily Digest...")
    
    # 3. Deep Analysis for High Value Papers
    high_value_papers, selection_info, existing_notes = _select_and_record_deep_analysis(
        screened_papers,
        config,
        provider,
        analysis_cfg,
        obsidian_writer,
        run_state,
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
            
            if not _paper_pdf_url_candidates(p):
                logger.warning(f"[WARN] No PDF URL for {p['title']}, skipping.")
                continue
            
            # Download PDF
            logger.info(f"  [STEP] Downloading PDF...")
            pdf_path = download_paper_pdf(p, destination_folder=obsidian_writer.pdf_folder, cache_paths=run_pdf_cache_paths)
            
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
    _cleanup_completed_run_pdf_cache(cache_cleanup_day_start, run_pdf_cache_paths)
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
        if schedule is None:
            logger.error("The 'schedule' package is required for scheduled mode. Install dependencies or use --run-now.")
            exit(1)
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
