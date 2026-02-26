import os
import time
import logging
import json
import fitz  # PyMuPDF
import re
from openai import OpenAI
from pypdf import PdfReader
from PIL import Image
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import base64

class PaperAnalyser:
    def __init__(self, config):
        self.config = config
        self.api_key = config['doubao']['api_key']
        # Doubao uses the Ark endpoint which is OpenAI compatible
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        # Use Lite for screening (was Flash)
        self.model_flash = config['doubao'].get('model_flash', 'doubao-seed-2-0-lite-260215')
        # Use Pro for deep analysis
        self.model_pro = config['doubao'].get('model_pro', 'doubao-seed-2-0-pro-260215')

    def pdf_to_base64_images(self, pdf_path, max_pages=10):
        """Converts PDF pages to base64 encoded images for Vision API."""
        try:
            doc = fitz.open(pdf_path)
            images = []
            # Limit pages to avoid excessive token usage, but cover main content
            # Usually first 8-10 pages contain the core paper (excluding references)
            for i in range(min(len(doc), max_pages)):
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # 2x zoom for better quality
                
                # Convert to bytes
                img_bytes = pix.tobytes("png")
                
                # Encode to base64
                base64_str = base64.b64encode(img_bytes).decode('utf-8')
                images.append(base64_str)
            
            doc.close()
            return images
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            return []

    def _sanitize_json(self, text):
        """Cleanups LLM response to ensure valid JSON."""
        # Remove markdown code blocks
        text = text.replace('```json', '').replace('```', '').strip()
        
        # Escape newlines inside strings (common LLM issue)
        # This regex looks for newlines that are NOT between objects/arrays
        # But a simpler way is to use strict mode=False in json.loads
        # Or let's just try to parse, if fail, try to fix common issues
        return text

    def screen_paper(self, paper):
        """
        Uses Doubao Lite (equivalent to Flash) to screen the paper based on abstract.
        Returns a dict with 'score' (1-10), 'reason', 'innovation', 'limitations', and 'tags'.
        """
        prompt = f"""
        You are an expert researcher in Robotics and AI.
        Please evaluate the following paper based on these keywords: {', '.join(self.config['search']['keywords'])}.
        
        Title: {paper['title']}
        Abstract: {paper['abstract']}
        
        Task:
        1. Rate the "Research Value" for my interests on a scale of 1-10.
           - 8-10: Must read immediately. SOTA results or major theoretical breakthrough.
           - 6-7: Worth reading. Interesting idea or good results.
           - 4-5: Maybe later. Standard incremental work.
           - 1-3: Skip. Irrelevant or low quality.
        2. Analyze the **Innovation**: What is the key novelty? (1 sentence)
        3. Analyze the **Limitations/Weaknesses**: What is missing or could be improved? (1 sentence)
        4. Identify **Tags**: Extract 3-5 specific technical tags (e.g., 'Diffusion Transformer', 'RLHF', 'Sim2Real', 'VLA', '3D Gaussian Splatting'). Do not use generic tags like 'AI' or 'Robotics'.
        5. Return JSON format only: 
        {{
            "score": int, 
            "innovation": "string", 
            "limitations": "string", 
            "reason": "string",
            "tags": ["string", "string"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_flash,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant. Be objective and critical. Use consistent scoring standards."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1 # Lower temperature for more stable/deterministic scoring
            )
            
            content = response.choices[0].message.content
            cleaned_content = self._sanitize_json(content)
            
            # Use strict=False to allow control characters like newlines in strings
            return json.loads(cleaned_content, strict=False)
            
        except Exception as e:
            logger.error(f"Error screening paper {paper['title']}: {e}")
            # Fallback parsing if JSON mode fails or returns text
            return {
                "score": 0, 
                "innovation": "Analysis failed", 
                "limitations": "Analysis failed", 
                "reason": str(e),
                "tags": []
            }

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            # Limit to first 20 pages to avoid token limits if paper is huge
            for page in reader.pages[:20]:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return ""

    def _is_valid_image(self, image_bytes):
        """Checks if the image is valid (not icon, not solid color, etc.)."""
        try:
            img = Image.open(io.BytesIO(image_bytes))
            # 1. Size Check: Ignore small icons or very thin lines
            if img.width < 150 or img.height < 150:
                return False
            
            # 2. Aspect Ratio Check: Ignore extreme ratios (likely separators or lines)
            aspect = img.width / img.height
            if aspect > 5 or aspect < 0.2:
                return False
            
            # 3. Entropy Check (Robust against solid colors/simple gradients)
            # A solid color has entropy 0. A simple gradient has low entropy.
            # Complex diagrams usually have entropy > 4.5
            entropy = img.entropy()
            if entropy < 3.5:
                return False
            
            # 4. Unique Colors Check
            # Vector graphics/backgrounds often have very few unique colors (< 30)
            # Complex diagrams with anti-aliasing usually have > 100
            if img.mode != 'RGB' and img.mode != 'RGBA':
                img = img.convert('RGB')
                
            # Efficiently estimate unique colors by resizing (to avoid OOM on huge images)
            # Small resize preserves color diversity of backgrounds but merges noise
            img_small = img.resize((100, 100))
            colors = img_small.getcolors(maxcolors=1000)
            # If colors is None, it means > 1000 unique colors (Good)
            # If colors is a list, check length
            if colors and len(colors) < 30:
                return False
                
            return True
        except Exception:
            return False

    def extract_images_from_pdf(self, pdf_path, output_folder):
        """
        Extracts images from the first 5 pages, uses Vision API to identify the best Architecture/Overview figure,
        and saves it. Considers BOTH extracted images and rendered pages to ensure vector diagrams are caught.
        Returns the path to the saved image AND a caption/description.
        """
        try:
            doc = fitz.open(pdf_path)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # --- Phase 0: Text-based Pre-Filtering ---
            # Scan text to find pages with "Figure X: ... Architecture/Overview ..."
            target_page_indices = set()
            keyword_pattern = re.compile(r'(Figure|Fig\.)\s*\d+.*?(Architecture|Overview|Framework|Pipeline|System)', re.IGNORECASE)
            
            for i in range(min(10, len(doc))):
                page_text = doc[i].get_text()
                if keyword_pattern.search(page_text):
                    target_page_indices.add(i)
            
            # If no keywords found, fallback to first 5 pages
            if not target_page_indices:
                target_page_indices = set(range(min(5, len(doc))))
            else:
                # Add adjacent pages just in case the figure is on one page and caption on another
                # But prioritize the found pages
                pass

            # --- Collection Phase ---
            candidates = []

            # 1. Extracted Images from Target Pages
            extracted_candidates = []
            for page_num in sorted(list(target_page_indices)):
                page = doc.load_page(page_num)
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    try:
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        if self._is_valid_image(image_bytes):
                            extracted_candidates.append({
                                "bytes": image_bytes,
                                "ext": base_image["ext"],
                                "source": f"Extracted Image (Page {page_num+1})",
                                "type": "extracted"
                            })
                    except Exception:
                        continue
            
            extracted_candidates.sort(key=lambda x: len(x["bytes"]), reverse=True)
            candidates.extend(extracted_candidates[:5]) # Top 5 largest extracted

            # 2. Rendered Pages (Target Pages only)
            for page_num in sorted(list(target_page_indices)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                candidates.append({
                    "bytes": img_bytes,
                    "ext": "png",
                    "source": f"Full Page {page_num+1} Render",
                    "type": "rendered_page"
                })

            if not candidates:
                logger.warning("No images or pages could be rendered.")
                return None, ""

            # --- Selection Phase ---
            vision_messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """
