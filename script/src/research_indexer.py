import os
import re
import json
import logging
from collections import Counter
from datetime import datetime

import yaml
from src.paper_identity import canonical_arxiv_id, paper_id_from_metadata

logger = logging.getLogger(__name__)


class ResearchIndexer:
    """Builds an Obsidian-native paper index from Research_Notes.

    The index is intentionally based on properties and nested tags instead of
    fixed theme pages, so papers can belong to many facets at the same time.
    """

    DOMAIN_RULES = [
        ("vla", ["vla", "vision-language-action", "vision language action", "openvla", "rt-2", "pi0"]),
        ("world_model", ["world model", "world dynamics", "latent dynamics", "predictive model", "video world model"]),
        ("robot_manipulation", ["manipulation", "robot manipulation", "grasp", "dexterous", "bimanual", "tool use"]),
        ("embodied_ai", ["embodied", "humanoid", "mobile manipulation", "whole-body", "robot system"]),
        ("reinforcement_learning", ["reinforcement learning", "rl", "policy gradient", "actor-critic", "grpo", "ppo", "sac"]),
        ("multimodal_perception", ["multimodal", "vision-language", "vlm", "perception", "point cloud"]),
        ("sim2real", ["sim2real", "sim-to-real", "domain randomization", "domain adaptation"]),
        ("3d_perception", ["3d", "4d", "point cloud", "gaussian", "nerf", "scene reconstruction"]),
    ]

    METHOD_RULES = [
        ("diffusion_policy", ["diffusion policy", "action diffusion", "flow matching", "denoising", "dit policy"]),
        ("latent_world_model", ["latent world model", "rssm", "latent dynamics", "dynamics tokenizer"]),
        ("planning", ["planning", "planner", "mpc", "tree search", "trajectory optimization", "lookahead"]),
        ("reinforcement_learning", ["reinforcement learning", "rl", "grpo", "ppo", "sac", "reward"]),
        ("imitation_learning", ["imitation", "behavior cloning", "demonstration", "offline data"]),
        ("foundation_model", ["foundation model", "llm", "vlm", "pretrained", "large language model"]),
        ("benchmark", ["benchmark", "evaluation suite", "dataset", "leaderboard"]),
        ("simulation", ["simulation", "simulator", "mujoco", "isaac", "synthetic"]),
        ("memory", ["memory", "retrieval", "experience", "long-horizon memory"]),
    ]

    TASK_RULES = [
        ("manipulation", ["manipulation", "pick-and-place", "grasp", "assembly", "tool"]),
        ("dexterous_contact", ["dexterous", "contact-rich", "tactile", "in-hand", "deformable"]),
        ("navigation", ["navigation", "nav", "driving", "autonomous driving", "trajectory"]),
        ("loco_manipulation", ["locomotion", "loco-manipulation", "whole-body", "humanoid"]),
        ("scene_understanding", ["scene understanding", "perception", "reconstruction", "3d", "4d"]),
        ("video_prediction", ["video prediction", "video generation", "future frame", "action-conditioned video"]),
        ("planning_reasoning", ["reasoning", "planning", "chain-of-thought", "task planning"]),
    ]

    PAPER_TYPE_RULES = [
        ("benchmark", ["benchmark", "evaluation suite", "dataset", "leaderboard"]),
        ("dataset", ["dataset", "large-scale data", "data generation"]),
        ("system", ["system", "framework", "platform", "infrastructure", "ros"]),
        ("survey", ["survey", "review", "taxonomy"]),
        ("analysis", ["mechanistic study", "analysis", "probe", "understanding"]),
    ]

    def __init__(self, config):
        self.config = config
        obsidian = config["obsidian"]
        self.vault_path = obsidian["vault_path"]
        self.notes_folder = os.path.join(self.vault_path, obsidian["detailed_notes_folder"])
        self.index_folder = os.path.join(self.vault_path, obsidian.get("research_index_folder", "Research_Index"))
        os.makedirs(self.index_folder, exist_ok=True)

    def build(self, update_notes=True):
        notes = self._scan_notes()
        if update_notes:
            for note in notes:
                self._rewrite_note_frontmatter(note)
        # Re-scan after frontmatter updates so generated files reflect persisted data.
        notes = self._scan_notes()
        self._write_index(notes)
        self._write_tag_guide()
        self._write_reading_queue(notes)
        self._write_review_queue(notes)
        self._write_reproduction_queue(notes)
        self._write_open_questions(notes)
        self._write_base_file()
        logger.info(f"Research index rebuilt: {self.index_folder} ({len(notes)} notes)")
        return notes

    def update_after_new_note(self, note_path=None):
        return self.build(update_notes=True)

    def _scan_notes(self):
        notes = []
        if not os.path.exists(self.notes_folder):
            return notes
        for filename in os.listdir(self.notes_folder):
            if not filename.endswith(".md"):
                continue
            path = os.path.join(self.notes_folder, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    raw = f.read()
                fm, body = self._split_frontmatter(raw)
                note = self._normalize_note(path, filename, fm, body, raw)
                notes.append(note)
            except Exception as e:
                logger.warning(f"Failed to scan note {filename}: {e}")
        notes.sort(key=lambda n: (self._date_sort_key(n.get("publication_date")), n.get("score", 0)), reverse=True)
        return notes

    def _split_frontmatter(self, raw):
        match = re.match(r"^---\n([\s\S]*?)\n---\n?", raw)
        if not match:
            return {}, raw
        try:
            fm = yaml.safe_load(match.group(1)) or {}
        except Exception:
            fm = {}
        return fm, raw[match.end():]

    def _normalize_note(self, path, filename, fm, body, raw):
        title = self._extract_title(body) or self._first_alias(fm) or filename[:-3]
        score = self._to_float(fm.get("score"), 0.0)
        arxiv_id = canonical_arxiv_id(fm.get("arxiv_id") or fm.get("url") or fm.get("pdf_url"))
        paper_id = paper_id_from_metadata({**fm, "title": title})
        pub = str(fm.get("publication_date") or "")
        year = self._extract_year(pub)
        text = " ".join([
            title,
            " ".join(self._ensure_list(fm.get("tags"))),
            self._extract_section(body, "Abstract")[:1500],
            self._extract_section(body, "AI Analysis")[:6000],
        ]).lower()

        domains = sorted(set(self._ensure_list(fm.get("domains")) + self._match_rules(text, self.DOMAIN_RULES)))
        methods = sorted(set(self._ensure_list(fm.get("methods")) + self._match_rules(text, self.METHOD_RULES)))
        tasks = sorted(set(self._ensure_list(fm.get("tasks")) + self._match_rules(text, self.TASK_RULES)))
        paper_type = fm.get("paper_type") or self._infer_paper_type(text)
        impact_band = fm.get("impact_band") or self._impact_band(score)
        reading_status = fm.get("reading_status") or ("read" if fm.get("Reading?") is True else "unread")
        priority_score = self._priority_score(score, domains, methods, tasks, impact_band, reading_status)
        review_status = fm.get("review_status") or self._review_status(domains, methods, tasks)
        next_action = fm.get("next_action") or self._next_action(
            score, paper_type, impact_band, reading_status, review_status, text
        )
        open_question = self._open_question_for_note(
            title=title,
            body=body,
            domains=domains,
            methods=methods,
            tasks=tasks,
            paper_type=paper_type,
        )

        tags = self._normalize_tags(
            self._ensure_list(fm.get("tags")),
            domains=domains,
            methods=methods,
            tasks=tasks,
            paper_type=paper_type,
            impact_band=impact_band,
            reading_status=reading_status,
            review_status=review_status,
        )

        fm_new = dict(fm)
        fm_new.update({
            "tags": tags,
            "domains": domains,
            "methods": methods,
            "tasks": tasks,
            "paper_type": paper_type,
            "impact_band": impact_band,
            "reading_status": reading_status,
            "priority_score": priority_score,
            "review_status": review_status,
            "next_action": next_action,
            "year": year,
        })
        fm_new["score"] = self._format_score(score)
        if arxiv_id:
            fm_new["arxiv_id"] = arxiv_id
        if paper_id:
            fm_new["paper_id"] = paper_id

        return {
            "path": path,
            "filename": filename,
            "note_name": filename[:-3],
            "title": title,
            "frontmatter": fm,
            "frontmatter_new": fm_new,
            "body": body,
            "raw": raw,
            "score": score,
            "arxiv_id": arxiv_id,
            "paper_id": paper_id,
            "publication_date": pub,
            "year": year,
            "domains": domains,
            "methods": methods,
            "tasks": tasks,
            "paper_type": paper_type,
            "impact_band": impact_band,
            "reading_status": reading_status,
            "priority_score": priority_score,
            "review_status": review_status,
            "next_action": next_action,
            "open_question": open_question,
            "tags": tags,
        }

    def _extract_title(self, body):
        m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        return m.group(1).strip() if m else ""

    def _first_alias(self, fm):
        aliases = self._ensure_list(fm.get("aliases"))
        return aliases[0] if aliases else ""

    def _extract_section(self, body, name):
        pattern = rf"^##\s+.*?{re.escape(name)}.*?\n([\s\S]*?)(?=^##\s+|\Z)"
        m = re.search(pattern, body, re.MULTILINE | re.IGNORECASE)
        return m.group(1).strip() if m else ""

    def _extract_heading_section(self, body, names):
        for name in names:
            pattern = rf"^#{{1,6}}\s+.*?{re.escape(name)}.*?\n([\s\S]*?)(?=^#{{1,6}}\s+|\Z)"
            m = re.search(pattern, body, re.MULTILINE | re.IGNORECASE)
            if m and m.group(1).strip():
                return m.group(1).strip()
        return ""

    def _strip_markdown(self, text):
        text = re.sub(r"```[\s\S]*?```", " ", text or "")
        text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
        text = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"`([^`]*)`", r"\1", text)
        text = re.sub(r"(\*\*|__|==|\*)", "", text)
        text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _short_clause(self, text, max_chars=170):
        text = self._strip_markdown(text)
        text = re.sub(r"^\s*\d+[\.)]\s*", "", text)
        text = re.sub(r"^[A-Za-z ]{2,45}:\s*", "", text)
        if not text:
            return ""
        pieces = re.split(r"(?<=[.!?])\s+", text)
        clause = pieces[0].strip() if pieces else text
        if len(clause) < 50 and len(pieces) > 1:
            clause = f"{clause} {pieces[1].strip()}"
        clause = clause.rstrip(".;:")
        if len(clause) <= max_chars:
            return clause
        cut = clause[:max_chars].rsplit(" ", 1)[0].rstrip(",;:")
        return f"{cut}..."

    def _question_focus(self, values, fallback):
        if not values:
            return fallback
        return values[0].replace("_", " ")

    def _extract_existing_question(self, body):
        sections = [
            self._extract_heading_section(body, ["Research Ideas And Open Questions", "Questions For Future Reading", "Limitations And Questions"]),
            self._extract_heading_section(body, ["Future Directions", "Concrete Future Research Ideas", "Task 3"]),
            self._extract_heading_section(body, ["Hidden Limitations", "隐藏局限", "隐性局限"]),
        ]
        text = "\n".join([s for s in sections if s])
        text = self._strip_markdown(text)
        candidates = re.findall(r"([^?。？]{35,260}[?？])", text)
        generic_markers = [
            "what kind of evidence would answer it",
            "questions for future reading",
            "after reading",
            "future papers in this area",
        ]
        for candidate in candidates:
            candidate = candidate.strip(" -")
            low = candidate.lower()
            if any(marker in low for marker in generic_markers):
                continue
            if len(candidate.split()) < 6:
                continue
            return candidate.replace("？", "?")
        return ""

    def _open_question_for_note(self, title, body, domains, methods, tasks, paper_type):
        existing = self._extract_existing_question(body)
        if existing:
            return existing

        problem = self._extract_heading_section(body, ["Problem Statement", "问题陈述"])
        contribution = self._extract_heading_section(body, ["Core Contribution", "核心贡献"])
        rationale = self._extract_heading_section(body, ["Innovation Origin", "创新来源"])
        limitation = self._extract_heading_section(
            body,
            ["Hidden Limitations", "Limitations", "Strengths, Limitations", "Contributions And Limitations", "隐藏局限", "隐性局限"],
        )

        method = self._question_focus(methods, paper_type or "method")
        domain = self._question_focus(domains, "this domain")
        task = self._question_focus(tasks, "the target task")
        problem_clause = self._short_clause(problem, 150)
        contribution_clause = self._short_clause(contribution, 150)
        limitation_clause = self._short_clause(limitation, 150)
        rationale_clause = self._short_clause(rationale, 140)

        if "world_model" in domains or "latent_world_model" in methods:
            if limitation_clause:
                return (
                    f"Can the paper's world-model assumption remain reliable over longer horizons or distribution shifts, "
                    f"given this limitation: {limitation_clause}?"
                )
            if contribution_clause:
                return (
                    f"Does the world-model mechanism in this paper improve planning because it predicts better futures, "
                    f"or because it gives the policy a useful inductive bias: {contribution_clause}?"
                )
        if "vla" in domains:
            if limitation_clause:
                return (
                    f"Which part of the VLA pipeline is the real bottleneck when moving beyond the tested tasks: perception, "
                    f"action generation, temporal prediction, or this limitation: {limitation_clause}?"
                )
            return (
                f"What would convince us that the VLA improvement in {title} transfers to new objects, embodiments, "
                f"and instruction styles rather than fitting the reported benchmark?"
            )
        if "benchmark" in methods or paper_type in ("benchmark", "dataset"):
            if problem_clause:
                return (
                    f"Does this benchmark or dataset actually measure the missing ability described by the problem, "
                    f"or could a simpler shortcut still score well: {problem_clause}?"
                )
            return (
                f"What failure mode would this benchmark or dataset reveal that current evaluations usually hide?"
            )
        if "diffusion_policy" in methods:
            if limitation_clause:
                return (
                    f"How much of the diffusion or flow-policy gain survives when inference speed, contact precision, "
                    f"and this limitation are tested together: {limitation_clause}?"
                )
            return (
                f"Is the diffusion-style action generator mainly helping multimodality, temporal smoothing, or robustness "
                f"under uncertain observations in {task}?"
            )
        if "reinforcement_learning" in methods:
            if limitation_clause:
                return (
                    f"Is the reinforcement-learning signal improving the policy's reasoning/behavior, or mostly exploiting "
                    f"benchmark reward structure under this limitation: {limitation_clause}?"
                )
            return (
                f"What small ablation would separate genuine policy improvement from reward-specific adaptation in this paper?"
            )
        if limitation_clause and contribution_clause:
            return (
                f"Where does the paper's {method} contribution stop being reliable, and what experiment would expose that boundary "
                f"given this limitation: {limitation_clause}?"
            )
        if problem_clause and contribution_clause:
            return (
                f"What evidence would show that the paper's core contribution really solves "
                f"{problem_clause}, rather than only working under the current benchmark setting?"
            )
        if rationale_clause:
            return (
                f"What can be learned from the design rationale behind {title}, and where might that rationale fail "
                f"when the task, embodiment, or data distribution changes?"
            )
        return (
            f"What is the most transferable idea in {title}, and what small experiment would reveal whether it is robust "
            f"outside the paper's original evaluation?"
        )

    def _match_rules(self, text, rules):
        hits = []
        for label, keywords in rules:
            if any(k.lower() in text for k in keywords):
                hits.append(label)
        return hits

    def _infer_paper_type(self, text):
        for label, keywords in self.PAPER_TYPE_RULES:
            if any(k.lower() in text for k in keywords):
                return label
        return "method"

    def _impact_band(self, score):
        if score >= 9.0:
            return "must_read"
        if score >= 8.0:
            return "high_value"
        if score >= 7.0:
            return "solid"
        if score >= 5.0:
            return "watch"
        return "archive"

    def _priority_score(self, score, domains, methods, tasks, impact_band, reading_status):
        priority = int(round(float(score or 0) * 10))
        if impact_band == "must_read":
            priority += 25
        elif impact_band == "high_value":
            priority += 15
        if "vla" in domains and "world_model" in domains:
            priority += 8
        if "robot_manipulation" in domains:
            priority += 4
        if "planning" in methods or "latent_world_model" in methods:
            priority += 4
        if reading_status == "read":
            priority -= 20
        return max(0, priority)

    def _review_status(self, domains, methods, tasks):
        if not domains or not methods or not tasks:
            return "needs_review"
        if len(domains) > 6 or len(methods) > 6:
            return "needs_review"
        return "auto_tagged"

    def _next_action(self, score, paper_type, impact_band, reading_status, review_status, text):
        if review_status == "needs_review":
            return "review_tags"
        if reading_status == "read":
            return "connect_or_summarize"
        if impact_band == "must_read":
            return "deep_read"
        if paper_type in ("benchmark", "dataset", "system"):
            return "inspect_protocol"
        if score >= 8.0 and any(k in text for k in ["github", "code", "implementation", "reproduce"]):
            return "try_reproduce"
        if score >= 7.0:
            return "skim_then_decide"
        return "archive"

    def _normalize_tags(self, raw_tags, domains, methods, tasks, paper_type, impact_band, reading_status, review_status):
        tags = []
        legacy_map = {
            "World_Model": "domain/world_model",
            "Diffusion_Model": "method/diffusion_policy",
            "Embodied_AI": "domain/embodied_ai",
            "3D_Gaussian_Splatting": "domain/3d_perception",
            "Sim2Real": "domain/sim2real",
            "Reinforcement_Learning": "method/reinforcement_learning",
            "Robot_Manipulation": "domain/robot_manipulation",
            "VLA": "domain/vla",
            "Foundation_Model": "method/foundation_model",
            "LLM": "method/foundation_model",
        }
        for tag in raw_tags:
            t = str(tag).strip().lstrip("#").replace(" ", "_")
            if not t:
                continue
            tags.append(legacy_map.get(t, t))
        tags.append("paper")
        tags.extend([f"domain/{x}" for x in domains])
        tags.extend([f"method/{x}" for x in methods])
        tags.extend([f"task/{x}" for x in tasks])
        tags.append(f"type/{paper_type}")
        tags.append(f"impact/{impact_band}")
        tags.append(f"status/{reading_status}")
        tags.append(f"review/{review_status}")
        return sorted(set(tags), key=lambda x: (x != "paper", x))

    def _rewrite_note_frontmatter(self, note):
        existing = note["frontmatter"]
        updated = note["frontmatter_new"]
        if existing == updated:
            return
        raw = note["raw"]
        body = note["body"]
        fm_yaml = yaml.safe_dump(updated, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
        new_raw = f"---\n{fm_yaml}\n---\n\n{body.lstrip()}"
        with open(note["path"], "w", encoding="utf-8") as f:
            f.write(new_raw)

    def _write_index(self, notes):
        total = len(notes)
        high = len([n for n in notes if n["score"] >= 8])
        must = len([n for n in notes if n["impact_band"] == "must_read"])
        unread = len([n for n in notes if n["reading_status"] == "unread"])
        needs_review = len([n for n in notes if n["review_status"] == "needs_review"])
        reproduce = len([
            n for n in notes
            if n["next_action"] in ("try_reproduce", "inspect_protocol")
            or n["paper_type"] in ("benchmark", "dataset", "system")
        ])
        avg = round(sum(n["score"] for n in notes) / total, 2) if total else 0

        domain_counts = self._facet_counts(notes, "domains")
        method_counts = self._facet_counts(notes, "methods")
        task_counts = self._facet_counts(notes, "tasks")

        recent = sorted(notes, key=lambda n: self._date_sort_key(n.get("publication_date")), reverse=True)[:12]
        top = sorted(notes, key=lambda n: n.get("score", 0), reverse=True)[:12]

        content = f"""# Research Index

> PaperBrain 的论文归纳入口：用 Obsidian 原生 properties、nested tags、Bases 与 Dataview 组织论文，而不是固定主题母页。

## Snapshot

| 指标 | 数值 |
|---|---:|
| Total papers | {total} |
| High impact (score >= 8) | {high} |
| Must read (score >= 9) | {must} |
| Unread | {unread} |
| Needs tag review | {needs_review} |
| Reproduction candidates | {reproduce} |
| Average score | {avg} |

## Core Views

- [[Paper_Library.base|Paper Library Base]]
- [[Reading_Queue]]
- [[Review_Queue]]
- [[Reproduction_Queue]]
- [[Open_Questions]]
- [[Tag_Guide]]

## Domain Map

{self._render_count_table(domain_counts, "domain")}

## Method Map

{self._render_count_table(method_counts, "method")}

## Task Map

{self._render_count_table(task_counts, "task")}

## Top Papers

{self._render_note_table(top)}

## Recent Papers

{self._render_note_table(recent)}

## Dataview Queries

### Must Read

```dataview
TABLE priority_score, score, publication_date, domains, methods, tasks, next_action
FROM "Research_Notes"
WHERE contains(file.tags, "#impact/must_read")
SORT priority_score DESC, publication_date DESC
```

### VLA + World Model

```dataview
TABLE priority_score, score, methods, tasks, publication_date, next_action
FROM "Research_Notes"
WHERE contains(file.tags, "#domain/vla") AND contains(file.tags, "#domain/world_model")
SORT priority_score DESC, score DESC
```

### Unread High Value

```dataview
TABLE priority_score, score, domains, methods, tasks, publication_date, next_action
FROM "Research_Notes"
WHERE contains(file.tags, "#status/unread") AND score >= 8
SORT priority_score DESC, publication_date DESC
```

### Notes Needing Tag Review

```dataview
TABLE score, domains, methods, tasks, next_action
FROM "Research_Notes"
WHERE contains(file.tags, "#review/needs_review")
SORT score DESC
```

---
Generated by `script/build_research_index.py` at {datetime.now().strftime("%Y-%m-%d %H:%M")}.
"""
        self._write_file("Research_Index.md", content)

    def _write_tag_guide(self):
        content = """# Tag Guide

PaperBrain uses Obsidian nested tags and properties as the main organization layer. A paper can belong to many facets at once, so do not force it into a single topic.

## Tag Families

- `domain/...`: research area, such as `domain/vla`, `domain/world_model`, `domain/robot_manipulation`.
- `method/...`: core method, such as `method/diffusion_policy`, `method/planning`, `method/reinforcement_learning`.
- `task/...`: task or setting, such as `task/manipulation`, `task/navigation`, `task/video_prediction`.
- `type/...`: paper type, such as `type/method`, `type/benchmark`, `type/dataset`, `type/system`.
- `impact/...`: reading priority, such as `impact/must_read`, `impact/high_value`, `impact/solid`.
- `status/...`: reading status, such as `status/unread`, `status/reading`, `status/read`.
- `review/...`: tag quality, such as `review/auto_tagged`, `review/needs_review`.

## Properties Worth Editing

- `reading_status`: change this to `reading` or `read` as you work through papers.
- `next_action`: use this as your next research move, for example `deep_read`, `try_reproduce`, `inspect_protocol`, or `review_tags`.
- `review_status`: set to `auto_tagged` after you manually verify tags.
- `priority_score`: generated ranking signal; usually do not edit manually.

## Obsidian Usage

Obsidian nested tags can be searched directly. For example, search `tag:domain/vla` to find VLA papers. In Bases, use tag filters or formulas such as `file.hasTag("domain/vla")` when you want parent/child tag-aware filtering.

Use the generated `Paper_Library.base` for day-to-day browsing. Use `Review_Queue` when tags look too broad or incomplete. Use `Reproduction_Queue` when you want a practical coding or reproduction target.
"""
        self._write_file("Tag_Guide.md", content)

    def _write_reading_queue(self, notes):
        unread = [n for n in notes if n["reading_status"] == "unread"]
        unread.sort(key=lambda n: (n["priority_score"], n["score"], self._date_sort_key(n.get("publication_date"))), reverse=True)
        content = f"""# Reading Queue

## Next Papers

{self._render_note_table(unread[:30])}

## Must Read, Unread

```dataview
TABLE priority_score, score, domains, methods, tasks, next_action, publication_date
FROM "Research_Notes"
WHERE contains(file.tags, "#status/unread") AND contains(file.tags, "#impact/must_read")
SORT priority_score DESC, publication_date DESC
```

## High Value, Unread

```dataview
TABLE priority_score, score, domains, methods, tasks, next_action, publication_date
FROM "Research_Notes"
WHERE contains(file.tags, "#status/unread") AND score >= 8
SORT priority_score DESC, publication_date DESC
```
"""
        self._write_file("Reading_Queue.md", content)

    def _write_review_queue(self, notes):
        review = [n for n in notes if n["review_status"] == "needs_review"]
        review.sort(key=lambda n: (n["score"], len(n["domains"]) + len(n["methods"]) + len(n["tasks"])), reverse=True)
        content = f"""# Review Queue

These notes need manual tag/property review. They usually have missing facets or too many automatically inferred tags.

## Needs Review

{self._render_note_table(review[:40])}

```dataview
TABLE score, domains, methods, tasks, next_action
FROM "Research_Notes"
WHERE contains(file.tags, "#review/needs_review")
SORT score DESC
```
"""
        self._write_file("Review_Queue.md", content)

    def _write_reproduction_queue(self, notes):
        candidates = [
            n for n in notes
            if n["next_action"] in ("try_reproduce", "inspect_protocol") or n["paper_type"] in ("benchmark", "dataset", "system")
        ]
        candidates.sort(key=lambda n: (n["priority_score"], n["score"], self._date_sort_key(n.get("publication_date"))), reverse=True)
        content = f"""# Reproduction Queue

Use this page when you want a practical implementation, benchmark, or protocol-reading target.

## Candidates

{self._render_note_table(candidates[:40])}

```dataview
TABLE priority_score, score, paper_type, domains, methods, tasks, github, project_page, next_action
FROM "Research_Notes"
WHERE next_action = "try_reproduce" OR next_action = "inspect_protocol" OR paper_type = "benchmark" OR paper_type = "dataset" OR paper_type = "system"
SORT priority_score DESC, score DESC
```
"""
        self._write_file("Reproduction_Queue.md", content)

    def _write_open_questions(self, notes):
        high_value = [n for n in notes if n["score"] >= 8]
        high_value.sort(key=lambda n: (n["priority_score"], n["score"]), reverse=True)
        lines = []
        for n in high_value[:25]:
            facets = ", ".join((n.get("domains") or [])[:2] + (n.get("methods") or [])[:2])
            facet_text = f" ({facets})" if facets else ""
            question = n.get("open_question") or self._open_question_for_note(
                title=n["title"],
                body=n["body"],
                domains=n["domains"],
                methods=n["methods"],
                tasks=n["tasks"],
                paper_type=n["paper_type"],
            )
            lines.append(
                f"- [ ] [[{n['note_name']}]]{facet_text}: {question} "
                f"`score:{self._format_score(n['score'])}` `next:{n['next_action']}`"
            )
        content = f"""# Open Questions

This page turns high-value papers into one concrete question each. The question should point to the paper's own method, evidence, limitation, or transferable idea instead of repeating a generic reading prompt.

## Question Capture

{os.linesep.join(lines) if lines else "- No high-value papers yet."}

## Dataview: High-Value Papers To Reflect On

```dataview
TABLE priority_score, score, domains, methods, tasks, reading_status
FROM "Research_Notes"
WHERE score >= 8
SORT priority_score DESC, score DESC
```
"""
        self._write_file("Open_Questions.md", content)

    def _write_base_file(self):
        content = """views:
  - type: table
    name: All Papers
    filters:
      and:
        - file.inFolder("Research_Notes")
    order:
      - file.name
      - priority_score
      - score
      - impact_band
      - reading_status
      - next_action
      - review_status
      - domains
      - methods
      - tasks
      - paper_type
      - publication_date
      - institutions
      - github
      - project_page
      - local_pdf
    sort:
      - property: priority_score
        direction: DESC
      - property: score
        direction: DESC
      - property: publication_date
        direction: DESC
  - type: cards
    name: Reading Queue
    filters:
      and:
        - file.inFolder("Research_Notes")
        - note.reading_status != "read"
        - note.score >= 7
    order:
      - file.name
      - priority_score
      - score
      - impact_band
      - next_action
      - domains
      - methods
      - tasks
      - publication_date
    sort:
      - property: priority_score
        direction: DESC
      - property: score
        direction: DESC
    cardSize: 300
  - type: table
    name: Must Read
    filters:
      and:
        - file.inFolder("Research_Notes")
        - note.impact_band == "must_read"
    order:
      - file.name
      - priority_score
      - score
      - next_action
      - domains
      - methods
      - tasks
      - publication_date
    sort:
      - property: publication_date
        direction: DESC
  - type: table
    name: Reproduction
    filters:
      and:
        - file.inFolder("Research_Notes")
        - note.score >= 7
    order:
      - file.name
      - priority_score
      - score
      - paper_type
      - next_action
      - github
      - project_page
      - domains
      - methods
      - tasks
    sort:
      - property: priority_score
        direction: DESC
  - type: table
    name: Needs Review
    filters:
      and:
        - file.inFolder("Research_Notes")
        - note.review_status == "needs_review"
    order:
      - file.name
      - score
      - domains
      - methods
      - tasks
      - next_action
    sort:
      - property: score
        direction: DESC
"""
        self._write_file("Paper_Library.base", content)

    def _facet_counts(self, notes, field):
        counter = Counter()
        for note in notes:
            counter.update(note.get(field, []))
        return counter

    def _render_count_table(self, counter, prefix):
        if not counter:
            return "_No data yet._"
        lines = ["| Tag | Count |", "|---|---:|"]
        for key, count in counter.most_common():
            lines.append(f"| `#{prefix}/{key}` | {count} |")
        return "\n".join(lines)

    def _render_note_table(self, notes):
        if not notes:
            return "_No papers yet._"
        lines = ["| Paper | Score | Tags | Date |", "|---|---:|---|---|"]
        for n in notes:
            tags = " ".join([f"`#{t}`" for t in n["tags"] if t.startswith(("domain/", "method/", "task/"))][:6])
            lines.append(
                f"| [[{n['note_name']}]] | {self._format_score(n['score'])} | {tags} | {n.get('publication_date') or ''} |"
            )
        return "\n".join(lines)

    def _write_file(self, filename, content):
        path = os.path.join(self.index_folder, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _ensure_list(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return [str(x) for x in value if x is not None and str(x).strip()]
        return [str(value)] if str(value).strip() else []

    def _to_int(self, value, default=0):
        try:
            return int(float(value))
        except Exception:
            return default

    def _to_float(self, value, default=0.0):
        try:
            return round(float(value), 1)
        except Exception:
            return default

    def _format_score(self, value):
        try:
            return f"{float(value):.1f}"
        except Exception:
            return "0.0"

    def _extract_year(self, publication_date):
        m = re.search(r"(19|20)\d{2}", str(publication_date or ""))
        return int(m.group(0)) if m else None

    def _date_sort_key(self, publication_date):
        value = str(publication_date or "")
        if not re.match(r"^\d{4}-\d{2}-\d{2}", value):
            return ""
        return value
