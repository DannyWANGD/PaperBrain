from __future__ import annotations

import os
import re
from collections import Counter
from datetime import date as Date
from datetime import datetime, timedelta

from src.paper_identity import canonical_arxiv_id, paper_id_from_arxiv_id
from src.paths import PaperBrainPaths
from src.research_indexer import ResearchIndexer


MANUAL_HEADING = "## 9. Manual Notes"
MANUAL_START = "<!-- paperbrain:manual:start -->"
MANUAL_END = "<!-- paperbrain:manual:end -->"


class ResearchBriefGenerator:
    """Generate Obsidian research briefs from existing deep paper notes."""

    def __init__(self, config):
        self.config = config
        paths = PaperBrainPaths.from_config_dict(config)
        self.vault_path = str(paths.vault_path)
        self.brief_folder = str(paths.research_brief_dir)
        self.daily_folder = str(paths.daily_digest_dir)
        os.makedirs(self.brief_folder, exist_ok=True)
        self.indexer = ResearchIndexer(config)

    def generate(
        self,
        start_date,
        end_date,
        period_label=None,
        brief_type="range",
        max_top=8,
        max_questions=10,
    ):
        start_date = _coerce_date(start_date)
        end_date = _coerce_date(end_date)
        if end_date < start_date:
            raise ValueError("end_date must be on or after start_date")

        period_label = period_label or f"{start_date.isoformat()}_to_{end_date.isoformat()}"
        filename = f"{self._safe_filename(period_label)}-ResearchBrief.md"
        path = os.path.join(self.brief_folder, filename)
        manual_notes = self._extract_manual_notes(path)
        notes = self._notes_in_range(start_date, end_date)
        content = self._render_brief(
            notes=notes,
            start_date=start_date,
            end_date=end_date,
            period_label=period_label,
            brief_type=brief_type,
            max_top=max_top,
            max_questions=max_questions,
            manual_notes=manual_notes,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _notes_in_range(self, start_date, end_date):
        all_notes = [self._normalize_brief_note(note) for note in self.indexer._scan_notes()]
        note_lookup = self._build_note_lookup(all_notes)
        notes_by_key = {}

        for note in all_notes:
            note_date = self._note_date(note)
            if note_date and start_date <= note_date <= end_date:
                key = self._identity_key(note)
                if key:
                    notes_by_key[key] = note

        notes_by_period_key = {}
        consumed_note_keys = set()
        for digest_note in self._daily_digest_notes_in_range(start_date, end_date):
            note = self._match_existing_note(digest_note, note_lookup)
            merged = self._merge_digest_and_note(digest_note, note) if note else digest_note
            key = self._identity_key(merged)
            if note:
                consumed_note_keys.add(self._identity_key(note))
            if key in notes_by_period_key:
                notes_by_period_key[key] = self._merge_digest_and_note(notes_by_period_key[key], merged)
            else:
                notes_by_period_key[key] = merged

        for key, note in notes_by_key.items():
            if key not in consumed_note_keys and key not in notes_by_period_key:
                notes_by_period_key[key] = note

        notes = list(notes_by_period_key.values())
        notes.sort(key=lambda n: (n.get("score", 0), n.get("priority_score", 0)), reverse=True)
        return notes

    def _daily_digest_notes_in_range(self, start_date, end_date):
        notes = []
        current = start_date
        while current <= end_date:
            path = os.path.join(self.daily_folder, f"{current.isoformat()}-PaperDigest.md")
            if os.path.exists(path):
                notes.extend(self._parse_daily_digest(path, current))
            current += timedelta(days=1)
        return notes

    def _parse_daily_digest(self, path, publication_date):
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
        except Exception:
            return []

        notes = []
        chunks = re.split(r"(?m)^###\s+", raw)
        for chunk in chunks[1:]:
            header, _, body = chunk.partition("\n")
            match = re.match(r"(.+?)\s*\(Score:\s*([0-9]+(?:\.[0-9]+)?)/10\)", header.strip())
            if not match:
                continue
            title = self._clean_digest_title(match.group(1))
            score = _to_float(match.group(2), 0.0)
            innovation = self._digest_field(body, "Innovation")
            limitations = self._digest_field(body, "Limitations")
            link_text = self._digest_field(body, "Link")
            institutions = self._split_csv(self._digest_field(body, "Institutions"))
            tags = self._digest_tags(body)
            arxiv_id = canonical_arxiv_id(link_text)
            paper_id = paper_id_from_arxiv_id(arxiv_id) if arxiv_id else ""
            domains, methods, tasks, paper_type = self._facets_from_tags(tags)
            link_note_name = self._extract_wikilink_target(link_text)
            note_name = link_note_name or self._safe_wikilink_title(title)
            body_text = "\n\n".join([
                f"## Abstract\n{innovation}",
                f"## Core Contribution\n{innovation}",
                f"## Limitations\n{limitations}",
            ])
            notes.append({
                "path": "",
                "filename": f"{note_name}.md",
                "note_name": note_name,
                "title": title,
                "frontmatter": {
                    "institutions": institutions,
                    "source_digest": path,
                    "url": self._extract_first_url(link_text),
                },
                "body": body_text,
                "raw": body_text,
                "score": score,
                "arxiv_id": arxiv_id,
                "paper_id": paper_id,
                "link_note_name": link_note_name,
                "publication_date": publication_date.isoformat(),
                "year": publication_date.year,
                "domains": domains,
                "methods": methods,
                "tasks": tasks,
                "paper_type": paper_type,
                "impact_band": self._impact_band(score),
                "reading_status": "unread",
                "priority_score": int(round(score * 10)),
                "review_status": "auto_tagged" if tags else "needs_review",
                "next_action": "deep_read" if score >= 8.0 else "skim_then_decide" if score >= 7.0 else "archive",
                "open_question": "",
                "tags": tags,
            })
        return notes

    def _merge_digest_and_note(self, digest_note, note):
        merged = dict(digest_note)
        for key, value in note.items():
            if key in {"domains", "methods", "tasks", "tags"}:
                merged[key] = self._merge_unique(merged.get(key), value)
            elif key == "frontmatter":
                fm = dict(merged.get("frontmatter") or {})
                fm.update(value or {})
                merged[key] = fm
            elif self._present(value):
                merged[key] = value
        merged["score"] = max(_to_float(digest_note.get("score"), 0.0), _to_float(note.get("score"), 0.0))
        return merged

    def _normalize_brief_note(self, note):
        normalized = dict(note or {})
        filename = str(normalized.get("filename") or "").strip()
        if filename and not normalized.get("note_name"):
            normalized["note_name"] = filename[:-3] if filename.endswith(".md") else filename
        if not normalized.get("note_name") and normalized.get("path"):
            filename = os.path.basename(str(normalized["path"]))
            normalized["filename"] = filename
            normalized["note_name"] = filename[:-3] if filename.endswith(".md") else filename
        return normalized

    def _build_note_lookup(self, notes):
        lookup = {}
        for note in notes:
            for key in self._lookup_keys(note):
                lookup.setdefault(key, note)
        return lookup

    def _match_existing_note(self, digest_note, note_lookup):
        for key in self._lookup_keys(digest_note):
            note = note_lookup.get(key)
            if note:
                return note
        return None

    def _identity_key(self, note):
        paper_id = str(note.get("paper_id") or "").strip().lower()
        if paper_id:
            return paper_id
        frontmatter = note.get("frontmatter") or {}
        arxiv_id = canonical_arxiv_id(
            note.get("arxiv_id")
            or note.get("url")
            or note.get("pdf_url")
            or frontmatter.get("arxiv_id")
            or frontmatter.get("url")
            or frontmatter.get("pdf_url")
            or note.get("paper_id")
        )
        if arxiv_id:
            return f"arxiv:{arxiv_id}"
        return self._lookup_key(note.get("title") or note.get("note_name"))

    def _lookup_keys(self, note):
        keys = []
        frontmatter = note.get("frontmatter") or {}
        values = [
            note.get("paper_id"),
            note.get("arxiv_id"),
            note.get("url"),
            note.get("pdf_url"),
            frontmatter.get("arxiv_id"),
            frontmatter.get("url"),
            frontmatter.get("pdf_url"),
            note.get("note_name"),
            note.get("filename"),
            note.get("link_note_name"),
            note.get("title"),
            frontmatter.get("title"),
            frontmatter.get("short_title"),
        ]
        values.extend(self._ensure_list(frontmatter.get("aliases")))
        for value in values:
            arxiv_id = canonical_arxiv_id(value)
            if arxiv_id:
                keys.append(f"arxiv:{arxiv_id}")
            key = self._lookup_key(value)
            if key:
                keys.append(key)
        return keys

    def _lookup_key(self, value):
        value = str(value or "").strip()
        if not value:
            return ""
        value = self._extract_wikilink_target(value) or value
        if value.endswith(".md"):
            value = value[:-3]
        return self._clean_text(value).casefold()

    def _digest_field(self, body, label):
        pattern = rf"-\s+\*\*[^*\n]*{re.escape(label)}\*\*:\s*([\s\S]*?)(?=\n-\s+\*\*|\n---|\Z)"
        match = re.search(pattern, body, flags=re.IGNORECASE)
        return self._clean_text(match.group(1)) if match else ""

    def _digest_tags(self, body):
        tags = []
        for tag in re.findall(r"#([A-Za-z0-9_/-]+)", body):
            normalized = tag.strip().replace("_", "_")
            if normalized and normalized not in tags:
                tags.append(normalized)
        if "paper" not in tags:
            tags.insert(0, "paper")
        return tags

    def _facets_from_tags(self, tags):
        domains = []
        methods = []
        tasks = []
        paper_type = "method"
        for tag in tags:
            if tag.startswith("domain/"):
                domains.append(tag.split("/", 1)[1])
            elif tag.startswith("method/"):
                methods.append(tag.split("/", 1)[1])
            elif tag.startswith("task/"):
                tasks.append(tag.split("/", 1)[1])
            elif tag.startswith("type/") and paper_type == "method":
                paper_type = tag.split("/", 1)[1]
        return sorted(set(domains)), sorted(set(methods)), sorted(set(tasks)), paper_type

    def _clean_digest_title(self, title):
        title = re.sub(r"^[^\w]+", "", str(title or ""), flags=re.UNICODE).strip()
        return self._clean_text(title)

    def _safe_wikilink_title(self, title):
        cleaned = re.sub(r"[\\/:*?\"<>|#^\[\]]+", "", str(title or "")).strip()
        return cleaned[:120].strip() or "Untitled Paper"

    def _extract_wikilink_target(self, text):
        match = re.search(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]*)?\]\]", str(text or ""))
        if not match:
            return ""
        target = match.group(1).strip()
        return target[:-3] if target.endswith(".md") else target

    def _extract_first_url(self, text):
        match = re.search(r"https?://[^)\s]+", str(text or ""))
        return match.group(0) if match else ""

    def _split_csv(self, text):
        text = self._clean_text(text)
        if not text or text.lower() == "unknown":
            return []
        return [item.strip() for item in text.split(",") if item.strip()]

    def _merge_unique(self, *values):
        merged = []
        seen = set()
        for value in values:
            for item in self._ensure_list(value):
                key = str(item).strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    merged.append(item)
        return merged

    def _present(self, value):
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, (list, tuple, dict)) and not value:
            return False
        return True

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

    def _render_brief(self, notes, start_date, end_date, period_label, brief_type, max_top, max_questions, manual_notes=""):
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        top_notes = notes[:max_top]
        avg_score = self._average_score(notes)
        high_count = len([n for n in notes if n.get("score", 0) >= 8.0])
        domain_counts = self._facet_counts(notes, "domains")
        method_counts = self._facet_counts(notes, "methods")
        task_counts = self._facet_counts(notes, "tasks")

        return "\n".join([
            "---",
            "tags:",
            "  - research_brief",
            f"  - period/{brief_type}",
            f'brief_type: "{brief_type}"',
            f'start_date: "{start_date.isoformat()}"',
            f'end_date: "{end_date.isoformat()}"',
            f"paper_count: {len(notes)}",
            f'generated_at: "{generated_at}"',
            "---",
            "",
            f"# Research Brief: {period_label}",
            "",
            f"**Period**: {start_date.isoformat()} to {end_date.isoformat()}",
            f"**Papers covered**: {len(notes)}",
            "",
            "## 1. Executive Summary",
            "",
            self._executive_summary(notes, avg_score, high_count, domain_counts, method_counts),
            "",
            "## 2. Top Papers This Period",
            "",
            self._top_papers(top_notes),
            "",
            "## 3. Research Trend Map",
            "",
            self._trend_map(domain_counts, method_counts, task_counts),
            "",
            "## 4. Novel Signals",
            "",
            self._novel_signals(top_notes),
            "",
            "## 5. Repeated Patterns And Saturation",
            "",
            self._repeated_patterns(notes, domain_counts, method_counts, task_counts),
            "",
            "## 6. Evidence Quality",
            "",
            self._evidence_quality(notes),
            "",
            "## 7. Reading Plan For Next Period",
            "",
            self._reading_plan(top_notes),
            "",
            "## 8. Open Research Questions",
            "",
            self._open_questions(top_notes, max_questions),
            "",
            self._manual_section(manual_notes),
            "",
        ])

    def _executive_summary(self, notes, avg_score, high_count, domain_counts, method_counts):
        if not notes:
            return (
                "No daily digest entries or deep-analysis notes fall inside this period. Treat this brief as a calendar "
                "placeholder, then generate or import paper data before using it for trend tracking."
            )

        leading_domains = self._format_counter(domain_counts, limit=3) or "no dominant domain"
        leading_methods = self._format_counter(method_counts, limit=3) or "no dominant method family"
        count = len(notes)
        plural = "paper" if count == 1 else "papers"
        high_phrase = f"{high_count} reached the high-value band" if high_count else "none reached the high-value band"

        first = (
            f"This period contains {count} {plural}, with an average score of **{avg_score:.1f}/10**; "
            f"{high_phrase}. The strongest visible domains are {leading_domains}, while the most repeated method "
            f"signals are {leading_methods}."
        )
        second = (
            "The practical reading priority is to separate durable mechanisms from attractive but narrow demonstrations. "
            "Start from the highest-scoring papers, then compare their evidence, baselines, code availability, and failure "
            "cases before turning any single result into a research direction."
        )
        return f"{first}\n\n{second}"

    def _top_papers(self, notes):
        if not notes:
            return "_No top papers are available for this period._"

        rows = [
            "| Rank | Paper | Score | Institutions | Why It Matters |",
            "| --- | --- | ---: | --- | --- |",
        ]
        for idx, note in enumerate(notes, start=1):
            rows.append(
                "| {rank} | {paper} | {score:.1f} | {institutions} | {why} |".format(
                    rank=idx,
                    paper=self._paper_link(note),
                    score=note.get("score", 0.0),
                    institutions=self._table_cell(self._institutions(note)),
                    why=self._table_cell(self._why_it_matters(note)),
                )
            )
        return "\n".join(rows)

    def _trend_map(self, domain_counts, method_counts, task_counts):
        rows = [
            "| Facet | Main Signals |",
            "| --- | --- |",
            f"| Domains | {self._format_counter(domain_counts, limit=6) or 'Not enough signal yet'} |",
            f"| Methods | {self._format_counter(method_counts, limit=6) or 'Not enough signal yet'} |",
            f"| Tasks | {self._format_counter(task_counts, limit=6) or 'Not enough signal yet'} |",
        ]
        return "\n".join(rows)

    def _novel_signals(self, notes):
        if not notes:
            return "_No novel signals can be extracted yet._"

        paragraphs = []
        for note in notes[:5]:
            method = self._first(note.get("methods")) or note.get("paper_type") or "method"
            domain = self._first(note.get("domains")) or "its target domain"
            clue = self._section_clause(note, ["Core Contribution", "Innovation Origin", "Abstract"], 230)
            if not clue:
                clue = self._why_it_matters(note)
            paragraphs.append(
                f"**{self._paper_link(note)}** is a useful signal for **{domain.replace('_', ' ')}** because "
                f"it pushes on **{method.replace('_', ' ')}** rather than only reporting another benchmark number. "
                f"{self._clean_text(clue)}"
            )
        return "\n\n".join(paragraphs)

    def _repeated_patterns(self, notes, domain_counts, method_counts, task_counts):
        if not notes:
            return "_No repeated patterns are visible without notes in the selected period._"

        repeated = [
            (name, count, "domain") for name, count in domain_counts.items() if count >= 2
        ] + [
            (name, count, "method") for name, count in method_counts.items() if count >= 2
        ] + [
            (name, count, "task") for name, count in task_counts.items() if count >= 2
        ]
        repeated.sort(key=lambda item: item[1], reverse=True)

        if not repeated:
            return (
                "The selected papers are still dispersed, so saturation is not yet a strong conclusion. "
                "Use this range mainly for exploration, then revisit the same facets after more notes accumulate."
            )

        top = repeated[:5]
        lines = []
        for name, count, facet in top:
            clean = name.replace("_", " ")
            lines.append(
                f"**{clean}** appears as a repeated {facet} signal in {count} papers. This is worth tracking, "
                "but it should be treated as a pattern to verify through evidence quality rather than as automatic progress."
            )
        limitation = self._common_limitation(notes)
        if limitation:
            lines.append(
                f"A recurring caution is: {limitation} This should guide which claims deserve close reading first."
            )
        return "\n\n".join(lines)

    def _evidence_quality(self, notes):
        if not notes:
            return "_Evidence quality cannot be assessed for an empty period._"

        code_count = len([n for n in notes if self._has_value(n, "github")])
        project_count = len([n for n in notes if self._has_value(n, "project_page")])
        institution_count = len([n for n in notes if self._institutions(n) != "Unknown"])
        keyword_counts = Counter()
        for note in notes:
            text = note.get("body", "").lower()
            for label, pattern in [
                ("real robot", r"real[- ]?robot|real world|hardware"),
                ("simulation", r"simulation|simulator|mujoco|isaac"),
                ("ablation", r"ablation"),
                ("baseline", r"baseline"),
                ("benchmark", r"benchmark"),
            ]:
                if re.search(pattern, text):
                    keyword_counts[label] += 1

        table = "\n".join([
            "| Evidence Signal | Count |",
            "| --- | ---: |",
            f"| Code link available | {code_count}/{len(notes)} |",
            f"| Project page available | {project_count}/{len(notes)} |",
            f"| Institutions identified | {institution_count}/{len(notes)} |",
            f"| Real-world or hardware evidence mentioned | {keyword_counts['real robot']}/{len(notes)} |",
            f"| Simulation evidence mentioned | {keyword_counts['simulation']}/{len(notes)} |",
            f"| Ablation mentioned | {keyword_counts['ablation']}/{len(notes)} |",
            f"| Baseline mentioned | {keyword_counts['baseline']}/{len(notes)} |",
        ])
        comment = (
            "Use this table as a reading filter. Papers with strong scores but weak evidence metadata should be read with "
            "extra attention to protocol details, benchmark fairness, and whether the reported setting matches your research use case."
        )
        return f"{table}\n\n{comment}"

    def _reading_plan(self, notes):
        if not notes:
            return "_No reading plan can be built for this period._"

        lines = []
        for idx, note in enumerate(notes[:5], start=1):
            action = str(note.get("next_action") or "read_deeply").replace("_", " ")
            reason = self._why_it_matters(note)
            lines.append(f"{idx}. Read {self._paper_link(note)} for **{action}**. {reason}")
        return "\n".join(lines)

    def _open_questions(self, notes, max_questions):
        if not notes:
            return "_No open questions are available yet._"

        questions = []
        for note in notes:
            question = self._question_for_note(note)
            if question and question not in questions:
                questions.append((note, question))
            if len(questions) >= max_questions:
                break

        if not questions:
            return "_No paper-specific open questions were found in the selected notes._"

        return "\n".join([
            f"{idx}. **{self._paper_link(note)}**: {question}"
            for idx, (note, question) in enumerate(questions, start=1)
        ])

    def _paper_link(self, note):
        return f"[[{self._display_note_name(note)}]]"

    def _display_note_name(self, note):
        note_name = str(note.get("note_name") or "").strip()
        if note_name:
            return note_name[:-3] if note_name.endswith(".md") else note_name
        filename = str(note.get("filename") or "").strip()
        if filename:
            return filename[:-3] if filename.endswith(".md") else filename
        return self._safe_wikilink_title(note.get("title") or "Untitled Paper")

    def _facet_counts(self, notes, field):
        counter = Counter()
        for note in notes:
            counter.update(note.get(field) or [])
        return counter

    def _format_counter(self, counter, limit=5):
        values = []
        for name, count in counter.most_common(limit):
            values.append(f"`{name}` ({count})")
        return ", ".join(values)

    def _average_score(self, notes):
        if not notes:
            return 0.0
        return round(sum(float(n.get("score", 0.0) or 0.0) for n in notes) / len(notes), 1)

    def _note_date(self, note):
        return _parse_date(note.get("publication_date"))

    def _institutions(self, note):
        frontmatter = note.get("frontmatter") or {}
        institutions = self._ensure_list(frontmatter.get("institutions"))
        return self._clean_text(", ".join(institutions)) if institutions else "Unknown"

    def _why_it_matters(self, note):
        contribution = self._section_clause(note, ["Core Contribution", "Problem Statement", "Abstract"], 180)
        if contribution:
            return self._clean_text(contribution)
        facets = (note.get("domains") or [])[:2] + (note.get("methods") or [])[:2]
        if facets:
            clean = ", ".join([f.replace("_", " ") for f in facets])
            return f"It is relevant because it connects directly to {clean}."
        return "It is relevant because it entered the selected period with a high score."

    def _common_limitation(self, notes):
        clauses = []
        for note in notes:
            clause = self._section_clause(
                note,
                ["Limitations", "Critical Assessment", "Hidden Limitations", "Evidence Quality"],
                180,
            )
            if clause and not self._is_weak_limitation_clause(clause):
                clauses.append(clause)
        return self._clean_text(clauses[0]) if clauses else ""

    def _section_clause(self, note, section_names, max_chars):
        body = note.get("body", "")
        for name in section_names:
            section = self.indexer._extract_heading_section(body, [name])
            if section:
                return self._clean_text(self.indexer._short_clause(section, max_chars))
        return ""

    def _question_for_note(self, note):
        candidate = self._extract_question_sentence(note.get("open_question") or "")
        if candidate and not self._is_low_quality_question(candidate):
            return candidate
        return self._fallback_question(note)

    def _extract_question_sentence(self, text):
        text = self._clean_text(self.indexer._strip_markdown(text or ""))
        text = re.sub(r">\s*\[!question\]\s*Open Question\s*>?", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text).strip()
        if not text or "[!" in text or ">" in text:
            return ""
        starts = r"(?:What|How|Why|Which|Can|Could|Does|Do|Is|Are|When|Where|To what extent)"
        matches = re.findall(rf"\b({starts}[^?]{{20,260}}\?)", text, flags=re.IGNORECASE)
        if matches:
            return self._clean_text(matches[0])
        if re.match(rf"^{starts}\b", text, flags=re.IGNORECASE) and "?" in text and len(text) <= 280:
            return self._clean_text(text[:text.index("?") + 1])
        return ""

    def _is_low_quality_question(self, question):
        low = question.lower()
        bad_markers = [
            "evidence supports three contributions",
            "strengths.",
            "[!question]",
            "open question",
        ]
        return any(marker in low for marker in bad_markers)

    def _is_weak_limitation_clause(self, clause):
        low = clause.lower()
        bad_markers = [
            "strengths.",
            "evidence supports",
            "contributions:",
            "the paper presents evidence",
        ]
        return any(marker in low for marker in bad_markers)

    def _fallback_question(self, note):
        title = self._display_note_name(note) or "this paper"
        domains = set(note.get("domains") or [])
        methods = set(note.get("methods") or [])
        if "world_model" in domains or "latent_world_model" in methods:
            return (
                f"Can the world-model mechanism in {title} stay reliable under longer horizons, "
                "distribution shifts, and real-robot noise?"
            )
        if "vla" in domains:
            return (
                f"What evidence would show that {title} transfers beyond the reported tasks, objects, "
                "embodiments, and instruction styles?"
            )
        if "benchmark" in methods or note.get("paper_type") in {"benchmark", "dataset"}:
            return (
                f"What failure mode does {title} reveal that standard benchmarks or datasets usually hide?"
            )
        method = self._first(note.get("methods")) or note.get("paper_type") or "method"
        return (
            f"Which assumption behind the {method.replace('_', ' ')} in {title} most needs independent verification?"
        )

    def _has_value(self, note, key):
        value = (note.get("frontmatter") or {}).get(key)
        return bool(value and str(value).strip().lower() not in {"none", "unknown", "null", ""})

    def _first(self, values):
        return values[0] if values else ""

    def _ensure_list(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v).strip() for v in value if v is not None and str(v).strip()]
        return [str(value).strip()] if str(value).strip() else []

    def _table_cell(self, value):
        text = self._clean_text(value)
        return text.replace("|", "/").replace("\n", " ").strip()

    def _clean_text(self, text):
        text = str(text or "")
        replacements = {
            "\u00a0": " ",
            "\u2010": "-",
            "\u2011": "-",
            "\u2012": "-",
            "\u2013": "-",
            "\u2014": "-",
            "\u2212": "-",
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2026": "...",
            "鈥憀": "-l",
            "鈥慴": "-b",
            "鈥慸": "-d",
            "鈥慳": "-a",
            "鈥憇": "-s",
            "鈥檚": "'s",
            "鈥檛": "n't",
            "鈥檙": "'r",
            "鈥檝": "'v",
            "鈥檒": "'l",
            "鈥檇": "'d",
            "鈥檓": "'m",
            "鈥渟": '"s',
            "鈥渢": '"t',
            "鈥": "-",
            "锛焆": "?",
            "锛?": "?",
            "銆": ".",
            "鈮?": ">=",
            "鈫?": "->",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r">\s*\[!question\]\s*Open Question\s*>?", " ", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _extract_manual_notes(self, path):
        if not os.path.exists(path):
            return ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
        except Exception:
            return ""

        start = raw.find(MANUAL_START)
        end = raw.find(MANUAL_END, start + len(MANUAL_START)) if start >= 0 else -1
        if start >= 0 and end >= 0:
            return raw[start + len(MANUAL_START):end].strip("\n")

        match = re.search(r"(?ms)^##\s+9\.\s+Manual Notes\s*\n(.*)\Z", raw)
        return match.group(1).strip("\n") if match else ""

    def _manual_section(self, manual_notes):
        body = str(manual_notes or "").strip("\n")
        lines = [MANUAL_HEADING, "", MANUAL_START]
        if body:
            lines.append(body)
        lines.append(MANUAL_END)
        return "\n".join(lines)

    def _safe_filename(self, value):
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value).strip())
        safe = re.sub(r"_+", "_", safe).strip("_")
        return safe[:100] or "ResearchBrief"


