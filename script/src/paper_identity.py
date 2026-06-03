"""Canonical paper identity helpers.

PaperBrain treats arXiv IDs as the primary identity whenever available. Titles,
short titles, note filenames, and aliases are presentation details; the stable
identity is `paper_id`, usually `arxiv:2606.02486`.
"""

from __future__ import annotations

import hashlib
import re


ARXIV_ID_RE = re.compile(r"(?P<id>\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)


def canonical_arxiv_id(value):
    """Return a versionless arXiv ID from a URL, Hugging Face paper URL, or raw ID."""
    if not value:
        return ""
    text = str(value).strip()
    text = text.replace(".pdf", "")
    text = text.split("?")[0].split("#")[0]
    match = ARXIV_ID_RE.search(text)
    return match.group("id") if match else ""


def paper_id_from_arxiv_id(arxiv_id):
    arxiv_id = canonical_arxiv_id(arxiv_id)
    return f"arxiv:{arxiv_id}" if arxiv_id else ""


def paper_id_from_metadata(metadata):
    """Infer the canonical paper ID from a paper dict or frontmatter dict."""
    if not isinstance(metadata, dict):
        return ""

    existing = str(metadata.get("paper_id") or "").strip()
    if existing.startswith("arxiv:"):
        arxiv_id = canonical_arxiv_id(existing)
        return paper_id_from_arxiv_id(arxiv_id)
    if existing:
        return existing

    for key in ("arxiv_id", "url", "pdf_url", "id"):
        arxiv_id = canonical_arxiv_id(metadata.get(key))
        if arxiv_id:
            return paper_id_from_arxiv_id(arxiv_id)

    title = str(metadata.get("title") or metadata.get("short_title") or "").strip().lower()
    if title:
        digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:12]
        return f"title:{digest}"
    return ""


def normalize_paper_identity(paper):
    """Return a shallow copy with normalized `arxiv_id` and `paper_id` fields."""
    normalized = dict(paper or {})
    arxiv_id = ""
    for key in ("arxiv_id", "url", "pdf_url", "id", "paper_id"):
        arxiv_id = canonical_arxiv_id(normalized.get(key))
        if arxiv_id:
            break

    if arxiv_id:
        normalized["arxiv_id"] = arxiv_id
        normalized["paper_id"] = paper_id_from_arxiv_id(arxiv_id)
    else:
        normalized["paper_id"] = paper_id_from_metadata(normalized)
    return normalized


def identity_key(paper):
    return paper_id_from_metadata(paper) or str((paper or {}).get("title") or "").strip().lower()
