import os
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportWriter:
    def __init__(self, config):
        self.config = config
        self.output_dir = config['output']['base_dir']
        self.naming_format = config['output']['naming_format']
        
        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def sanitize_filename(self, filename):
        # Remove invalid characters
        safe_name = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).strip()
        return safe_name[:100].replace(' ', '_')

    def save_report(self, paper, report_content, report_type="DeepAnalysis"):
        """Saves the generated report to the standardized output directory."""
        
        timestamp = datetime.now().strftime("%Y%m%d")
        safe_title = self.sanitize_filename(paper['title'])
        
        # Generate filename based on config format
        # format: "{title}_{type}_{timestamp}.md"
        filename = self.naming_format.format(
            title=safe_title,
            type=report_type,
            timestamp=timestamp
        )
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Add metadata frontmatter
        tags = paper.get('tags', [])
        tags_yaml = "\n".join([f"  - {t}" for t in tags]) if tags else ""
        
        final_content = f"""---
title: "{paper['title']}"
date: {datetime.now().strftime("%Y-%m-%d")}
type: {report_type}
paper_url: {paper.get('url')}
pdf_url: {paper.get('pdf_url')}
tags:
{tags_yaml}
---

{report_content}
"""
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(final_content)
            logger.info(f"Report saved to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving report {filename}: {e}")
            return None
