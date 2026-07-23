"""Persistent run state and full screening records."""

from __future__ import annotations

import json
import os
import shutil
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from src.paper_identity import identity_key, normalize_paper_identity
from src.paths import PaperBrainPaths
from src.file_io import atomic_write_text


STAGE_ORDER = {
    "initialized": 0,
    "fetched": 1,
    "coarse_screened": 2,
    "screened": 3,
    "digest_written": 4,
    "deep_analyzed": 5,
    "completed": 6,
    "cancelled": 7,
    "failed": 8,
}

LIST_FIELDS = ("authors", "tags", "red_flags", "ai_aliases", "institutions", "paper_sources", "provider_sources")
OR_FIELDS = (
    "in_daily_digest",
    "selected_for_deep_analysis",
    "forced_deep",
    "forced_digest",
    "preserved_deep",
    "deep_analysis_completed",
    "should_rescreen",
)


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _atomic_write_with_retry(path, content, attempts=4):
    for attempt in range(attempts):
        try:
            atomic_write_text(path, content)
            return
        except PermissionError:
            if attempt + 1 >= attempts:
                raise
            time.sleep(0.02 * (2 ** attempt))


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _present(value):
    if value is None:
        return False
    if isinstance(value, str) and value.strip().lower() in ("", "unknown", "none", "null"):
        return False
    if isinstance(value, (list, tuple, dict)) and not value:
        return False
    return True


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [item for item in value if item is not None and str(item).strip()]
    if str(value).strip():
        return [value]
    return []


def _merge_unique(*values):
    merged = []
    seen = set()
    for value in values:
        for item in _as_list(value):
            key = str(item).strip().lower()
            if key and key not in seen:
                seen.add(key)
                merged.append(item)
    return merged


