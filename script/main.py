import yaml
import time
import requests
import os
import logging
from copy import deepcopy
from src.config_loader import load_config, load_prompts
from src import scoring as scoring_utils
from src import run_control
from src.paper_identity import canonical_arxiv_id, identity_key, normalize_paper_identity
from src.paths import PaperBrainPaths
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

DEFAULT_PATHS = PaperBrainPaths.default()
os.makedirs(DEFAULT_PATHS.logs_dir, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', # Simplified format for console
    handlers=[
        logging.FileHandler(DEFAULT_PATHS.log_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# def load_config(path=None): ... REMOVED, imported from src.config_loader

import shutil

PDF_RATE_LIMIT_COOLDOWN_MINUTES = 60
PDF_CACHE_DIR = str(DEFAULT_PATHS.pdf_cache_dir)
PDF_COOLDOWN_PATH = str(DEFAULT_PATHS.pdf_cooldown_path)
TEMP_PDF_DIR = str(DEFAULT_PATHS.temp_pdf_dir)

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

    folder = destination_folder or TEMP_PDF_DIR
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

def _maybe_cancel(cancel_check):
    if cancel_check:
        cancel_check()

DEEP_PRESERVE_SIGNALS = (
    "selected_for_deep_analysis",
    "forced_deep",
    "manual_requested_at",
    "manual_deep_completed_at",
    "preserved_deep",
)
PRESERVED_DEEP_LIST_FIELDS = ("authors", "tags", "red_flags", "ai_aliases", "institutions", "paper_sources", "provider_sources")
PRESERVED_DEEP_METADATA_FIELDS = (
    "note_path",
    "pdf_path",
    "local_pdf_path",
    "manual_requested_at",
    "manual_screened_at",
    "manual_deep_supplement_date",
    "manual_deep_completed_at",
    "deep_analysis_completed",
    "preserved_deep",
    "preserved_deep_at",
    "forced_deep",
    "forced_digest",
    "selected_for_deep_analysis",
    "in_daily_digest",
)

def _now_iso():
    return datetime.now().isoformat(timespec="seconds")

def _as_clean_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        items = value
    else:
        items = [value]
    return [item for item in items if item is not None and str(item).strip()]

def _merge_unique_values(*values):
    merged = []
    seen = set()
    for value in values:
        for item in _as_clean_list(value):
            key = str(item).strip().lower()
            if key and key not in seen:
                seen.add(key)
                merged.append(item)
    return merged

def _digest_force_signal(paper):
    return bool(
        paper.get("forced_deep")
        or paper.get("forced_digest")
        or paper.get("manual_requested_at")
        or paper.get("preserved_deep")
    )

def _deep_preservation_signal(paper):
    return any(bool(paper.get(key)) for key in DEEP_PRESERVE_SIGNALS)

def _existing_file(path):
    if not path:
        return ""
    try:
        return os.path.abspath(path) if os.path.isfile(path) else ""
    except Exception:
        return ""

def _note_path_candidates(raw_path, paths):
    value = str(raw_path or "").strip().strip('"')
    if not value:
        return []
    candidates = []
    if os.path.isabs(value):
        candidates.append(value)
    else:
        candidates.extend([
            value,
            os.path.join(os.getcwd(), value),
            os.path.join(str(paths.repo_root), value),
            os.path.join(str(paths.vault_path), value),
            os.path.join(str(paths.notes_dir), value),
        ])
        if not value.lower().endswith(".md"):
            candidates.append(os.path.join(str(paths.notes_dir), f"{value}.md"))
    return candidates

def _date_key_from_value(value):
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, str) and len(value) >= 10:
        return value[:10]
    return ""

def _index_note_matches_paper(note, paper):
    note_paper = normalize_paper_identity({
        "paper_id": note.get("paper_id") or (note.get("frontmatter") or {}).get("paper_id"),
        "arxiv_id": note.get("arxiv_id") or (note.get("frontmatter") or {}).get("arxiv_id"),
        "url": (note.get("frontmatter") or {}).get("url"),
        "pdf_url": (note.get("frontmatter") or {}).get("pdf_url"),
        "title": note.get("title") or note.get("note_name"),
    })
    paper = normalize_paper_identity(paper)
    if identity_key(note_paper) and identity_key(note_paper) == identity_key(paper):
        return True
    for key in ("paper_id", "arxiv_id"):
        if note_paper.get(key) and note_paper.get(key) == paper.get(key):
            return True
    note_title = str(note_paper.get("title") or "").strip().lower()
    paper_titles = {str(paper.get("title") or "").strip().lower(), str(paper.get("short_title") or "").strip().lower()}
    return bool(note_title and note_title in paper_titles)

def _find_note_path_from_index_notes(paper, scanned_notes):
    for note in scanned_notes or []:
        if _index_note_matches_paper(note, paper):
            return _existing_file(note.get("path"))
    return ""

def _find_note_path_by_content(paper, paths):
    notes_dir = str(paths.notes_dir)
    if not os.path.isdir(notes_dir):
        return ""
    paper = normalize_paper_identity(paper)
    precise_tokens = [
        str(paper.get("paper_id") or "").strip().lower(),
        str(paper.get("arxiv_id") or "").strip().lower(),
    ]
    title_tokens = [
        str(paper.get("title") or "").strip().lower(),
        str(paper.get("short_title") or "").strip().lower(),
    ]
    title_tokens = [token for token in title_tokens if len(token) >= 8]
    try:
        filenames = [name for name in os.listdir(notes_dir) if name.endswith(".md")]
    except Exception:
        return ""
    for filename in filenames:
        path = os.path.join(notes_dir, filename)
        stem = filename[:-3].lower()
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read(12000).lower()
        except Exception:
            continue
        if any(token and token in raw for token in precise_tokens):
            return os.path.abspath(path)
        if any(token and (token in raw or token == stem) for token in title_tokens):
            return os.path.abspath(path)
    return ""

def _existing_research_note_path(paper, config=None, scanned_notes=None):
    paths = PaperBrainPaths.from_config_dict(config or {})
    for candidate in _note_path_candidates(paper.get("note_path"), paths):
        existing = _existing_file(candidate)
        if existing:
            return existing
    existing = _find_note_path_from_index_notes(paper, scanned_notes)
    if existing:
        return existing
    return _find_note_path_by_content(paper, paths)

def _prepare_preserved_deep_paper(paper, note_path, preserved_at):
    preserved = normalize_paper_identity(deepcopy(paper))
    preserved["note_path"] = note_path
    preserved["deep_analysis_completed"] = True
    preserved["preserved_deep"] = True
    preserved["selected_for_deep_analysis"] = True
    preserved["in_daily_digest"] = True
    preserved["preserved_deep_at"] = preserved_at
    preserved.setdefault("screening_stage", "preserved")
    return preserved

def _preserved_deep_paper_from_note(note, preserved_at):
    fm = note.get("frontmatter") or {}
    paper = {
        "title": note.get("title") or note.get("note_name") or fm.get("title"),
        "short_title": note.get("note_name") or "",
        "paper_id": note.get("paper_id") or fm.get("paper_id"),
        "arxiv_id": note.get("arxiv_id") or fm.get("arxiv_id"),
        "url": fm.get("url"),
        "pdf_url": fm.get("pdf_url"),
        "authors": fm.get("authors") or [],
        "tags": note.get("tags") or fm.get("tags") or [],
        "score": note.get("score", 0),
        "publication_date": note.get("publication_date") or fm.get("publication_date"),
        "note_path": note.get("path"),
        "paper_sources": ["research_note"],
    }
    return _prepare_preserved_deep_paper(paper, note.get("path"), preserved_at)

def _dedupe_preserved_deep_papers(papers):
    by_key = {}
    for paper in papers or []:
        key = identity_key(paper)
        if not key:
            continue
        existing = by_key.get(key)
        if existing is None or bool(paper.get("note_path")):
            by_key[key] = paper
    return list(by_key.values())

def _collect_force_preserved_deep(run_state, config, target_date, research_indexer=None):
    preserved_at = _now_iso()
    source_papers = run_state.papers()
    preserved = []
    for paper in source_papers:
        if not _deep_preservation_signal(paper):
            continue
        note_path = _existing_research_note_path(paper, config=config)
        if not note_path:
            continue
        preserved.append(_prepare_preserved_deep_paper(paper, note_path, preserved_at))

    if not source_papers and research_indexer is not None:
        date_key = _target_date_key(target_date)
        try:
            scanned_notes = research_indexer._scan_notes()
        except Exception as exc:
            logger.warning(f"[WARN] Failed to scan Research_Notes for force preservation: {exc}")
            scanned_notes = []
        for note in scanned_notes:
            if _date_key_from_value(note.get("publication_date")) == date_key and _existing_file(note.get("path")):
                preserved.append(_preserved_deep_paper_from_note(note, preserved_at))

    return _dedupe_preserved_deep_papers(preserved)

def _force_preserved_deep_info(preserved_papers):
    paper_ids = []
    for paper in preserved_papers or []:
        paper_ids.append(paper.get("paper_id") or identity_key(paper))
    return {"count": len(paper_ids), "paper_ids": paper_ids}

def _record_force_preserved_deep(run_state, preserved_papers):
    info = _force_preserved_deep_info(preserved_papers)
    run_state.update_selection(force_preserved_deep=info)
    if not preserved_papers:
        return info
    run_state.add_log_event(
        event_type="force_preserved_deep",
        status="preserved",
        stage=run_state.data.get("stage", ""),
        message=f"preserved_deep={info['count']}",
        details=info,
    )
    return info

def _merge_preserved_deep_record(fresh, preserved):
    merged = normalize_paper_identity(deepcopy(fresh or {}))
    preserved = normalize_paper_identity(preserved or {})
    for key in PRESERVED_DEEP_LIST_FIELDS:
        merged[key] = _merge_unique_values(merged.get(key), preserved.get(key))
    if isinstance(preserved.get("metadata"), dict) or isinstance(merged.get("metadata"), dict):
        metadata = deepcopy(preserved.get("metadata") if isinstance(preserved.get("metadata"), dict) else {})
        metadata.update(merged.get("metadata") if isinstance(merged.get("metadata"), dict) else {})
        merged["metadata"] = metadata
    for key in PRESERVED_DEEP_METADATA_FIELDS:
        if key in preserved:
            if key in ("forced_deep", "forced_digest"):
                merged[key] = bool(merged.get(key) or preserved.get(key))
            else:
                merged[key] = preserved.get(key)
    for key, value in preserved.items():
        if key not in merged or merged.get(key) in (None, "", [], {}, "Unknown"):
            merged[key] = value
    return normalize_paper_identity(merged)

def _merge_preserved_deep_papers(screened_papers, preserved_papers):
    merged = [normalize_paper_identity(deepcopy(p)) for p in screened_papers or [] if p]
    by_key = {identity_key(p): index for index, p in enumerate(merged) if identity_key(p)}
    for preserved in _dedupe_preserved_deep_papers(preserved_papers):
        key = identity_key(preserved)
        if key in by_key:
            merged[by_key[key]] = _merge_preserved_deep_record(merged[by_key[key]], preserved)
        else:
            by_key[key] = len(merged)
            merged.append(normalize_paper_identity(deepcopy(preserved)))
    return merged

def _has_completed_deep_note(paper, target_date, config=None):
    has_completion_flag = bool(
        paper.get("preserved_deep")
        or paper.get("deep_analysis_completed")
        or paper.get("manual_deep_completed_at")
        or (
            paper.get("forced_deep")
            and paper.get("manual_deep_supplement_date") == _target_date_key(target_date)
        )
    )
    if not has_completion_flag:
        return False
    return bool(_existing_research_note_path(paper, config=config))

def _mark_digest_membership(papers, config, provider='doubao'):
    analysis_cfg = config.get('analysis', {})
    provider_cfg = config.get(provider, config.get('doubao', {}))
    provider_threshold = float(provider_cfg.get('threshold_score', 7.0))
    digest_papers, digest_info = scoring_utils.select_daily_digest_papers(
        papers,
        analysis_cfg=analysis_cfg,
        provider_threshold=provider_threshold,
    )
    selected_ids = {id(paper) for paper in digest_papers}
    selected_keys = {p.get('paper_id') for p in digest_papers if p.get('paper_id')}
    selected_keys.update({p.get('title') for p in digest_papers if p.get('title')})
    forced_keys = {
        p.get('paper_id') for p in papers
        if p.get('paper_id') and _digest_force_signal(p)
    }
    forced_keys.update({
        p.get('title') for p in papers
        if p.get('title') and _digest_force_signal(p)
    })
    for paper in papers:
        paper['in_daily_digest'] = (
            id(paper) in selected_ids
            or (paper.get('paper_id') and paper.get('paper_id') in selected_keys)
            or paper.get('title') in selected_keys
            or (paper.get('paper_id') and paper.get('paper_id') in forced_keys)
            or paper.get('title') in forced_keys
        )
    digest_info["forced_count"] = len(forced_keys)
    digest_info["selected_count"] = len([p for p in papers if p.get("in_daily_digest")])
    return digest_info

def _mark_deep_selection(papers, high_value_papers):
    selected_keys = {p.get('paper_id') for p in high_value_papers if p.get('paper_id')}
    selected_keys.update({p.get('title') for p in high_value_papers if p.get('title')})
    for paper in papers:
        paper['selected_for_deep_analysis'] = (
            (paper.get('paper_id') and paper.get('paper_id') in selected_keys)
            or paper.get('title') in selected_keys
            or bool(paper.get('forced_deep'))
            or bool(paper.get('preserved_deep'))
        )

def _load_papers_for_run(scraper, run_state, target_date, arxiv_url, resume=True, force=False, single_paper=None):
    if arxiv_url:
        if single_paper is None:
            single_paper = scraper.fetch_single_arxiv_paper(arxiv_url)
        if single_paper:
            single_paper = normalize_paper_identity(single_paper)
            single_paper["forced_deep"] = True
            single_paper["forced_digest"] = True
            single_paper["selected_for_deep_analysis"] = True
            single_paper["in_daily_digest"] = True
            single_paper["manual_requested_at"] = datetime.now().isoformat(timespec="seconds")
            merged = run_state.merge_paper(single_paper, mode="single", forced_deep=True)
            logger.info(f"[INFO] Injected manual single paper into daily state: {merged.get('paper_id') or merged.get('title')}")
        papers = run_state.papers()
    elif resume and not force and run_state.data.get("stage") in SAVED_PAPER_STAGES:
        papers = run_state.papers()
        logger.info(f"[RESUME] Loaded {len(papers)} papers from {run_state.path}")
    else:
        papers = scraper.get_all_papers(target_date=target_date)

    papers = [normalize_paper_identity(p) for p in papers if p]
    if papers and not arxiv_url and (run_state.data.get("stage") == "initialized" or not resume or force):
        run_state.set_papers(papers, stage="fetched")
    return papers

def _needs_coarse_screening(paper):
    if paper.get("preserved_deep") and paper.get("note_path"):
        return False
    return not paper.get("coarse_score") and not paper.get("score")

def _run_coarse_screening(papers, analyser, run_state, resume=True, cancel_check=None):
    screened_papers = run_state.papers() if resume and run_state.data.get("stage") in COARSE_READY_STAGES else []
    if screened_papers:
        pending = [p for p in screened_papers if _needs_coarse_screening(p)]
        if not pending:
            logger.info(f"[RESUME] Using cached coarse-screened papers: {len(screened_papers)}")
            return screened_papers
        logger.info(f"[RESUME] Coarse screening {len(pending)} newly injected paper(s).")
    else:
        pending = list(papers)

    logger.info(f"[INFO] Starting stage-1 coarse screening for {len(pending)} papers with {analyser.model_flash}...")
    known_keys = {identity_key(p) for p in screened_papers}
    for p in tqdm(pending, desc="Coarse Screening", unit="paper", ascii=True):
        _maybe_cancel(cancel_check)
        coarse_result = analyser.coarse_screen_paper(p)
        _apply_coarse_screen_result(p, coarse_result)
        p = normalize_paper_identity(p)
        if identity_key(p) not in known_keys:
            screened_papers.append(p)
            known_keys.add(identity_key(p))
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
    forced = [p for p in screened_papers if p.get('forced_deep')]
    combined = []
    seen = set()
    for paper in forced + rescreen_pool:
        key = identity_key(paper)
        if key not in seen:
            seen.add(key)
            combined.append(paper)
    return combined

def _run_rigorous_screening(
    screened_papers,
    rescreen_pool,
    analyser,
    run_state,
    analysis_cfg,
    resume=True,
    cache_paths=None,
    cancel_check=None,
):
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
        pending_rescreen = [p for p in rescreen_pool if not p.get("score")]
        if not pending_rescreen:
            logger.info(f"[RESUME] Using cached rigorous screening results: {len(screened_papers)}")
            return
        logger.info(f"[RESUME] Rigorous screening {len(pending_rescreen)} newly injected paper(s).")
        rescreen_pool = pending_rescreen

    for p in tqdm(rescreen_pool, desc="Rigorous Re-Screen", unit="paper", ascii=True):
        _maybe_cancel(cancel_check)
        if use_pdf_context:
            p.pop('screening_document_excerpt', None)
            if _paper_pdf_url_candidates(p):
                logger.info(f"  [CTX] Building stage-2 document excerpt: {p['title']}")
                tmp_pdf_path = download_paper_pdf(p, destination_folder=TEMP_PDF_DIR, cache_paths=cache_paths)
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
        if p.get("forced_deep"):
            p["manual_screened_at"] = datetime.now().isoformat(timespec="seconds")
        p = normalize_paper_identity(p)
        run_state.update_paper(p)
    run_state.mark_stage("screened")

def _drop_screening_excerpts(papers):
    for p in papers:
        p.pop('screening_document_excerpt', None)

def _cleanup_temp_pdfs():
    if os.path.exists(TEMP_PDF_DIR):
        try:
            shutil.rmtree(TEMP_PDF_DIR, ignore_errors=True)
            logger.info("[INFO] Cleaned up temporary PDF files from screening stage.")
        except Exception as e:
            logger.warning(f"[WARN] Failed to clean temp PDFs: {e}")

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
    forced_papers = [p for p in screened_papers if p.get("forced_deep") or p.get("preserved_deep")]
    if forced_papers:
        selected_by_key = {identity_key(p): p for p in high_value_papers}
        for paper in forced_papers:
            selected_by_key.setdefault(identity_key(paper), paper)
        high_value_papers = list(selected_by_key.values())
        selection_info["forced_count"] = len([p for p in forced_papers if p.get("forced_deep")])
        selection_info["preserved_count"] = len([p for p in forced_papers if p.get("preserved_deep")])
        selection_info["selected_count"] = len(high_value_papers)
    _mark_deep_selection(screened_papers, high_value_papers)
    digest_info = _mark_digest_membership(screened_papers, config, provider=provider)
    run_state.set_papers(screened_papers, stage="screened")
    run_state.update_selection(deep_analysis=selection_info, daily_digest=digest_info)
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

def _job_summary(run_state, ok=True):
    summary = run_state.summary()
    for key in ("target_date_source", "arxiv_publication_date", "date_resolution_warning"):
        if run_state.data.get(key):
            summary[key] = run_state.data.get(key)
    summary["ok"] = bool(ok and not summary.get("errors"))
    return summary

def _target_date_key(target_date):
    return target_date.strftime("%Y-%m-%d") if hasattr(target_date, "strftime") else str(target_date)

def _paper_publication_date(paper):
    if not paper:
        return None
    value = paper.get("publication_date") or paper.get("published")
    if hasattr(value, "date"):
        return value.date()
    if hasattr(value, "strftime"):
        return value
    if isinstance(value, str) and value and value.lower() != "unknown":
        try:
            return datetime.strptime(value[:10], "%Y-%m-%d").date()
        except Exception:
            return None
    return None

def _resolve_target_date_for_run(scraper, target_date=None, arxiv_url=None):
    if target_date is not None:
        return target_date, "manual", None, "", ""
    if arxiv_url:
        single_paper = scraper.fetch_single_arxiv_paper(arxiv_url)
        if single_paper:
            single_paper = normalize_paper_identity(single_paper)
        publication_date = _paper_publication_date(single_paper)
        if publication_date:
            return publication_date, "arxiv_v1", single_paper, publication_date.isoformat(), ""
        return (
            datetime.now().date() - timedelta(days=1),
            "fallback_yesterday",
            single_paper,
            "",
            "arxiv_publication_date_unavailable",
        )
    return datetime.now().date() - timedelta(days=1), "default_yesterday", None, "", ""

def _pending_deep_papers(high_value_papers, target_date, config=None):
    pending = []
    for paper in high_value_papers or []:
        if _has_completed_deep_note(paper, target_date, config=config):
            continue
        pending.append(paper)
    return pending

def write_digest_from_state(target_date=None, provider='doubao', single_paper=False):
    if target_date is None:
        target_date = datetime.now().date() - timedelta(days=1)
    if single_paper:
        logger.info("[INFO] digest --single-paper is a compatibility no-op; using canonical daily state.")
        single_paper = False

    config = load_config()
    from src.obsidian_writer import ObsidianWriter

    run_state = RunState(config, target_date, provider, single_paper=single_paper)
    papers = run_state.papers()
    if not papers:
        return {
            **_job_summary(run_state, ok=False),
            "error": {
                "code": "no_saved_papers",
                "message": f"No saved papers found for {target_date} / {provider}.",
                "suggestion": "Run screening first, then rerun `paperbrain digest`.",
                "retryable": False,
            },
        }

    obsidian_writer = ObsidianWriter(config, provider=provider)
    digest_info = _mark_digest_membership(papers, config, provider=provider)
    current_stage = run_state.data.get("stage") or "screened"
    run_state.set_papers(papers, stage=current_stage)
    run_state.update_selection(daily_digest=digest_info)
    screening_report = run_state.write_screening_report()
    digest_path = obsidian_writer.write_daily_digest(papers, target_date=target_date)
    run_state.update_artifacts(daily_digest=digest_path, screening_report=screening_report)

    summary = _job_summary(run_state, ok=True)
    summary["selection"] = {"daily_digest": digest_info}
    return summary

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

    config = load_config()
    prompts = load_prompts()
    def check_cancel():
        run_control.raise_if_cancelled(config)

    from src.scraper import PaperScraper
    from src.analyser import PaperAnalyser
    from src.obsidian_writer import ObsidianWriter
    from src.gardener import KnowledgeGardener
    from src.knowledge_base import KnowledgeBase
    from src.podcaster import Podcaster
    from src.research_indexer import ResearchIndexer

    scraper = PaperScraper(config)
    research_indexer = ResearchIndexer(config)
    target_date, target_date_source, single_paper, arxiv_publication_date, date_resolution_warning = (
        _resolve_target_date_for_run(scraper, target_date=target_date, arxiv_url=arxiv_url)
    )
    if date_resolution_warning:
        logger.warning("[WARN] arXiv publication date unavailable; falling back to yesterday for single-paper run.")

    logger.info(f"[INFO] Target Date for search: {target_date}")
    logger.info(f"[INFO] Target Date Source: {target_date_source}")
    logger.info(f"[INFO] AI Provider: {provider}")
    logger.info(f"[INFO] Podcast Generation: {'Enabled' if generate_podcast else 'Disabled'}")
    logger.info(f"[INFO] Podcast Duration: ~{podcast_minutes} minutes")
    if arxiv_url:
        logger.info(f"[INFO] Single-paper mode enabled for: {arxiv_url}")

    run_state = RunState(config, target_date, provider, single_paper=bool(arxiv_url))
    run_state.data["target_date_source"] = target_date_source
    if arxiv_publication_date:
        run_state.data["arxiv_publication_date"] = arxiv_publication_date
    if date_resolution_warning:
        run_state.data["date_resolution_warning"] = date_resolution_warning
    run_state.save()
    force_preserved_deep = []
    if force:
        force_preserved_deep = _collect_force_preserved_deep(
            run_state,
            config,
            target_date,
            research_indexer=research_indexer,
        )
        logger.info("[INFO] Force mode enabled: resetting run state.")
        if force_preserved_deep:
            logger.info(f"[INFO] Preserving {len(force_preserved_deep)} completed deep-analysis paper(s) across force reset.")
        run_state.reset()
        run_state.data["target_date_source"] = target_date_source
        if arxiv_publication_date:
            run_state.data["arxiv_publication_date"] = arxiv_publication_date
        if date_resolution_warning:
            run_state.data["date_resolution_warning"] = date_resolution_warning
        run_state.save()
        _record_force_preserved_deep(run_state, force_preserved_deep)

    analyser = PaperAnalyser(config, provider=provider, prompts=prompts)
    obsidian_writer = ObsidianWriter(config, provider=provider)
    gardener = KnowledgeGardener(config, provider=provider)
    knowledge_base = KnowledgeBase(config, provider=provider, prompts=prompts)
    podcaster = Podcaster(config, provider=provider, prompts=prompts)
    
    papers = _load_papers_for_run(
        scraper,
        run_state,
        target_date,
        arxiv_url,
        resume=resume,
        force=force,
        single_paper=single_paper,
    )
    if not papers:
        if force_preserved_deep:
            run_state.set_papers(force_preserved_deep, stage="screened")
            papers = run_state.papers()
        else:
            logger.info(f"No papers found for date {target_date}.")
            run_state.mark_stage("completed")
            return _job_summary(run_state)
    if force_preserved_deep and stop_after == "fetch":
        fetched_papers = _merge_preserved_deep_papers(run_state.papers(), force_preserved_deep)
        run_state.set_papers(fetched_papers, stage=run_state.data.get("stage") or "fetched")
    if not papers:
        logger.info(f"No papers found for date {target_date}.")
        run_state.mark_stage("completed")
        return _job_summary(run_state)
    check_cancel()
    if stop_after == "fetch":
        logger.info("[STOP] stop_after=fetch")
        return _job_summary(run_state)

    # 2. Two-stage screening
    screened_papers = _run_coarse_screening(papers, analyser, run_state, resume=resume, cancel_check=check_cancel)
    check_cancel()
    if stop_after == "coarse":
        logger.info("[STOP] stop_after=coarse")
        return _job_summary(run_state)

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
        cancel_check=check_cancel,
    )
    check_cancel()
    if force_preserved_deep:
        screened_papers = _merge_preserved_deep_papers(screened_papers, force_preserved_deep)
        run_state.set_papers(screened_papers, stage=run_state.data.get("stage") or "screened")

    if stop_after == "screen":
        logger.info("[STOP] stop_after=screen")
        return _job_summary(run_state)

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
    check_cancel()
    
    highest_scoring_paper = None
    highest_score = -1
    highest_analysis_content = ""
    highest_rag_context = ""

    papers_for_deep = _pending_deep_papers(high_value_papers, target_date, config=config)

    if not high_value_papers:
        logger.info("[INFO] No suitable papers found for deep analysis even after relaxing criteria.")
    elif not papers_for_deep:
        logger.info("[RESUME] Deep analysis already completed in run state.")
    else:
        if len(papers_for_deep) != len(high_value_papers):
            logger.info(f"[RESUME] Deep analysis pending for {len(papers_for_deep)} paper(s); completed/preserved notes will be skipped.")
        logger.info(f"[INFO] Starting Deep Analysis for {len(papers_for_deep)} high-value papers...")
        
        for i, p in enumerate(papers_for_deep):
            check_cancel()
            logger.info(f"[{i+1}/{len(papers_for_deep)}] Analyzing: {p['title']} (Score: {p['score']})")
            
            if not _paper_pdf_url_candidates(p):
                logger.warning(f"[WARN] No PDF URL for {p['title']}, skipping.")
                continue
            
            # Download PDF
            logger.info(f"  [STEP] Downloading PDF...")
            pdf_path = download_paper_pdf(p, destination_folder=obsidian_writer.pdf_folder, cache_paths=run_pdf_cache_paths)
            
            if pdf_path:
                p["pdf_path"] = pdf_path
                run_state.update_paper(p)

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
                if p.get("forced_deep"):
                    p["manual_deep_supplement_date"] = _target_date_key(target_date)
                    p["manual_deep_completed_at"] = datetime.now().isoformat(timespec="seconds")
                note_path = obsidian_writer.write_detailed_note(p, analysis_text, local_pdf_path=pdf_path, image_caption=None)
                p["note_path"] = note_path
                p["deep_analysis_completed"] = True
                run_state.update_paper(p)
                research_indexer.update_after_new_note(note_path)
                
                logger.info(f"  [DONE] Analysis complete and saved.")
            else:
                logger.error(f"  [ERR] PDF unavailable for '{p['title']}'. Skipping deep analysis to avoid extra token cost.")
        run_state.mark_stage("deep_analyzed")

    if stop_after == "deep":
        logger.info("[STOP] stop_after=deep")
        return _job_summary(run_state)

    # 4. Write Daily Digest from the merged canonical daily state.
    check_cancel()
    digest_papers = run_state.papers()
    _mark_digest_membership(digest_papers, config, provider=provider)
    run_state.set_papers(digest_papers, stage=run_state.data.get("stage") or "screened")
    digest_path = obsidian_writer.write_daily_digest(run_state.papers(), target_date=target_date)
    run_state.update_artifacts(daily_digest=digest_path)
    run_state.mark_stage("digest_written")

    # 5. Knowledge Gardening (Backlinking)
    if high_value_papers:
        check_cancel()
        logger.info("[INFO] Starting Knowledge Gardening (Backlinking)...")
        gardener.prune_and_graft(high_value_papers)
        research_indexer.build(update_notes=True)

    # 6. Generate Podcast for the BEST paper
    if generate_podcast and highest_scoring_paper:
        check_cancel()
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
    return _job_summary(run_state)

if __name__ == "__main__":
    import sys
    from src.cli import legacy_main_args, main as cli_main

    print(
        "[DEPRECATED] Use `python script/paperbrain.py run ...` instead of `python script/main.py ...`.",
        file=sys.stderr,
    )
    raise SystemExit(cli_main(legacy_main_args(sys.argv[1:]), pipeline_module=sys.modules[__name__]))
