import os
import re
from datetime import datetime
import logging
import yaml
from src.paper_identity import canonical_arxiv_id, normalize_paper_identity, paper_id_from_arxiv_id
from src.paths import PaperBrainPaths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ObsidianWriter:
    def __init__(self, config, provider='doubao'):
        self.config = config
        self.provider = provider
        paths = PaperBrainPaths.from_config_dict(config)
        self.vault_path = str(paths.vault_path)
        self.daily_folder = str(paths.daily_digest_dir)
        self.notes_folder = str(paths.notes_dir)
        self.pdf_folder = str(paths.pdf_dir)
        self.assets_folder = str(paths.assets_dir)
        
        # Ensure directories exist
        os.makedirs(self.daily_folder, exist_ok=True)
        os.makedirs(self.notes_folder, exist_ok=True)
        os.makedirs(self.pdf_folder, exist_ok=True)
        os.makedirs(self.assets_folder, exist_ok=True)

    def sanitize_filename(self, filename):
        # Replace invalid characters and ensure it's not too long
        filename = str(filename or "").replace("_", " ")
        safe_name = "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ']).strip()
        # Collapse multiple spaces
        safe_name = re.sub(r'\s+', ' ', safe_name)
        return safe_name[:100] # Limit length

    def _format_score(self, value):
        try:
            return f"{float(value):.1f}"
        except Exception:
            return "0.0"

    def _numeric_score(self, value, default=0.0):
        try:
            return float(value)
        except Exception:
            return default

    def _sanitize_obsidian_text(self, text):
        if not text:
            return ""
        t = str(text).replace("\r\n", "\n").replace("\r", "\n")
        t = t.replace("\\n", "\n")
        t = t.replace("\u200b", "").replace("\ufeff", "")
        return t

    def get_filename_from_paper(self, paper):
        """Generates filename based on short_title or title."""
        if paper.get('short_title'):
            return self.sanitize_filename(paper['short_title'])
        return self.sanitize_filename(paper['title'])

    def get_pdf_path(self, title):
        """Returns the destination path for a PDF in the Obsidian vault."""
        # Note: This method was using title directly, but ideally should use short_title if available.
        # However, at download time we might not have short_title if it's not analyzed yet?
        # Actually we do have it after screening.
        filename = f"{self.sanitize_filename(title)}.pdf"
        return os.path.join(self.pdf_folder, filename)

    def get_pdf_path_from_paper(self, paper):
        """Returns the destination path for a PDF in the Obsidian vault using paper object."""
        base_name = self.get_filename_from_paper(paper)
        return os.path.join(self.pdf_folder, f"{base_name}.pdf")

    def _extract_arxiv_id(self, url):
        """Extracts normalized arXiv ID from a URL (arxiv.org or huggingface.co/papers)."""
        return canonical_arxiv_id(url)

    def _find_note_by_arxiv_id(self, arxiv_id, exclude=""):
        """Returns filename of an existing note with the same arXiv ID, or empty string."""
        if not os.path.exists(self.notes_folder):
            return ""
        for fn in os.listdir(self.notes_folder):
            if not fn.endswith(".md") or fn == exclude:
                continue
            try:
                with open(os.path.join(self.notes_folder, fn), "r", encoding="utf-8") as f:
                    content = f.read(2000)  # only need frontmatter
                if arxiv_id in content:
                    return fn
            except Exception:
                continue
        return ""

    def _find_note_path_for_paper(self, paper):
        """Returns the path of an existing detailed note for this paper, if any."""
        note_name = self.get_filename_from_paper(paper) if paper.get("title") else ""
        if note_name:
            note_path = os.path.join(self.notes_folder, f"{note_name}.md")
            if os.path.exists(note_path):
                return note_path

        for key in ("url", "pdf_url", "arxiv_id", "paper_id"):
            arxiv_id = self._extract_arxiv_id(paper.get(key, ""))
            if arxiv_id:
                existing = self._find_note_by_arxiv_id(arxiv_id)
                if existing:
                    return os.path.join(self.notes_folder, existing)
        return ""

    def _read_note_frontmatter(self, note_path):
        try:
            with open(note_path, "r", encoding="utf-8") as f:
                raw = f.read(6000)
            match = re.match(r"^---\n([\s\S]*?)\n---\n?", raw)
            if not match:
                return {}
            frontmatter = yaml.safe_load(match.group(1)) or {}
            return frontmatter if isinstance(frontmatter, dict) else {}
        except Exception:
            return {}

    def _ensure_clean_list(self, value):
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            items = value
        else:
            items = [value]
        return [str(item).strip() for item in items if item is not None and str(item).strip()]

    def _paper_institutions(self, paper):
        metadata = paper.get("metadata") if isinstance(paper.get("metadata"), dict) else {}
        for value in (paper.get("institutions"), metadata.get("institutions")):
            institutions = self._ensure_clean_list(value)
            if institutions:
                return institutions

        note_path = paper.get("note_path")
        if not note_path or not os.path.exists(note_path):
            note_path = self._find_note_path_for_paper(paper)
        if note_path:
            institutions = self._ensure_clean_list(self._read_note_frontmatter(note_path).get("institutions"))
            if institutions:
                return institutions
        return []

    def _note_link_for_paper(self, paper):
        """Returns an Obsidian note link when possible, otherwise the source URL."""
        note_path = self._find_note_path_for_paper(paper)
        if note_path:
            return f"[[{os.path.basename(note_path)[:-3]}]]"

        return f"[Web Link]({paper.get('url', '#')})"

    def _digest_identity_tokens(self, paper):
        paper = normalize_paper_identity(paper)
        tokens = set()
        for key in ("paper_id", "arxiv_id", "url", "pdf_url", "title", "short_title"):
            value = str(paper.get(key) or "").strip()
            if value:
                tokens.add(value.lower())
        arxiv_id = canonical_arxiv_id(paper.get("paper_id") or paper.get("arxiv_id") or paper.get("url") or paper.get("pdf_url"))
        if arxiv_id:
            tokens.add(arxiv_id.lower())
            tokens.add(f"arxiv:{arxiv_id}".lower())
        return tokens

    def _digest_entry_exists(self, digest_text, paper):
        digest_low = digest_text.lower()
        return any(token and token in digest_low for token in self._digest_identity_tokens(paper))

    def _digest_entry_score(self, entry_text):
        m = re.search(r"\(Score:\s*([0-9]+(?:\.[0-9]+)?)/10\)", entry_text)
        return self._numeric_score(m.group(1), 0.0) if m else 0.0

    def _render_daily_digest_entry(self, paper):
        paper = normalize_paper_identity(paper)
        score = self._numeric_score(paper.get('score', 0), 0.0)
        score_text = self._format_score(score)
        icon = "🔥" if score >= 8 else "✨" if score >= 5 else "📄"
        innovation = paper.get('innovation', paper.get('summary', paper.get('abstract', '')[:200] + "..."))
        limitations = paper.get('limitations', "Not analyzed.")
        link = self._note_link_for_paper(paper)
        authors = ', '.join(paper.get('authors', []) or [])
        institutions = self._paper_institutions(paper)
        institutions_text = ', '.join(institutions) if institutions else "Unknown"

        content = f"### {icon} {paper['title']} (Score: {score_text}/10)\n"
        content += f"- **💡 Innovation**: {innovation}\n"
        content += f"- **⚠️ Limitations**: {limitations}\n"
        content += f"- **🔗 Link**: {link}\n"
        content += f"- **👥 Authors**: {authors}\n"
        content += f"- **Institutions**: {institutions_text}\n"

        if paper.get('tags'):
            tags_formatted = ' '.join([f"#{t.strip().replace(' ', '_').replace('-', '_')}" for t in paper['tags']])
            content += f"- **🏷️ Tags**: {tags_formatted}\n"
        elif paper.get('source'):
            content += f"- **🏷️ Source**: #{paper['source']}\n"

        content += "\n---\n"
        return content

    def _split_digest_entries(self, content):
        entries = re.findall(r"^###\s+[\s\S]*?(?=^###\s+|\Z)", content.strip(), flags=re.MULTILINE)
        return [entry.strip() + "\n" for entry in entries if entry.strip()]

    def _update_digest_summary_counts(self, text, total_count, high_count):
        replacement = f"Total Papers: {total_count} | High Impact: {high_count}"
        if re.search(r"Total Papers:\s*\d+\s*\|\s*High Impact:\s*\d+", text):
            return re.sub(r"Total Papers:\s*\d+\s*\|\s*High Impact:\s*\d+", replacement, text, count=1)
        return text

    def upsert_single_paper_digest_entry(self, paper, target_date=None):
        """Insert a single-paper result into that day's digest if it is not already present."""
        paper = normalize_paper_identity(paper)
        if target_date is None:
            target_date = self._paper_publication_date(paper)
        if target_date is None:
            logger.info("Single-paper digest update skipped: publication date is unknown.")
            return None

        min_score = self._numeric_score(self.config.get('analysis', {}).get('daily_digest_min_score'), 7.0)
        score = self._numeric_score(paper.get('score', 0), 0.0)
        if score < min_score:
            logger.info(f"Single-paper digest update skipped: score {score:.1f} < {min_score:.1f}.")
            return None

        today_str = target_date.strftime("%Y-%m-%d")
        filepath = os.path.join(self.daily_folder, f"{today_str}-PaperDigest.md")
        if not os.path.exists(filepath):
            logger.info(f"Daily digest does not exist for {today_str}; creating it with the single paper.")
            return self.write_daily_digest([paper], target_date=target_date)

        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        if self._digest_entry_exists(raw, paper):
            logger.info(f"Daily digest already contains this paper: {paper.get('paper_id') or paper.get('title')}")
            return filepath

        papers_header = re.search(r"^##\s+.*?Papers List.*?$", raw, flags=re.MULTILINE)
        if not papers_header:
            logger.warning(f"Could not find Papers List section in {filepath}; leaving digest unchanged.")
            return filepath

        head = raw[:papers_header.end()].rstrip() + "\n"
        body = raw[papers_header.end():].strip()
        entries = self._split_digest_entries(body)
        new_entry = self._render_daily_digest_entry(paper)
        entries.append(new_entry)
        entries.sort(key=self._digest_entry_score, reverse=True)

        content = head + "\n" + "\n".join(entries).strip() + "\n"
        total_count = len(entries)
        high_count = len([entry for entry in entries if self._digest_entry_score(entry) >= self._numeric_score(
            self.config.get(self.provider, self.config.get('doubao', {})).get('threshold_score', 7), 7.0
        )])
        content = self._update_digest_summary_counts(content, total_count, high_count)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Inserted single paper into daily digest: {filepath}")
        return filepath

    def _paper_publication_date(self, paper):
        value = paper.get("published") or paper.get("publication_date")
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

    def scan_existing_notes(self):
        """Scans the vault for existing markdown files to use for context."""
        notes = []
        for root, dirs, files in os.walk(self.vault_path):
            for file in files:
                if file.endswith(".md"):
                    notes.append(file.replace(".md", ""))
        return notes

    def write_daily_digest(self, papers, target_date=None):
        """Writes the daily digest file with structured analysis."""
        papers = [normalize_paper_identity(p) for p in papers]
        if target_date:
            today_str = target_date.strftime("%Y-%m-%d")
        else:
            today_str = datetime.now().strftime("%Y-%m-%d")
            
        filename = f"{today_str}-PaperDigest.md"
        filepath = os.path.join(self.daily_folder, filename)
        
        provider_cfg = self.config.get(self.provider, self.config.get('doubao', {}))
        threshold = provider_cfg.get('threshold_score', 7)
        high_impact = [p for p in papers if self._numeric_score(p.get('score', 0)) >= threshold]

        # Daily digest is the broad daily map: include every paper with score >= 7.0.
        # Deep-analysis selection remains stricter and is handled separately in main.py.
        MIN_DIGEST_SCORE = self._numeric_score(
            self.config.get('analysis', {}).get('daily_digest_min_score'),
            7.0
        )
        digest_papers = [
            p for p in papers
            if self._numeric_score(p.get('score', 0)) >= MIN_DIGEST_SCORE
        ]
        digest_papers.sort(key=lambda x: self._numeric_score(x.get('score', 0)), reverse=True)

        if not digest_papers:
            logger.info("No papers met the minimum score threshold for daily digest. Writing summary-only digest.")

        content = "\n".join([self._render_daily_digest_entry(p).strip() for p in digest_papers])
        if content:
            content += "\n"

        if not content:
            content = "_今日无符合质量标准的论文（分数 ≥ 7）。_\n"

        template = self.config['obsidian']['daily_digest_template']
        final_content = template.replace("{{date}}", today_str) \
                                .replace("{{total_count}}", str(len(digest_papers))) \
                                .replace("{{high_impact_count}}", str(len(high_impact))) \
                                .replace("{{content}}", content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        
        logger.info(f"Daily digest written to {filepath}")
        return filepath

    def write_detailed_note(self, paper, analysis_content, local_pdf_path=None, image_caption=""):
        """Writes a detailed note for a high-value paper."""
        paper = normalize_paper_identity(paper)
        safe_title = self.get_filename_from_paper(paper)
        filename = f"{safe_title}.md"
        filepath = os.path.join(self.notes_folder, filename)

        # Dedup check: scan existing notes for same arXiv ID
        paper_url = paper.get('url', '')
        arxiv_id = self._extract_arxiv_id(paper_url)
        if arxiv_id:
            existing = self._find_note_by_arxiv_id(arxiv_id, exclude=filename)
            if existing:
                logger.warning(
                    f"[DEDUP] Skipping write for '{filename}': "
                    f"arXiv ID {arxiv_id} already exists as '{existing}'. "
                    f"Delete the old file first if you want to overwrite."
                )
                return os.path.join(self.notes_folder, existing)
        
        pdf_link = ""
        if local_pdf_path:
            pdf_filename = os.path.basename(local_pdf_path)
            pdf_link = f"[[{pdf_filename}]]"

        # Look for architecture image in Assets
        arch_image_link = ""
        # The analyser saves images as {pdf_filename_no_ext}_arch.png/jpg
        if local_pdf_path:
            base_name = os.path.splitext(os.path.basename(local_pdf_path))[0]
            # Try common extensions
            for ext in ['png', 'jpg', 'jpeg']:
                img_name = f"{base_name}_arch.{ext}"
                if os.path.exists(os.path.join(self.assets_folder, img_name)):
                    arch_image_link = f"![[{img_name}]]"
                    # Only append caption if provided and not empty (Requirement 4: Remove caption)
                    if image_caption:
                        arch_image_link += f"\n*{image_caption}*"
                    break

        # Add metadata frontmatter
        tags = paper.get('tags', [])
        if not tags:
            tags = ['paper', 'robotics', 'AI']
        else:
            tags = ['paper'] + tags
        safe_tags = [t.strip().replace(' ', '_').replace('-', '_') for t in tags]
        score = self._format_score(paper.get('score', 0))
        tags_yaml = "\n".join([f"  - {t}" for t in safe_tags])

        # Build aliases: original title + AI-generated aliases
        all_aliases = [paper['title']]
        ai_aliases = paper.get('ai_aliases', [])
        for a in ai_aliases:
            if a and a not in all_aliases:
                all_aliases.append(a)
        aliases_yaml = "\n".join([f'  - "{a}"' for a in all_aliases])

        # arxiv_id for dedup
        arxiv_id_val = canonical_arxiv_id(arxiv_id or paper.get("arxiv_id") or paper.get("pdf_url") or paper.get("url"))
        paper_id_val = paper.get("paper_id") or paper_id_from_arxiv_id(arxiv_id_val)

        meta = paper.get('metadata', {}) if isinstance(paper.get('metadata'), dict) else {}
        pub_date_obj = self._paper_publication_date(paper)
        pub_date = pub_date_obj.strftime("%Y-%m-%d") if hasattr(pub_date_obj, "strftime") else (paper.get('publication_date') or 'Unknown')
        metadata_pub_date = meta.get('publication_date') or 'Unknown'
        institutions = self._ensure_clean_list(meta.get('institutions') or paper.get('institutions'))
        github = meta.get('github') or paper.get('github') or 'None'
        project_page = meta.get('project_page') or paper.get('project_page') or 'None'
        paper['publication_date'] = pub_date
        paper['metadata_publication_date'] = metadata_pub_date
        paper['institutions'] = institutions
        paper['github'] = github
        paper['project_page'] = project_page
        institutions_yaml = ""
        if institutions:
            institutions_yaml = "\ninstitutions:" + "".join([f"\n  - \"{i}\"" for i in institutions])

        abstract_block = paper.get('abstract', '')
        analysis_clean = analysis_content or ""
        try:
            m = re.search(r"##\s*📌\s*Abstract\s*\n([\s\S]*?)(?:\n##\s+|\Z)", analysis_clean)
            if m:
                abstract_block = m.group(1).strip()
                analysis_clean = analysis_clean.replace(m.group(0), "").strip()
        except Exception:
            pass

        # Strip any stray wrapper headers the model or analyser may have injected
        analysis_clean = re.sub(r'^#\s+🚀\s+Deep Analysis Report:[^\n]*\n+', '', analysis_clean, flags=re.MULTILINE)
        analysis_clean = re.sub(r'^##\s+📊\s+Academic Quality & Innovation\s*\n+', '', analysis_clean, flags=re.MULTILINE)
        analysis_clean = re.sub(r'^#\s+Deep (Analysis|Engineering Analysis):[^\n]*\n+', '', analysis_clean, flags=re.MULTILINE)
        # Strip residual metadata JSON blocks
        analysis_clean = re.sub(r'^[^\n]*"publication_date"[^\n]*\n(?:.*\n)*?.*\}\s*\n(?:```[^\n]*\n)?', '', analysis_clean, flags=re.MULTILINE)
        # Fix numbered section headers missing ## prefix: "1. 核心摘要" → "## 1. 核心摘要"
        analysis_clean = re.sub(r'^(\d+\.\s+(?:核心摘要|技术分解|证据与指标|批判性评估|研究者灵感提示))', r'## \1', analysis_clean, flags=re.MULTILINE)
        # Collapse 3+ consecutive blank lines to 2
        analysis_clean = re.sub(r'\n{3,}', '\n\n', analysis_clean).strip()

        abstract_block = self._sanitize_obsidian_text(abstract_block)
        analysis_clean = self._sanitize_obsidian_text(analysis_clean)

        content = f"""---
tags:
{tags_yaml}
aliases:
{aliases_yaml}
paper_id: "{paper_id_val}"
arxiv_id: "{arxiv_id_val}"
url: {paper.get('url')}
pdf_url: {paper.get('pdf_url')}
local_pdf: "{pdf_link}"
github: "{github}"
project_page: "{project_page}"{institutions_yaml}
publication_date: "{pub_date}"
metadata_publication_date: "{metadata_pub_date}"
score: {score}
---

# {paper['title']}

## 📌 Abstract
{abstract_block}

## 🖼️ Architecture
{arch_image_link}

## 🧠 AI Analysis
{analysis_clean}

## 📂 Resources
- **Local PDF**: {pdf_link}
- [Online PDF]({paper.get('pdf_url')})
- [ArXiv Link]({paper.get('url')})
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Detailed note written to {filepath}")
        return filepath
