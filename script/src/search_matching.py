"""Deterministic local matching for user-defined research interests."""

from __future__ import annotations

import re
import unicodedata


_SEPARATOR_RE = re.compile(r"[-\u2010-\u2015\u2212_/]+")
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_search_text(value) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    text = _SEPARATOR_RE.sub(" ", text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def keyword_matches(text, keyword) -> bool:
    haystack = normalize_search_text(text)
    needle = normalize_search_text(keyword)
    if not haystack or not needle:
        return False

    expression = re.escape(needle).replace(r"\ ", r"\s+")
    if needle[0].isalnum():
        expression = rf"(?<!\w){expression}"
    if needle[-1].isalnum():
        expression = rf"{expression}(?!\w)"
    return re.search(expression, haystack, flags=re.UNICODE) is not None


def matched_keywords(title, abstract, keywords) -> list[str]:
    text = f"{title or ''} {abstract or ''}"
    matches = []
    seen = set()
    for value in keywords or []:
        keyword = str(value or "").strip()
        normalized = normalize_search_text(keyword)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        if keyword_matches(text, keyword):
            matches.append(keyword)
    return matches


def paper_matches_keywords(title, abstract, keywords) -> bool:
    return bool(matched_keywords(title, abstract, keywords))
