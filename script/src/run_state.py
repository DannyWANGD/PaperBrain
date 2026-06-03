"""Persistent run state and full screening records."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import datetime

from src.paper_identity import identity_key, normalize_paper_identity


class RunState:
    def __init__(self, config, target_date, provider, single_paper=False):
        obsidian = config["obsidian"]
        self.vault_path = obsidian["vault_path"]
        self.folder = os.path.join(self.vault_path, "Run_Records")
        os.makedirs(self.folder, exist_ok=True)
        date_key = target_date.strftime("%Y-%m-%d") if hasattr(target_date, "strftime") else str(target_date)
        suffix = "single" if single_paper else provider
        self.date_key = date_key
        self.provider = provider
        self.path = os.path.join(self.folder, f"{date_key}-{suffix}-run-state.json")
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {
                "date": self.date_key,
                "provider": self.provider,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "updated_at": "",
                "stage": "initialized",
                "papers": [],
                "selection": {},
                "artifacts": {},
            }
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "date": self.date_key,
                "provider": self.provider,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "updated_at": "",
                "stage": "initialized",
                "papers": [],
                "selection": {},
                "artifacts": {},
            }

    def save(self):
        self.data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        tmp_path = f"{self.path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.path)

    def mark_stage(self, stage):
        self.data["stage"] = stage
        self.save()

    def reset(self):
        self.data = {
            "date": self.date_key,
            "provider": self.provider,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": "",
            "stage": "initialized",
            "papers": [],
            "selection": {},
            "artifacts": {},
        }
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
        self.save()

    def write_screening_report(self):
        report_path = os.path.join(self.folder, f"{self.date_key}-{self.provider}-screening-results.md")
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