I have extracted these images from a research paper. Some are specific extracted figures, others are full page renders.
Please identify the **Main Architecture Diagram** (System Pipeline/Framework).

**Selection Rules:**
1. **Target**: Look for block diagrams, flowcharts, or schematics with boxes, arrows, and technical text labels.
2. **Context**: Look for captions like "Figure 1: Overview", "Figure 2: Architecture", "Framework".
3. **Negative Filter (CRITICAL)**: 
   - IGNORE "Teaser Images" (often Figure 1, showing a cool result/screenshot/3D render).
   - IGNORE Gameplay screenshots, Photos, or 3D Scenes.
   - IGNORE Bar charts/Plots.
4. **Tie-breaker**: If unsure between a "cool image" and a "boring chart", CHOOSE THE CHART. If a Full Page contains the diagram clearly, select the Full Page.

**Output Format**:
Return a JSON object with:
- "index": The index of the best image (integer).
- "caption": A verbatim extraction of the figure caption from the image if readable (e.g. "Figure 2: The overall architecture..."). If not readable, write a descriptive caption.

JSON ONLY.
"""}
                    ]
                }
            ]

            for idx, item in enumerate(candidates):
                b64_img = base64.b64encode(item["bytes"]).decode('utf-8')
                vision_messages[0]["content"].append({
                    "type": "text", 
                    "text": f"Index {idx} [{item['source']}]:"
                })
                vision_messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{item['ext']};base64,{b64_img}"}
                })

            try:
                response = self.client.chat.completions.create(
                    model=self.model_pro,
                    messages=vision_messages,
                    max_tokens=200
                )
                choice_text = response.choices[0].message.content.strip()
                cleaned_json = self._sanitize_json(choice_text)
                data = json.loads(cleaned_json, strict=False)
                
                best_idx = data.get("index", -1)
                caption = data.get("caption", "Architecture Diagram")

                if best_idx >= 0 and best_idx < len(candidates):
                    chosen = candidates[best_idx]
                    logger.info(f"Vision Model selected Index {best_idx} ({chosen['source']}) as architecture diagram.")
                    saved_path = self._save_image(chosen, pdf_path, output_folder)
                    return saved_path, caption
            except Exception as e:
                logger.error(f"Error in Vision selection: {e}")
                
            # Fallback: If vision fails, just save Page 1 render
            logger.info("Vision selection failed. Defaulting to Page 1 Render.")
            fallback = next((c for c in candidates if "Page 1" in c['source']), candidates[0])
            saved_path = self._save_image(fallback, pdf_path, output_folder)
            return saved_path, "Figure: Overview (Fallback Selection)"

        except Exception as e:
            logger.error(f"Error extracting images from PDF: {e}")
            return None, ""

    def _save_image(self, img_data, pdf_path, output_folder):
        paper_filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(paper_filename)[0]
        image_filename = f"{base_name}_arch.{img_data['ext']}"
        path = os.path.join(output_folder, image_filename)
        with open(path, "wb") as f:
            f.write(img_data["bytes"])
        return path

    def analyze_full_paper_iterative(self, paper, pdf_path, existing_notes_list):
        """
        Performs a multi-round deep analysis using Vision capabilities (PDF to Images).
        """
        logger.info(f"Starting Iterative Deep Analysis for: {paper['title']}")
        
        # Step 1: Convert PDF to images for Vision model
        # We process the first 8 pages which usually contain the main text
        images = self.pdf_to_base64_images(pdf_path, max_pages=8)
        
        if not images:
            logger.error("Failed to convert PDF to images. Fallback to text extraction.")
            # Fallback logic could go here, but for now we return error
            return "Failed to read PDF visually."

        # Construct Vision API messages
        vision_messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"This is the paper titled '{paper['title']}'. Please read it carefully page by page."}
                ]
            }
        ]
        
        # Add images to message
        for img_b64 in images:
            vision_messages[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img_b64}"}
            })

        # --- Round 1: Comprehensive Analysis & Academic Quality ---
        logger.info(f"  [Round 1] Performing initial academic quality & innovation assessment...")
        
        # Load custom prompts from config
        system_role = self.config['analysis']['prompts']['system_role']
        deep_analysis_prompt = self.config['analysis']['prompts']['deep_analysis']
        
        round1_prompt = f"""
        {deep_analysis_prompt}
        
        **Visual Context**: Please refer to the provided images to interpret figures and tables accurately.
        """
        
        # Copy vision messages for this turn
        messages_r1 = vision_messages.copy()
        # Update system role
        messages_r1.insert(0, {"role": "system", "content": system_role})
        messages_r1.append({"role": "user", "content": round1_prompt})
        
        response_r1 = self.client.chat.completions.create(
            model=self.model_pro,
            messages=messages_r1
        )
        r1_content = response_r1.choices[0].message.content

        # --- Round 2: Logical Optimization & Relation Analysis ---
        logger.info(f"  [Round 2] Building knowledge graph and future research directions...")
        
        context_notes = ', '.join(existing_notes_list[:50])
        
        round2_prompt = f"""
        Based on the analysis above, now perform a Connection & Refinement step.
        
        **Task 1: Knowledge Connections**
        - Connect this paper's concepts to my existing knowledge base: {context_notes}.
        - Use [[Wiki-Link]] format.
        
        **Task 2: Mermaid Knowledge Graph**
        - Generate a Mermaid JS code block (`graph LR` or `mindmap`) visualizing the paper's core concepts.
        - **STRICT MERMAID RULES**:
          1. Use ONLY English characters and numbers for Node IDs (e.g., A, B, Node1). No spaces or special chars in IDs.
          2. Put descriptive text in quotes or brackets (e.g., A["Descriptive Text"]).
          3. DO NOT use Chinese characters anywhere.
          4. Ensure all parentheses are balanced.
        
        **Task 3: Future Directions**
        - Propose 3 concrete research ideas based on this paper.
        """
        
        messages_r2 = messages_r1 + [
            {"role": "assistant", "content": r1_content},
            {"role": "user", "content": round2_prompt}
        ]
        
        response_r2 = self.client.chat.completions.create(
            model=self.model_pro,
            messages=messages_r2
        )
        r2_content = response_r2.choices[0].message.content

        # --- Final Compilation ---
        final_report = f"""
# 🚀 Deep Analysis Report: {paper['title']}

## 📊 Academic Quality & Innovation
{r1_content}

## 🔗 Knowledge Graph & Connections
{r2_content}

---
*Analysis performed by PaperBrain-Doubao (Vision-Enabled)*
"""
        return final_report
