"""Deterministic scoring helpers for PaperBrain screening.

The LLM gives dimension estimates; this module applies the stable rubric:
weighted score, confidence/red-flag penalties, and conservative quality caps.
"""

from __future__ import annotations

from math import ceil


DEFAULT_SCREENING_WEIGHTS = {
    "relevance": 0.30,
    "novelty": 0.23,
    "rigor": 0.22,
    "evidence": 0.15,
    "reproducibility": 0.10,
}

DEFAULT_QUALITY_GATE = {
    "relevance": 6.0,
    "rigor": 6.0,
    "evidence": 6.0,
    "confidence": 4.0,
    "red_flags_max": 2,
}


def safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def clamp_score(value, default=5.0):
    n = safe_float(value, default)
    return round(max(1.0, min(10.0, n)), 1)


def normalize_red_flags(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def normalize_screening_weights(weights=None):
    merged = dict(DEFAULT_SCREENING_WEIGHTS)
    if isinstance(weights, dict):
        for key in merged:
            merged[key] = max(0.0, safe_float(weights.get(key), merged[key]))
    if sum(merged.values()) <= 0:
        return dict(DEFAULT_SCREENING_WEIGHTS)
    return merged


def coarse_screening_score(relevance, evidence, method_completeness):
    relevance = clamp_score(relevance)
    evidence = clamp_score(evidence)
    method_completeness = clamp_score(method_completeness)
    score = 0.45 * relevance + 0.35 * evidence + 0.20 * method_completeness

    # The first pass is recall-oriented, but off-topic or empty abstracts should
    # not occupy the stronger second-pass model budget.
    if relevance <= 4.0:
        score = min(score, 5.0)
    if evidence <= 4.0 and method_completeness <= 4.0:
        score = min(score, 5.0)

    return clamp_score(score)


def calibrated_screening_score(
    relevance,
    novelty,
    rigor,
    evidence,
    reproducibility,
    confidence=6.0,
    red_flags=None,
    weights=None,
):
    relevance = clamp_score(relevance)
    novelty = clamp_score(novelty)
    rigor = clamp_score(rigor)
    evidence = clamp_score(evidence)
    reproducibility = clamp_score(reproducibility)
    confidence = clamp_score(confidence, default=6.0)
    flags = normalize_red_flags(red_flags)
    weights = normalize_screening_weights(weights)

    total_w = sum(weights.values()) or 1.0
    score = (
        weights["relevance"] * relevance
        + weights["novelty"] * novelty
        + weights["rigor"] * rigor
        + weights["evidence"] * evidence
        + weights["reproducibility"] * reproducibility
    ) / total_w

    # Low confidence should make the final score cautious without erasing the
    # useful signal from the dimension scores.
    if confidence < 6.0:
        score -= 0.15 * (6.0 - confidence)

    score -= 0.35 * len(flags)

    caps = []
    if relevance <= 4.0:
        caps.append(6.0)
    if rigor <= 4.0 or evidence <= 4.0:
        caps.append(7.0)
    if confidence <= 4.0:
        caps.append(7.0)
    if rigor < 6.0 and evidence < 6.0:
        caps.append(7.4)
    if reproducibility <= 3.5:
        caps.append(8.5)
    if len(flags) >= 2:
        caps.append(7.5)
    if len(flags) >= 3:
        caps.append(6.8)
    if caps:
        score = min(score, *caps)

    return clamp_score(score)


def dynamic_stage2_top_k(total_count, min_k=10, ratio=0.25, max_k=20):
    total_count = max(0, int(total_count or 0))
    if total_count == 0:
        return 0
    min_k = max(1, int(min_k or 1))
    max_k = max(1, int(max_k or min_k))
    ratio = max(0.0, safe_float(ratio, 0.25))
    dynamic_k = max(min_k, ceil(total_count * ratio))
    return max(1, min(dynamic_k, max_k, total_count))


def quality_priority(paper):
    rel = safe_float(paper.get("relevance"), 0.0)
    nov = safe_float(paper.get("novelty"), 0.0)
    rig = safe_float(paper.get("rigor"), 0.0)
    evd = safe_float(paper.get("evidence"), 0.0)
    rep = safe_float(paper.get("reproducibility"), 0.0)
    conf = safe_float(paper.get("confidence"), 0.0)
    flags = normalize_red_flags(paper.get("red_flags", []))
    github = str(paper.get("github", "") or "").strip().lower()
    code_bonus = 0.15 if github and github not in ("none", "unknown", "nan") else 0.0
    penalty = 0.35 * len(flags)
    return (
        0.30 * rel
        + 0.22 * nov
        + 0.22 * rig
        + 0.16 * evd
        + 0.10 * rep
        + 0.10 * conf
        + code_bonus
        - penalty
    )


def daily_digest_backfill_priority(paper):
    score = safe_float(paper.get("score"), 0.0)
    coarse_score = safe_float(paper.get("coarse_score"), score)
    novelty = safe_float(paper.get("novelty"), 0.0)
    rigor = safe_float(
        paper.get("rigor"),
        safe_float(paper.get("coarse_method_completeness"), 0.0),
    )
    evidence = safe_float(
        paper.get("evidence"),
        safe_float(paper.get("coarse_evidence"), 0.0),
    )
    reproducibility = safe_float(paper.get("reproducibility"), 0.0)
    confidence = safe_float(paper.get("confidence"), 0.0)
    flags = normalize_red_flags(paper.get("red_flags", []))
    return (
        0.35 * max(score, coarse_score)
        + 0.20 * novelty
        + 0.20 * rigor
        + 0.20 * evidence
        + 0.05 * reproducibility
        + 0.05 * confidence
        - 0.25 * len(flags)
    )


def select_daily_digest_papers(screened_papers, analysis_cfg=None, provider_threshold=7.0):
    analysis_cfg = analysis_cfg or {}
    min_score = safe_float(
        analysis_cfg.get("daily_digest_min_score"),
        safe_float(provider_threshold, 7.0),
    )
    target_min_count = max(0, int(safe_float(
        analysis_cfg.get("daily_digest_target_min_count"),
        5,
    )))
    papers = list(screened_papers or [])

    selected = [
        paper for paper in papers
        if safe_float(paper.get("score"), 0.0) >= min_score
    ]
    selected.sort(
        key=lambda paper: (
            safe_float(paper.get("score"), 0.0),
            daily_digest_backfill_priority(paper),
        ),
        reverse=True,
    )

    backfilled = []
    if target_min_count and len(selected) < target_min_count:
        selected_ids = {id(paper) for paper in selected}
        remaining = [paper for paper in papers if id(paper) not in selected_ids]
        remaining.sort(
            key=lambda paper: (
                daily_digest_backfill_priority(paper),
                safe_float(paper.get("score"), 0.0),
            ),
            reverse=True,
        )
        backfilled = remaining[:target_min_count - len(selected)]
        selected.extend(backfilled)
        selected.sort(
            key=lambda paper: (
                safe_float(paper.get("score"), 0.0),
                daily_digest_backfill_priority(paper),
            ),
            reverse=True,
        )

    threshold_count = len([
        paper for paper in papers
        if safe_float(paper.get("score"), 0.0) >= min_score
    ])
    diagnostics = {
        "min_score": min_score,
        "target_min_count": target_min_count,
        "threshold_count": threshold_count,
        "backfill_count": len(backfilled),
        "selected_count": len(selected),
    }
    return selected, diagnostics


def passes_quality_gate(paper, gate=None):
    gate = {**DEFAULT_QUALITY_GATE, **(gate or {})}
    flags = normalize_red_flags(paper.get("red_flags", []))
    return (
        safe_float(paper.get("relevance"), 0.0) >= safe_float(gate.get("relevance"), 6.0)
        and safe_float(paper.get("rigor"), 0.0) >= safe_float(gate.get("rigor"), 6.0)
        and safe_float(paper.get("evidence"), 0.0) >= safe_float(gate.get("evidence"), 6.0)
        and safe_float(paper.get("confidence"), 10.0) >= safe_float(gate.get("confidence"), 4.0)
        and len(flags) <= int(safe_float(gate.get("red_flags_max"), 2))
    )


def select_deep_analysis_papers(screened_papers, analysis_cfg=None, provider_threshold=8.0):
    analysis_cfg = analysis_cfg or {}
    lower_threshold = safe_float(
        analysis_cfg.get("deep_analysis_lower_threshold"),
        safe_float(provider_threshold, 8.0),
    )
    extra_threshold = safe_float(analysis_cfg.get("deep_analysis_extra_threshold"), 8.8)
    base_max = int(safe_float(
        analysis_cfg.get("daily_deep_analysis_base_max", analysis_cfg.get("max_papers_per_day", 2)),
        2,
    ))
    base_max = max(1, base_max)
    daily_min = max(0, int(safe_float(analysis_cfg.get("daily_deep_analysis_min"), 1)))
    quality_gate_cfg = analysis_cfg.get("deep_analysis_quality_gate", {})

    candidates = [
        paper for paper in screened_papers
        if safe_float(paper.get("score"), 0.0) >= lower_threshold
    ]
    quality_passed = [
        paper for paper in candidates
        if passes_quality_gate(paper, quality_gate_cfg)
    ]
    ranked = sorted(
        quality_passed,
        key=lambda paper: (safe_float(paper.get("score"), 0.0), quality_priority(paper)),
        reverse=True,
    )

    base_selection = ranked[:base_max]
    extra_selection = [
        paper for paper in ranked[base_max:]
        if safe_float(paper.get("score"), 0.0) >= extra_threshold
    ]
    selected = base_selection + extra_selection
    if len(selected) < daily_min and ranked:
        selected = ranked[:daily_min]

    diagnostics = {
        "lower_threshold": lower_threshold,
        "extra_threshold": extra_threshold,
        "base_max": base_max,
        "daily_min": daily_min,
        "candidate_count": len(candidates),
        "quality_passed_count": len(quality_passed),
        "base_count": len(base_selection),
        "extra_count": len(extra_selection),
        "selected_count": len(selected),
    }
    return selected, diagnostics
