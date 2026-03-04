import os
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ObsidianWriter:
    def __init__(self, config):
        self.config = config
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
        
        high_impact = [p for p in papers if p.get('score', 0) >= self.config['doubao']['threshold_score']]
        
        content = ""
        for p in papers:
            score = p.get('score', 0)
            icon = "🔥" if score >= 8 else "✨" if score >= 5 else "📄"
            
            # Use 'innovation' if available (new format), else fallback to 'summary' or 'abstract'
            innovation = p.get('innovation', p.get('summary', p.get('abstract', '')[:200] + "..."))
            limitations = p.get('limitations', "Not analyzed.")
            
            link = f"[[{self.get_filename_from_paper(p)}]]" if score >= self.config['doubao']['threshold_score'] else f"[Link]({p.get('url', '#')})"
            # Requirement 2: Only provide local link for high scoring papers, otherwise just web link
            if score < self.config['doubao']['threshold_score']:
                # Ensure it's just the web link
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

        template = self.config['obsidian']['daily_digest_template']
        final_content = template.replace("{{date}}", today_str) \
                                .replace("{{total_count}}", str(len(papers))) \
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
        # Ensure default tags
        if not tags:
            tags = ['paper', 'robotics', 'AI']
        else:
            tags = ['paper'] + tags
        
        # Sanitize tags: Replace spaces/hyphens with underscores to avoid YAML errors and match requirement
        safe_tags = [t.strip().replace(' ', '_').replace('-', '_') for t in tags]
        
        # Add score tag (REMOVED: Now a property)
        score = paper.get('score', 0)
        # safe_tags.append(f"Score_{score}")

        tags_yaml = "\n".join([f"  - {t}" for t in safe_tags])
        
        # Extract metadata from deep analysis
        meta = paper.get('metadata', {})
        # Default to "Unknown" if not found, but we want YYYY-MM-DD format if possible
        pub_date = meta.get('publication_date', 'Unknown')
        institutions = meta.get('institutions', [])
        if isinstance(institutions, str):
            institutions = [institutions]
        
        github = meta.get('github', 'None')
        project_page = meta.get('project_page', 'None')
        
        institutions_yaml = ""
        if institutions:
            institutions_yaml = "\ninstitutions:" + "".join([f"\n  - \"{i}\"" for i in institutions])

        content = f"""---
tags:
{tags_yaml}
aliases:
  - "{paper['title']}"
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
{paper['abstract']}

## 🖼️ Architecture
{arch_image_link}

## 🧠 AI Analysis
{analysis_content}

## 📂 Resources
- **Local PDF**: {pdf_link}
- [Online PDF]({paper.get('pdf_url')})
- [ArXiv Link]({paper.get('url')})
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Detailed note written to {filepath}")
        return filepath