class RunState:
    def __init__(self, config, target_date, provider, single_paper=False):
        paths = PaperBrainPaths.from_config_dict(config)
        date_key = target_date.strftime("%Y-%m-%d") if hasattr(target_date, "strftime") else str(target_date)
        self.paths = paths
        self.date_key = date_key
        self.provider = provider
        self.single_paper = single_paper
        self.run_id = paths.run_id(date_key, provider, single_paper)
        self.folder = str(paths.run_records_dir)
        self.run_dir = str(paths.run_dir(date_key, provider, single_paper))
        self.path = str(paths.state_path(date_key, provider, single_paper))
        self.legacy_path = str(paths.legacy_state_path(date_key, provider, single_paper))
        self.screening_report_path = str(paths.screening_report_path(date_key, provider, single_paper))
        self.log_summary_path = str(paths.log_summary_path(date_key, provider, single_paper))
        self.errors_path = str(paths.errors_path(date_key, provider, single_paper))
        self._legacy_sources_to_archive = []
        os.makedirs(self.run_dir, exist_ok=True)
        self.data = self._load()
        self._ensure_runtime_fields()
        self.save()
        archived = self._archive_legacy_sources()
        if archived:
            self.add_log_event(
                event_type="legacy_migration",
                status="archived",
                stage=self.data.get("stage", ""),
                message=f"archived_legacy_sources={archived}",
                save=True,
            )

    def _load(self):
        candidates = self._state_candidates()
        if not candidates:
            return self._empty_data()

        merged = self._empty_data()
        for candidate in candidates:
            data = candidate["data"]
            source_path = candidate["path"]
            mode = self._source_mode(data, source_path)
            provider = data.get("provider") or self.provider
            normalized = self._normalize_loaded_data(data, source_path, mode, provider)
            merged = self._merge_run_data(merged, normalized)
            if candidate.get("archive"):
                self._legacy_sources_to_archive.append(candidate["archive_path"])
        return merged

    def _state_candidates(self):
        candidates = []
        seen = set()
        run_records = Path(self.folder)

        def add_state(path, archive=False, archive_path=None):
            path = Path(path)
            key = str(path.resolve()) if path.exists() else str(path)
            if key in seen or not path.exists() or not path.is_file():
                return
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                return
            seen.add(key)
            candidates.append(
                {
                    "path": path,
                    "data": data,
                    "archive": bool(archive),
                    "archive_path": Path(archive_path or path),
                }
            )

        add_state(self.path, archive=False)

        if run_records.exists():
            for entry in run_records.iterdir():
                if entry.name == self.run_id or entry.name == "_legacy":
                    continue
                if not entry.name.startswith(f"{self.date_key}-"):
                    continue
                if entry.is_dir():
                    add_state(entry / "state.json", archive=True, archive_path=entry)
                elif entry.is_file() and entry.name.endswith("-run-state.json"):
                    add_state(entry, archive=True, archive_path=entry)

        # A no-provider flat legacy state is uncommon, but it still belongs to
        # the same canonical day if present.
        add_state(Path(self.legacy_path), archive=True, archive_path=Path(self.legacy_path))
        return candidates

    def _source_mode(self, data, source_path):
        modes = {str(item).lower() for item in _as_list(data.get("run_modes"))}
        name = str(source_path).lower()
        if data.get("single_paper") or "single" in modes or "-single" in name:
            return "single"
        return "daily"

    def _normalize_loaded_data(self, data, source_path, mode, provider):
        normalized = deepcopy(data or {})
        normalized.setdefault("date", self.date_key)
        normalized.setdefault("provider", provider)
        normalized.setdefault("stage", "initialized")
        normalized.setdefault("papers", [])
        normalized.setdefault("selection", {})
        normalized.setdefault("artifacts", {})
        normalized.setdefault("errors", [])
        normalized.setdefault("logs", [])
        normalized.setdefault("merged_from", [])
        normalized["providers"] = _merge_unique(normalized.get("providers"), provider)
        normalized["run_modes"] = _merge_unique(normalized.get("run_modes"), mode)
        normalized["source_path"] = str(source_path)
        papers = []
        for paper in normalized.get("papers", []) or []:
            prepared = self._annotate_paper(paper, mode=mode, provider=provider)
            if mode == "single":
                prepared["forced_deep"] = True
                prepared["forced_digest"] = True
                prepared["selected_for_deep_analysis"] = True
                prepared["in_daily_digest"] = True
                prepared.setdefault("manual_requested_at", normalized.get("created_at") or normalized.get("updated_at") or _now())
            papers.append(prepared)
        normalized["papers"] = papers
        return normalized

    def _merge_run_data(self, base, incoming):
        merged = deepcopy(base or self._empty_data())
        incoming = incoming or {}
        merged["created_at"] = min(
            [value for value in (merged.get("created_at"), incoming.get("created_at")) if value] or [_now()]
        )
        if incoming.get("updated_at") and incoming.get("updated_at", "") > merged.get("updated_at", ""):
            merged["updated_at"] = incoming.get("updated_at", "")

        current_stage = merged.get("stage", "initialized")
        incoming_stage = incoming.get("stage", "initialized")
        if STAGE_ORDER.get(incoming_stage, 0) > STAGE_ORDER.get(current_stage, 0):
            merged["stage"] = incoming_stage

        merged["providers"] = _merge_unique(merged.get("providers"), incoming.get("providers"), incoming.get("provider"))
        merged["run_modes"] = _merge_unique(merged.get("run_modes"), incoming.get("run_modes"))
        merged["selection"] = {**(merged.get("selection") or {}), **(incoming.get("selection") or {})}
        merged["artifacts"] = {**(merged.get("artifacts") or {}), **(incoming.get("artifacts") or {})}
        merged["errors"] = list(merged.get("errors") or []) + list(incoming.get("errors") or [])
        merged["logs"] = list(merged.get("logs") or []) + list(incoming.get("logs") or [])
        merged["merged_from"] = _merge_unique(merged.get("merged_from"), incoming.get("merged_from"), incoming.get("source_path"))
        merged["papers"] = self._merge_paper_lists(merged.get("papers", []), incoming.get("papers", []))
        return merged

    def _empty_data(self):
        mode = "single" if self.single_paper else "daily"
        return {
            "run_id": self.run_id,
            "date": self.date_key,
            "provider": self.provider,
            "providers": [self.provider],
            "single_paper": self.single_paper,
            "run_modes": [mode],
            "created_at": _now(),
            "updated_at": "",
            "stage": "initialized",
            "papers": [],
            "selection": {},
            "artifacts": {},
            "errors": [],
            "logs": [],
            "merged_from": [],
            "paths": {},
        }

    def _ensure_runtime_fields(self):
        self.data["run_id"] = self.run_id
        self.data["date"] = self.date_key
        self.data["provider"] = self.provider
        self.data["providers"] = _merge_unique(self.data.get("providers"), self.provider)
        self.data["run_modes"] = _merge_unique(self.data.get("run_modes"), "single" if self.single_paper else "daily")
        self.data["single_paper"] = "single" in self.data["run_modes"] and "daily" not in self.data["run_modes"]
        self.data.setdefault("created_at", _now())
        self.data.setdefault("updated_at", "")
        self.data.setdefault("stage", "initialized")
        self.data.setdefault("papers", [])
        self.data.setdefault("selection", {})
        self.data.setdefault("artifacts", {})
        self.data.setdefault("errors", [])
        self.data.setdefault("logs", [])
        self.data.setdefault("merged_from", [])
        self.data["paths"] = {
            "run_dir": self.run_dir,
            "state": self.path,
            "legacy_state": self.legacy_path,
            "screening_report": self.screening_report_path,
            "log_summary": self.log_summary_path,
            "errors": self.errors_path,
        }

    def _archive_legacy_sources(self):
        archived = 0
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_root = Path(self.folder) / "_legacy" / self.date_key
        for source in self._legacy_sources_to_archive:
            source = Path(source)
            if not source.exists() or source == Path(self.run_dir) or source == Path(self.path):
                continue
            archive_root.mkdir(parents=True, exist_ok=True)
            dest = archive_root / source.name
            if dest.exists():
                dest = archive_root / f"{source.name}-{timestamp}"
            try:
                shutil.move(str(source), str(dest))
                archived += 1
            except Exception:
                continue
        return archived

    def save(self):
        self.data["updated_at"] = _now()
        _atomic_write_with_retry(
            self.path,
            json.dumps(self.data, ensure_ascii=False, indent=2),
        )
        self._write_errors()
        self._write_log_summary()

    def mark_stage(self, stage):
        self.data["stage"] = stage
        event_type = "completed" if stage == "completed" else "stage_completed"
        if stage in ("failed", "cancelled"):
            event_type = stage
        self.add_log_event(
            event_type=event_type,
            status=self._event_status(event_type, stage),
            stage=stage,
            message=f"stage={stage}",
            save=False,
        )
        self.save()

    def reset(self):
        self.data = self._empty_data()
        self._ensure_runtime_fields()
        self.save()

    def has_stage(self, stage):
        return self.data.get("stage") == stage

    def papers(self):
        return [normalize_paper_identity(p) for p in self.data.get("papers", [])]

    def set_papers(self, papers, stage):
        mode = "single" if self.single_paper else "daily"
        incoming = [self._annotate_paper(p, mode=mode, provider=self.provider) for p in papers]
        self.data["papers"] = self._merge_paper_lists(self.data.get("papers", []), incoming)
        self.data["stage"] = stage
        self.add_log_event(
            event_type="queue_updated",
            status="updated",
            stage=stage,
            message=f"papers={len(self.data['papers'])}",
            save=False,
        )
        self.save()

    def merge_paper(self, paper, mode=None, forced_deep=False):
        mode = mode or ("single" if self.single_paper else "daily")
        prepared = self._annotate_paper(paper, mode=mode, provider=self.provider)
        if forced_deep:
            prepared["forced_deep"] = True
            prepared["forced_digest"] = True
            prepared["selected_for_deep_analysis"] = True
            prepared["in_daily_digest"] = True
            prepared.setdefault("manual_requested_at", _now())
        self.data["papers"] = self._merge_paper_lists(self.data.get("papers", []), [prepared])
        merged = self._find_paper(prepared)
        self.data["run_modes"] = _merge_unique(self.data.get("run_modes"), mode)
        self.add_log_event(
            event_type="paper_updated",
            status="updated",
            stage=self.data.get("stage", ""),
            paper_id=prepared.get("paper_id", ""),
            title=prepared.get("short_title") or prepared.get("title", ""),
            message="paper_merged",
            save=False,
        )
        self.save()
        return merged or prepared

    def update_paper(self, paper):
        paper = self._annotate_paper(paper, mode="single" if self.single_paper else "daily", provider=self.provider)
        self.data["papers"] = self._merge_paper_lists(self.data.get("papers", []), [paper])
        self.add_log_event(
            event_type="paper_updated",
            status="updated",
            stage=self.data.get("stage", ""),
            paper_id=paper.get("paper_id", ""),
            title=paper.get("short_title") or paper.get("title", ""),
            message="paper_updated",
            save=False,
        )
        self.save()

    def update_selection(self, **kwargs):
        self.data.setdefault("selection", {}).update(kwargs)
        self.save()

    def update_artifacts(self, **kwargs):
        self.data.setdefault("artifacts", {}).update(kwargs)
        for key, value in kwargs.items():
            self.add_log_event(
                event_type="artifact_written",
                status="available",
                stage=self.data.get("stage", ""),
                artifact_path=value,
                message=f"artifact={key}",
                save=False,
            )
        self.save()

    def add_log_event(
        self,
        event_type="log",
        status="",
        stage="",
        paper_id="",
        title="",
        provider="",
        model="",
        elapsed_ms=None,
        retry_count=0,
        artifact_path="",
        message="",
        details=None,
        save=True,
    ):
        created_at = _now()
        stage_value = stage or self.data.get("stage", "")
        event_type = event_type or "log"
        event = {
            "schema_version": 1,
            "event_type": event_type,
            "status": status or self._event_status(event_type, stage_value),
            "created_at": created_at,
            "ts": created_at,
            "stage": stage_value,
            "paper_id": paper_id,
            "title": title,
            "provider": provider or self.provider,
            "model": model,
            "elapsed_ms": elapsed_ms,
            "retry_count": retry_count,
            "artifact_path": artifact_path or "",
            "message": message,
            "details": details or {},
        }
        self.data.setdefault("logs", []).append(event)
        if save:
            self.save()

    def _event_status(self, event_type, stage):
        if event_type in ("error", "failed"):
            return "failed"
        if event_type == "cancelled" or stage == "cancelled":
            return "cancelled"
        if event_type == "artifact_written":
            return "available"
        if event_type in ("queue_updated", "paper_updated"):
            return "updated"
        if event_type in ("completed", "stage_completed"):
            return "completed"
        return "running" if stage and stage not in ("initialized", "completed") else "idle"

    def add_error(
        self,
        code,
        message,
        suggestion="",
        stage="",
        paper_id="",
        title="",
        exception="",
        retryable=False,
        save=True,
    ):
        error = {
            "created_at": _now(),
            "code": code,
            "message": message,
            "suggestion": suggestion,
            "stage": stage or self.data.get("stage", ""),
            "paper_id": paper_id,
            "title": title,
            "exception": exception,
            "retryable": bool(retryable),
        }
        duplicate = next(
            (
                existing
                for existing in self.data.setdefault("errors", [])
                if existing.get("code") == error["code"]
                and existing.get("stage") == error["stage"]
                and existing.get("paper_id") == error["paper_id"]
                and existing.get("title") == error["title"]
            ),
            None,
        )
        if duplicate is not None:
            duplicate.update(error)
            if save:
                self.save()
            return duplicate
        self.data.setdefault("errors", []).append(error)
        self.add_log_event(
            event_type="error",
            status="failed",
            stage=error["stage"],
            paper_id=paper_id,
            title=title,
            message=f"error={code}",
            save=False,
        )
        if save:
            self.save()
        return error

    def clear_retryable_errors(self):
        errors = list(self.data.get("errors", []))
        retained = [error for error in errors if not error.get("retryable")]
        removed = len(errors) - len(retained)
        if not removed:
            return 0
        self.data["errors"] = retained
        self.add_log_event(
            event_type="retry_errors_cleared",
            status="cleared",
            stage=self.data.get("stage", ""),
            message=f"retryable_errors_cleared={removed}",
            save=False,
        )
        self.save()
        return removed

    def resolve_errors(
        self,
        code=None,
        stage=None,
        paper_id=None,
        title=None,
        retryable=None,
        save=True,
    ):
        """Resolve only errors whose failed operation has now succeeded."""
        errors = list(self.data.get("errors", []))

        def matches(error):
            if code is not None and error.get("code") != code:
                return False
            if stage is not None and error.get("stage") != stage:
                return False
            if paper_id is not None and error.get("paper_id") != paper_id:
                return False
            if title is not None and error.get("title") != title:
                return False
            if retryable is not None and bool(error.get("retryable")) != bool(retryable):
                return False
            return True

        retained = [error for error in errors if not matches(error)]
        removed = len(errors) - len(retained)
        if not removed:
            return 0
        self.data["errors"] = retained
        self.add_log_event(
            event_type="errors_resolved",
            status="resolved",
            stage=stage or self.data.get("stage", ""),
            paper_id=paper_id or "",
            title=title or "",
            message=f"errors_resolved={removed};code={code or '*'}",
            save=False,
        )
        if save:
            self.save()
        return removed

    def resolve_error(self, code, stage="", paper_id="", title=None, save=True):
        return self.resolve_errors(
            code=code,
            stage=stage or None,
            paper_id=paper_id,
            title=title,
            save=save,
        )

    def write_screening_report(self):
        report_path = self.screening_report_path
        papers = sorted(
            self.papers(),
            key=lambda p: _safe_float(p.get("score"), _safe_float(p.get("coarse_score"), 0.0)),
            reverse=True,
        )

        lines = [
            f"# {self.date_key} Screening Results",
            "",
            f"- Provider: `{self.provider}`",
            f"- Providers seen: `{', '.join(self.data.get('providers', []))}`",
            f"- Run modes: `{', '.join(self.data.get('run_modes', []))}`",
            f"- Run state: `{os.path.basename(self.path)}`",
            f"- Papers tracked: {len(papers)}",
            "",
            "| Score | Stage | Source | Forced | Paper ID | Title | Decision | Red Flags |",
            "|---:|---|---|---|---|---|---|---|",
        ]
        for p in papers:
            score = self._score_text(p.get("score", p.get("coarse_score", 0)))
            stage = p.get("screening_stage") or ""
            sources = "+".join(_as_list(p.get("paper_sources"))) or ""
            forced = "yes" if p.get("forced_deep") or p.get("forced_digest") else ""
            paper_id = p.get("paper_id") or ""
            title = str(p.get("title") or "").replace("|", "\\|")
            decision = self._decision_text(p)
            red_flags = ", ".join(p.get("red_flags", []) or [])
            red_flags = red_flags.replace("|", "\\|")
            lines.append(f"| {score} | {stage} | {sources} | {forced} | `{paper_id}` | {title} | {decision} | {red_flags} |")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines).strip() + "\n")
        self.update_artifacts(screening_report=report_path)
        return report_path

    def summary(self):
        return {
            "ok": not self.data.get("errors"),
            "run_id": self.run_id,
            "date": self.date_key,
            "provider": self.provider,
            "providers": self.data.get("providers", []),
            "run_modes": self.data.get("run_modes", []),
            "stage": self.data.get("stage", ""),
            "run_dir": self.run_dir,
            "state_path": self.path,
            "artifacts": self.data.get("artifacts", {}),
            "errors": self.data.get("errors", []),
        }

    def _annotate_paper(self, paper, mode, provider):
        cleaned = self._clean_paper(paper)
        cleaned["paper_sources"] = _merge_unique(cleaned.get("paper_sources"), mode)
        cleaned["provider_sources"] = _merge_unique(cleaned.get("provider_sources"), provider)
        if mode == "single":
            cleaned.setdefault("manual_requested_at", _now())
        if not cleaned.get("best_score_source") and _present(cleaned.get("score")):
            cleaned["best_score_source"] = mode
        return cleaned

    def _merge_paper_lists(self, existing, incoming):
        merged = [self._clean_paper(p) for p in existing or [] if p]
        for paper in incoming or []:
            paper = self._clean_paper(paper)
            key = identity_key(paper)
            for index, current in enumerate(merged):
                if identity_key(current) == key:
                    merged[index] = self._merge_paper_records(current, paper)
                    break
            else:
                merged.append(paper)
        return merged

    def _merge_paper_records(self, current, incoming):
        current = self._clean_paper(current)
        incoming = self._clean_paper(incoming)
        current_score = _safe_float(current.get("score"), -1.0)
        incoming_score = _safe_float(incoming.get("score"), -1.0)
        if incoming_score > current_score:
            primary, secondary = incoming, current
        else:
            primary, secondary = current, incoming

        merged = deepcopy(primary)
        for key, value in secondary.items():
            if key in LIST_FIELDS:
                merged[key] = _merge_unique(secondary.get(key), primary.get(key))
            elif key in OR_FIELDS:
                merged[key] = bool(primary.get(key) or secondary.get(key))
            elif key == "metadata" and isinstance(value, dict):
                metadata = deepcopy(value)
                metadata.update(primary.get("metadata") if isinstance(primary.get("metadata"), dict) else {})
                merged[key] = metadata
            elif not _present(merged.get(key)) and _present(value):
                merged[key] = value

        for key in LIST_FIELDS:
            if key in current or key in incoming:
                merged[key] = _merge_unique(current.get(key), incoming.get(key))
        for key in OR_FIELDS:
            merged[key] = bool(current.get(key) or incoming.get(key))
        if current.get("manual_requested_at") or incoming.get("manual_requested_at"):
            merged["manual_requested_at"] = current.get("manual_requested_at") or incoming.get("manual_requested_at")
        if incoming_score > current_score:
            merged["best_score_source"] = (_as_list(incoming.get("paper_sources")) or [self.provider])[0]
        else:
            merged.setdefault("best_score_source", (_as_list(current.get("paper_sources")) or [self.provider])[0])
        return self._clean_paper(merged)

    def _find_paper(self, paper):
        key = identity_key(paper)
        for existing in self.data.get("papers", []) or []:
            if identity_key(existing) == key:
                return normalize_paper_identity(existing)
        return None

    def _clean_paper(self, paper):
        paper = normalize_paper_identity(paper)
        cleaned = deepcopy(paper)
        cleaned.pop("screening_document_excerpt", None)
        for key, value in list(cleaned.items()):
            if isinstance(value, datetime):
                cleaned[key] = value.isoformat()
            elif hasattr(value, "isoformat"):
                cleaned[key] = value.isoformat()
        return cleaned

    def _decision_text(self, paper):
        parts = []
        if paper.get("in_daily_digest"):
            parts.append("digest")
        if paper.get("selected_for_deep_analysis"):
            parts.append("deep")
        if paper.get("forced_deep"):
            parts.append("forced")
        if paper.get("preserved_deep"):
            parts.append("preserved")
        if paper.get("should_rescreen"):
            parts.append("stage2")
        return ", ".join(parts) if parts else "screened"

    def _score_text(self, value):
        try:
            return f"{float(value):.1f}"
        except Exception:
            return "0.0"

    def _write_errors(self):
        payload = {
            "run_id": self.run_id,
            "date": self.date_key,
            "provider": self.provider,
            "providers": self.data.get("providers", []),
            "run_modes": self.data.get("run_modes", []),
            "stage": self.data.get("stage", ""),
            "errors": self.data.get("errors", []),
        }
        _atomic_write_with_retry(
            self.errors_path,
            json.dumps(payload, ensure_ascii=False, indent=2),
        )

    def _write_log_summary(self):
        lines = [
            f"# Run Log Summary: {self.run_id}",
            "",
            f"- Stage: `{self.data.get('stage', '')}`",
            f"- Provider: `{self.provider}`",
            f"- Providers seen: `{', '.join(self.data.get('providers', []))}`",
            f"- Run modes: `{', '.join(self.data.get('run_modes', []))}`",
            f"- State: `{self.path}`",
            "",
            "| Time | Type | Status | Stage | Paper ID | Title | Provider | Model | Elapsed ms | Retry | Artifact | Message |",
            "|---|---|---|---|---|---|---|---|---:|---:|---|---|",
        ]
        for event in self.data.get("logs", []):
            title = str(event.get("title") or "").replace("|", "\\|")
            artifact = str(event.get("artifact_path") or "").replace("|", "\\|")
            message = str(event.get("message") or "").replace("|", "\\|")
            elapsed = event.get("elapsed_ms")
            elapsed_text = "" if elapsed is None else str(elapsed)
            lines.append(
                "| {created_at} | {event_type} | {status} | {stage} | `{paper_id}` | {title} | {provider} | {model} | {elapsed} | {retry} | {artifact} | {message} |".format(
                    created_at=event.get("created_at", ""),
                    event_type=event.get("event_type", ""),
                    status=event.get("status", ""),
                    stage=event.get("stage", ""),
                    paper_id=event.get("paper_id", ""),
                    title=title,
                    provider=event.get("provider", ""),
                    model=event.get("model", ""),
                    elapsed=elapsed_text,
                    retry=event.get("retry_count", 0),
                    artifact=artifact,
                    message=message,
                )
            )
        _atomic_write_with_retry(self.log_summary_path, "\n".join(lines).strip() + "\n")
