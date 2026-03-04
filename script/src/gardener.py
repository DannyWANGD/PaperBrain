import os
import re
import logging
import yaml
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeGardener:
    def __init__(self, config):
        self.config = config
        self.vault_path = config['obsidian']['vault_path']
        self.notes_folder = os.path.join(self.vault_path, config['obsidian']['detailed_notes_folder'])
        
    def _get_existing_notes_metadata(self):
        """
        Scans all existing notes and returns a dictionary:
        {
            "Note_Filename": {
                "path": "full/path/to/note.md",
                "aliases": ["Alias 1", "Alias 2"],
                "title": "Full Title"
            }
        }
        """
        notes_meta = {}
        if not os.path.exists(self.notes_folder):
            return notes_meta

        for filename in os.listdir(self.notes_folder):
            if not filename.endswith(".md"):
                continue
                
            filepath = os.path.join(self.notes_folder, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract Frontmatter
                frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
                aliases = []
                title = filename.replace(".md", "").replace("_", " ") # Default title from filename
                
                if frontmatter_match:
                    try:
                        fm = yaml.safe_load(frontmatter_match.group(1))
                        if fm:
                            aliases = fm.get('aliases', [])
                            # Ensure aliases is a list
                            if isinstance(aliases, str):
                                aliases = [aliases]
                    except yaml.YAMLError:
                        pass
                
                # Add filename stem as an alias too
                stem = filename.replace(".md", "")
                if stem not in aliases:
                    aliases.append(stem)
                
                notes_meta[filename] = {
                    "path": filepath,
                    "aliases": [a.lower() for a in aliases if a], # Normalize for matching
                    "title": title
                }
            except Exception as e:
                logger.error(f"Error reading note {filename}: {e}")
                
        return notes_meta

    def prune_and_graft(self, new_papers):
        """
        Main entry point.
        new_papers: List of paper dictionaries that were just analyzed (must have 'title', 'abstract', 'innovation').
        """
        logger.info("🌱 Knowledge Gardener started pruning and grafting...")
        
        existing_notes = self._get_existing_notes_metadata()
        if not existing_notes:
            logger.info("No existing notes to link back to.")
            return

        updates_count = 0
        
        for new_paper in new_papers:
            # We only care about high-quality papers that generated a detailed note
            # Assuming main.py passes only analyzed papers or we check score
            if new_paper.get('score', 0) < self.config['doubao']['threshold_score']:
                continue
                
            # Prepare new paper data for matching
            new_title = new_paper.get('title', '')
            new_abstract = new_paper.get('abstract', '')
            new_innovation = new_paper.get('innovation', '')
            new_note_filename = new_paper.get('short_title', '') or new_title
            # Sanitize filename to match what ObsidianWriter likely produced
            # (Re-implementing basic sanitation or we rely on main.py passing the actual filename if possible. 
            #  For now, let's assume standard sanitation)
            safe_new_filename = "".join([c for c in new_note_filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).strip()
            safe_new_filename = re.sub(r'\s+', ' ', safe_new_filename)[:100]
            
            # Text to search IN (the new paper's content)
            search_text = (new_title + " " + new_abstract + " " + new_innovation).lower()
            
            for note_file, note_data in existing_notes.items():
                # Don't link to self
                if note_file == f"{safe_new_filename}.md":
                    continue
                
                # Check for Concept Match: Does the NEW paper mention the OLD note's aliases?
                matched_alias = None
                for alias in note_data['aliases']:
                    # Simple substring match (could be improved with regex for word boundaries)
                    # Use spaces around alias to avoid partial word matches (e.g. "rain" in "brain")
                    # But aliases can be multi-word.
                    if f" {alias} " in f" {search_text} ":
                        matched_alias = alias
                        break
                
                if matched_alias:
                    # FOUND A CONNECTION!
                    # Grafting: Add backlink to the OLD note
                    self._append_backlink(
                        note_data['path'], 
                        new_paper, 
                        safe_new_filename, 
                        matched_alias
                    )
                    updates_count += 1

        logger.info(f"🌿 Gardening complete. Updated {updates_count} existing notes with backlinks.")

    def _append_backlink(self, target_note_path, source_paper, source_filename, matched_concept):
        """Appends a backlink entry to the target note."""
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            backlink_text = f"\n- [ ] **{today_str}**: New paper [[{source_filename}]] discusses *{matched_concept}*. Innovation: \"{source_paper.get('innovation', 'No summary')}\""
            
            with open(target_note_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            header = "## 🔗 Related Work Updates"
            
            if header in content:
                # Append to existing section
                # We simply append to the end of the file if section exists, or find the section?
                # Simplest robust way: Append to end of file, assuming the header is near the end or we just add it.
                # Actually, let's look for the header.
                pattern = re.escape(header)
                if re.search(pattern, content):
                    # Insert after the header
                    # Find the header and the next newline
                    # This is tricky with regex replacement.
                    # Let's just append to the file end for safety, Obsidian handles it well.
                    # Or better: check if we already linked this paper to avoid duplicates
                    if f"[[{source_filename}]]" in content:
                        return # Already linked
                        
                    # Append to end of file
                    with open(target_note_path, 'a', encoding='utf-8') as f:
                        f.write(backlink_text)
            else:
                # Create section at the end
                if f"[[{source_filename}]]" in content:
                    return
                    
                with open(target_note_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n{header}{backlink_text}")
                    
            logger.info(f"  -> Linked '{source_paper['title'][:30]}...' to '{os.path.basename(target_note_path)}'")
            
        except Exception as e:
            logger.error(f"Failed to update backlink in {target_note_path}: {e}")