def resolve_period(mode="week", week=None, month=None, from_date=None, to_date=None, last_days=None, date_value=None):
    anchor = _parse_date(date_value) or Date.today()

    if from_date or to_date:
        if not from_date or not to_date:
            raise ValueError("--from-date and --to-date must be used together")
        start = _parse_date(from_date)
        end = _parse_date(to_date)
        return start, end, f"{start.isoformat()}_to_{end.isoformat()}", "range"

    if last_days:
        if int(last_days) < 1:
            raise ValueError("--last-days must be at least 1")
        end = anchor
        start = end - timedelta(days=int(last_days) - 1)
        return start, end, f"{start.isoformat()}_to_{end.isoformat()}", "range"

    if week:
        match = re.match(r"^(\d{4})-?W(\d{1,2})$", week.strip(), re.IGNORECASE)
        if not match:
            raise ValueError("--week must look like 2026-W23")
        year, week_no = int(match.group(1)), int(match.group(2))
        start = Date.fromisocalendar(year, week_no, 1)
        end = start + timedelta(days=6)
        return start, end, f"{year}-W{week_no:02d}", "week"

    if month:
        start, end = _month_bounds(month)
        return start, end, start.strftime("%Y-%m"), "month"

    if mode == "month":
        start, end = _month_bounds(anchor.strftime("%Y-%m"))
        return start, end, start.strftime("%Y-%m"), "month"

    if mode == "range":
        start = anchor - timedelta(days=6)
        return start, anchor, f"{start.isoformat()}_to_{anchor.isoformat()}", "range"

    start = anchor - timedelta(days=anchor.weekday())
    end = start + timedelta(days=6)
    iso = start.isocalendar()
    return start, end, f"{iso.year}-W{iso.week:02d}", "week"


def _month_bounds(month):
    try:
        start = datetime.strptime(month, "%Y-%m").date()
    except Exception as exc:
        raise ValueError("--month must look like 2026-06") from exc

    if start.month == 12:
        next_month = Date(start.year + 1, 1, 1)
    else:
        next_month = Date(start.year, start.month + 1, 1)
    return start, next_month - timedelta(days=1)


def _parse_date(value):
    if value is None or value == "":
        return None
    if isinstance(value, Date):
        return value
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except Exception:
        return None


def _coerce_date(value):
    parsed = _parse_date(value)
    if parsed is None:
        raise ValueError(f"Invalid date: {value}")
    return parsed


def _to_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default
