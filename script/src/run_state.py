"""Persistent run state and full screening records."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import datetime

from src.paper_identity import identity_key, normalize_paper_identity
from src.paths import PaperBrainPaths


class RunState:
    def __init__(self, config, target_date, provider, single_paper=False):
        paths = PaperBrainPaths.from_config_dict(config)
        date_key = target_date.strftime("%Y-%m-%d") if hasattr(target_date, "strftime") else str(target_date)
        suffix = "single" if single_paper else provider
        self.paths = paths
        self.date_key = date_key
        self.provider = provider
        self.single_paper = single_paper
        self.run_id = f"{date_key}-{suffix}"
        self.folder = str(paths.run_records_dir)
        self.run_dir = str(paths.run_dir(date_key, provider, single_paper))
        self.path = str(paths.state_path(date_key, provider, single_paper))
        self.legacy_path = str(paths.legacy_state_path(date_key, provider, single_paper))
        self.screening_report_path = str(paths.screening_report_path(date_key, provider, single_paper))
        self.log_summary_path = str(paths.log_summary_path(date_key, provider, single_paper))
        self.errors_path = str(paths.errors_path(date_key, provider, single_paper))
        os.makedirs(self.run_dir, exist_ok=True)
        self.data = self._load()
        self._ensure_runtime_fields()
        self.save()

    def _load(self):
        load_path = self.path if os.path.exists(self.path) else self.legacy_path
        if not os.path.exists(load_path):
            return self._empty_data()
        try:
            with open(load_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return self._empty_data()

    def _empty_data(self):
        return {
            "run_id": self.run_id,
            "date": self.date_key,
            "provider": self.provider,
            "single_paper": self.single_paper,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": "",
            "stage": "initialized",
            "papers": [],
            "selection": {},
            "artifacts": {},
            "errors": [],
            "logs": [],
            "paths": {},
        }

    def _ensure_runtime_fields(self):
        self.data.setdefault("run_id", self.run_id)
        self.data.setdefault("date", self.date_key)
        self.data.setdefault("provider", self.provider)
        self.data.setdefault("single_paper", self.single_paper)
        self.data.setdefault("created_at", datetime.now().isoformat(timespec="seconds"))
        self.data.setdefault("updated_at", "")
        self.data.setdefault("stage", "initialized")
        self.data.setdefault("papers", [])
        self.data.setdefault("selection", {})
        self.data.setdefault("artifacts", {})
        self.data.setdefault("errors", [])
        self.data.setdefault("logs", [])
        self.data["paths"] = {
            "run_dir": self.run_dir,
            "state": self.path,
            "legacy_state": self.legacy_path,
            "screening_report": self.screening_report_path,
            "log_summary": self.log_summary_path,
            "errors": self.errors_path,
        }

    def save(self):
        self.data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        tmp_path = f"{self.path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.path)
        self._write_errors()
        self._write_log_summary()

    def mark_stage(self, stage):
        self.data["stage"] = stage
        self.add_log_event(stage=stage, message=f"stage={stage}", save=False)
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
        self.data["papers"] = [self._clean_paper(p) for p in papers]
        self.data["stage"] = stage
        self.save()

    def update_paper(self, paper):
        paper = self._clean_paper(paper)
        key = identity_key(paper)
        papers = self.data.setdefault("papers", [])
        for index, existing in enumerate(papers):
            if identity_key(existing) == key:
                papers[index] = paper
                self.save()
                return
        papers.append(paper)
        self.save()

    def update_selection(self, **kwargs):
        self.data.setdefault("selection", {}).update(kwargs)
        self.save()

    def update_artifacts(self, **kwargs):
        self.data.setdefault("artifacts", {}).update(kwargs)
        for key, value in kwargs.items():
            self.add_log_event(
                stage=self.data.get("stage", ""),
                artifact_path=value,
                message=f"artifact={key}",
                save=False,
            )
        self.save()

    def add_log_event(
        self,
        stage="",
        paper_id="",
        title="",
        provider="",
        model="",
        elapsed_ms=None,
        retry_count=0,
        artifact_path="",
        message="",
        save=True,
    ):
        event = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "stage": stage or self.data.get("stage", ""),
            "paper_id": paper_id,
            "title": title,
            "provider": provider or self.provider,
            "model": model,
            "elapsed_ms": elapsed_ms,
            "retry_count": retry_count,
            "artifact_path": artifact_path or "",
            "message": message,
        }
        self.data.setdefault("logs", []).append(event)
        if save:
            self.save()

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
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "code": code,
            "message": message,
            "suggestion": suggestion,
            "stage": stage or self.data.get("stage", ""),
            "paper_id": paper_id,
            "title": title,
            "exception": exception,
            "retryable": bool(retryable),
        }
        self.data.setdefault("errors", []).append(error)
        self.add_log_event(
            stage=error["stage"],
            paper_id=paper_id,
            title=title,
            message=f"error={code}",
            save=False,
        )
        if save:
            self.save()

    def write_screening_report(self):
        report_path = self.screening_report_path
        papers = sorted(
            self.papers(),
            key=lambda p: float(p.get("score", 0) or 0),
            reverse=True,
        )

        lines = [
            f"# {self.date_key} Screening Results",
            "",
            f"- Provider: `{self.provider}`",
            f"- Run state: `{os.path.basename(self.path)}`",
            f"- Papers tracked: {len(papers)}",
            "",
            "| Score | Stage | Paper ID | Title | Decision | Red Flags |",
            "|---:|---|---|---|---|---|",
        ]
        for p in papers:
            score = self._score_text(p.get("score", 0))
            stage = p.get("screening_stage") or ""
            paper_id = p.get("paper_id") or ""
            title = str(p.get("title") or "").replace("|", "\\|")
            decision = self._decision_text(p)
            red_flags = ", ".join(p.get("red_flags", []) or [])
            red_flags = red_flags.replace("|", "\\|")
            lines.append(f"| {score} | {stage} | `{paper_id}` | {title} | {decision} | {red_flags} |")

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
            "stage": self.data.get("stage", ""),
            "run_dir": self.run_dir,
            "state_path": self.path,
            "artifacts": self.data.get("artifacts", {}),
            "errors": self.data.get("errors", []),
        }

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
            "stage": self.data.get("stage", ""),
            "errors": self.data.get("errors", []),
        }
        tmp_path = f"{self.errors_path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.errors_path)

    def _write_log_summary(self):
        lines = [
            f"# Run Log Summary: {self.run_id}",
            "",
            f"- Stage: `{self.data.get('stage', '')}`",
            f"- Provider: `{self.provider}`",
            f"- State: `{self.path}`",
            "",
            "| Time | Stage | Paper ID | Title | Provider | Model | Elapsed ms | Retry | Artifact | Message |",
            "|---|---|---|---|---|---|---:|---:|---|---|",
        ]
        for event in self.data.get("logs", []):
            title = str(event.get("title") or "").replace("|", "\\|")
            artifact = str(event.get("artifact_path") or "").replace("|", "\\|")
            message = str(event.get("message") or "").replace("|", "\\|")
            elapsed = event.get("elapsed_ms")
            elapsed_text = "" if elapsed is None else str(elapsed)
            lines.append(
                "| {created_at} | {stage} | `{paper_id}` | {title} | {provider} | {model} | {elapsed} | {retry} | {artifact} | {message} |".format(
                    created_at=event.get("created_at", ""),
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
        tmp_path = f"{self.log_summary_path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines).strip() + "\n")
        os.replace(tmp_path, self.log_summary_path)
