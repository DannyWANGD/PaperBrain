import os
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ObsidianWriter:
    def __init__(self, config, provider='doubao'):
        self.config = config
        self.provider = provider
        self.vault_path = config['obsidian']['vault_path']
        self.daily_folder = os.path.join(self.vault_path, config['obsidian']['daily_digest_folder'])
        self.notes_folder = os.path.join(self.vault_path, config['obsidian']['detailed_notes_folder'])
        self.pdf_folder = os.path.join(self.vault_path, config['obsidian'].get('pdf_storage_folder', 'PDFs'))
        self.assets_folder = os.path.join(self.vault_path, "Assets")
        
        # Ensure directories exist
        os.makedirs(self.daily_folder, exist_ok=True)
        os.makedirs(self.notes_folder, exist_ok=True)
        os.makedirs(self.pdf_folder, exist_ok=True)
        os.makedirs(self.assets_folder, exist_ok=True)

    def sanitize_filename(self, filename):
        # Replace invalid characters and ensure it's not too long
        safe_name = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).strip()
        # Collapse multiple spaces
        safe_name = re.sub(r'\s+', ' ', safe_name)
        return safe_name[:100] # Limit length

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
        if not url:
            return ""
        m = re.search(r'arxiv\.org/(?:abs|pdf)/([0-9]+\.[0-9]+)', url)
        if m:
            return m.group(1)
        m = re.search(r'huggingface\.co/papers/([0-9]+\.[0-9]+)', url)
        if m:
            return m.group(1)
        return ""

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
        if target_date:
            today_str = target_date.strftime("%Y-%m-%d")
        else:
            today_str = datetime.now().strftime("%Y-%m-%d")
            
        filename = f"{today_str}-PaperDigest.md"
        filepath = os.path.join(self.daily_folder, filename)
        
        provider_cfg = self.config.get(self.provider, self.config.get('doubao', {}))
        threshold = provider_cfg.get('threshold_score', 7)
        high_impact = [p for p in papers if p.get('score', 0) >= threshold]

        # Filter papers for digest: skip score <= 6, show all >= 7
        # Within 7-score papers, only include if relevance >= 5 (basic quality gate)
        MIN_DIGEST_SCORE = 7
        digest_papers = [
            p for p in papers
            if p.get('score', 0) >= MIN_DIGEST_SCORE
            and p.get('relevance', 10) >= 5
        ]
        digest_papers.sort(key=lambda x: x.get('score', 0), reverse=True)

        if not digest_papers:
            logger.info("No papers met the minimum score threshold for daily digest. Writing summary-only digest.")

        content = ""
        for p in digest_papers:
            score = p.get('score', 0)
            icon = "🔥" if score >= 8 else "✨" if score >= 5 else "📄"
            
            # Use 'innovation' if available (new format), else fallback to 'summary' or 'abstract'
            innovation = p.get('innovation', p.get('summary', p.get('abstract', '')[:200] + "..."))
            limitations = p.get('limitations', "Not analyzed.")
            
            note_name = self.get_filename_from_paper(p)
            note_path = os.path.join(self.notes_folder, f"{note_name}.md")
            has_detailed_note = os.path.exists(note_path)
            if has_detailed_note:
                link = f"[[{note_name}]]"
            else:
                link = f"[Web Link]({p.get('url', '#')})"
            
            content += f"### {icon} {p['title']} (Score: {score}/10)\n"
            content += f"- **💡 Innovation**: {innovation}\n"
            content += f"- **⚠️ Limitations**: {limitations}\n"
            content += f"- **🔗 Link**: {link}\n"
            content += f"- **👥 Authors**: {', '.join(p.get('authors', []))}\n"
            
            # Add tags if available
            if p.get('tags'):
                # Format tags as #Tag1 #Tag2 (replacing spaces with underscores)
                # Requirement 1: Use "_" instead of "-" for tags
                tags_formatted = ' '.join([f"#{t.strip().replace(' ', '_').replace('-', '_')}" for t in p['tags']])
                content += f"- **🏷️ Tags**: {tags_formatted}\n"
            elif p.get('source'):
                content += f"- **🏷️ Source**: #{p['source']}\n"
            
            content += "\n---\n\n"

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
        score = paper.get('score', 0)
        tags_yaml = "\n".join([f"  - {t}" for t in safe_tags])

        # Build aliases: original title + AI-generated aliases
        all_aliases = [paper['title']]
        ai_aliases = paper.get('ai_aliases', [])
        for a in ai_aliases:
            if a and a not in all_aliases:
                all_aliases.append(a)
        aliases_yaml = "\n".join([f'  - "{a}"' for a in all_aliases])

        # arxiv_id for dedup
        arxiv_id_val = arxiv_id or ""

        meta = paper.get('metadata', {})
        pub_date = meta.get('publication_date', 'Unknown')
        institutions = meta.get('institutions', [])
        if isinstance(institutions, str):
            institutions = [institutions]
        github = meta.get('github', 'None')
        project_page = meta.get('project_page', 'None')
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
arxiv_id: "{arxiv_id_val}"
url: {paper.get('url')}
pdf_url: {paper.get('pdf_url')}
local_pdf: "{pdf_link}"
github: "{github}"
project_page: "{project_page}"{institutions_yaml}
publication_date: "{pub_date}"
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
