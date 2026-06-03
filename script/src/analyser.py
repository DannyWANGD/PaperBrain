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

import yaml # Ensure yaml is imported
from src.scoring import (
    calibrated_screening_score,
    clamp_score,
    coarse_screening_score,
    normalize_red_flags,
)

class PaperAnalyser:
    def __init__(self, config, provider='doubao', prompts=None):
        self.config = config
        self.provider = provider
        self.prompts = prompts or {}
        self._openrouter_banned_authors = set()
        
        if provider == 'openrouter':
            self.api_key = config['openrouter']['api_key']
            self.base_url = "https://openrouter.ai/api/v1"
            self.model_flash = config['openrouter'].get('model_flash', 'deepseek/deepseek-v4-flash')
            self.model_screening_pro = config['openrouter'].get('model_screening_pro', self.model_flash)
            self.model_pro = config['openrouter'].get('model_pro', 'deepseek/deepseek-v4-pro')
            self.model_vision = config['openrouter'].get('model_vision', 'qwen/qwen3-vl-30b-a3b-thinking')
            logger.info(f"Using OpenRouter Provider. Flash: {self.model_flash}, Screening-Pro: {self.model_screening_pro}, Pro: {self.model_pro}, Vision: {self.model_vision}")
        else:
            self.api_key = config['doubao']['api_key']
            self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
            self.model_flash = config['doubao'].get('model_flash', 'doubao-seed-2-0-lite-260215')
            self.model_screening_pro = config['doubao'].get('model_screening_pro', self.model_flash)
            self.model_pro = config['doubao'].get('model_pro', 'doubao-seed-2-0-pro-260215')
            logger.info(f"Using Doubao Provider. Flash: {self.model_flash}, Screening-Pro: {self.model_screening_pro}, Pro: {self.model_pro}")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Load Tag Taxonomy
        self.tags_taxonomy = []
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate_paths = [
                os.path.join(script_dir, "config", "tags.yaml"),
                os.path.join(script_dir, "tags.yaml"),
            ]
            tags_path = next((p for p in candidate_paths if os.path.exists(p)), candidate_paths[0])
            with open(tags_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.tags_taxonomy = data.get('taxonomy', [])
        except Exception as e:
            logger.warning(f"Could not load tags.yaml: {e}")

    def _openrouter_model_candidates(self, primary_model: str, kind: str):
        if self.provider != 'openrouter':
            return [primary_model]

        cfg = self.config.get('openrouter', {})
        fallback_key = f"{kind}_fallbacks"
        fallbacks = cfg.get(fallback_key, [])
        if not isinstance(fallbacks, list):
            fallbacks = []

        defaults = []
        if kind == "model_flash":
            defaults = [
                "deepseek/deepseek-v4-flash",
                "stepfun/step-3.7-flash",
                "qwen/qwen3.6-flash",
                "z-ai/glm-4.7-flash",
                "deepseek/deepseek-v3.2",
            ]
        elif kind == "model_screening_pro":
            defaults = [
                "deepseek/deepseek-v4-pro",
                "x-ai/grok-4.3",
                "qwen/qwen3.7-max",
                "minimax/minimax-m3",
                "qwen/qwen3-max-thinking",
                "z-ai/glm-5.1",
                "moonshotai/kimi-k2.6",
            ]
        elif kind == "model_pro":
            defaults = [
                "deepseek/deepseek-v4-pro",
                "x-ai/grok-4.3",
                "qwen/qwen3.7-max",
                "minimax/minimax-m3",
                "z-ai/glm-5.1",
                "moonshotai/kimi-k2.6",
                "qwen/qwen3-max-thinking",
            ]
        elif kind == "model_vision":
            defaults = [
                "qwen/qwen3-vl-30b-a3b-thinking",
                "perceptron/perceptron-mk1",
                "minimax/minimax-m3",
                "stepfun/step-3.7-flash",
                "qwen/qwen3.5-plus-20260420",
                "z-ai/glm-5v-turbo",
                "moonshotai/kimi-k2.5",
            ]

        candidates = []
        for m in [primary_model, *fallbacks, *defaults]:
            if m and m not in candidates:
                candidates.append(m)
        if self._openrouter_banned_authors:
            filtered = []
            for m in candidates:
                author = (m.split("/", 1)[0] if "/" in m else "").strip().lower()
                if author and author in self._openrouter_banned_authors:
                    continue
                filtered.append(m)
            candidates = filtered
        return candidates

    def _chat_with_fallback(self, models, messages, **kwargs):
        last_err = None
        for model in models:
            try:
                return self.client.chat.completions.create(model=model, messages=messages, **kwargs), model
            except Exception as e:
                msg = str(e)
                last_err = e
                m = re.search(r"Author\s+([A-Za-z0-9_-]+)\s+is banned", msg)
                if m:
                    self._openrouter_banned_authors.add(m.group(1).strip().lower())
                if self.provider == 'openrouter' and (
                    "not available in your region" in msg
                    or "Error code: 403" in msg
                    or "Error code: 404" in msg
                ):
                    logger.warning(f"[WARN] OpenRouter model failed, trying fallback: {model} ({msg})")
                    continue
                raise
        raise last_err

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
        """Robustly extract a JSON object from LLM response text."""
        if not text:
            return "{}"
        # 1. Try direct parse first
        try:
            json.loads(text.strip())
            return text.strip()
        except Exception:
            pass
        # 2. Strip markdown code fences
        cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)
        try:
            json.loads(cleaned.strip())
            return cleaned.strip()
        except Exception:
            pass
        # 3. Extract outermost {...} block (non-greedy to avoid over-matching)
        m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", cleaned, re.DOTALL)
        if not m:
            # fallback: greedy match
            m = re.search(r"\{[\s\S]*\}", cleaned)
        if m:
            candidate = m.group(0)
            # Clean trailing commas
            candidate = re.sub(r',\s*}', '}', candidate)
            candidate = re.sub(r',\s*]', ']', candidate)
            try:
                json.loads(candidate)
                return candidate
            except Exception:
                pass
        # 4. Return original stripped text as last resort
        return text.strip()

    def _clamp_score(self, value, default=5.0):
        return clamp_score(value, default=default)

    def _short_title_from_title(self, title):
        title = title or ""
        short_title = title.split(':')[0].strip() if ':' in title else title.strip()
        return short_title.replace(' ', '_')

    def _taxonomy_prompt(self):
        taxonomy_str = ""
        if self.tags_taxonomy:
            taxonomy_str = "\n**Standard Tag Taxonomy (Choose from these if applicable):**\n"
            for tag in self.tags_taxonomy:
                taxonomy_str += f"- {tag['name']} (Aliases: {', '.join(tag['aliases'])})\n"
        return taxonomy_str

    def _screening_extra_params(self):
        return self._openrouter_extra_params("screening")

    def _openrouter_quality_params(self, stage="analysis"):
        if self.provider != 'openrouter':
            return {}
        cfg = self.config.get('openrouter', {})
        effort_key = {
            "screening": "reasoning_effort_screening",
            "vision": "reasoning_effort_vision",
        }.get(stage, "reasoning_effort_analysis")
        body = {
            "provider": {
                "sort": cfg.get("routing_sort", "throughput"),
                "data_collection": cfg.get("routing_data_collection", "deny"),
                "allow_fallbacks": True,
                "require_parameters": False,
            }
        }
        partition = cfg.get("routing_partition")
        if partition and str(partition).lower() != "none":
            body["provider"]["quantizations"] = [partition]
        effort = cfg.get(effort_key)
        if effort:
            body["reasoning"] = {"effort": effort}
        return {"extra_body": body}

    def _openrouter_extra_params(self, stage="analysis"):
        if self.provider != 'openrouter':
            return {}
        extra_params = {
            "extra_headers": {
                "HTTP-Referer": "https://paperbrain.ai",
                "X-Title": "PaperBrain"
            }
        }
        extra_params.update(self._openrouter_quality_params(stage))
        return extra_params

    def _run_with_model_fallback(self, label, models, messages, extra_params=None, **kwargs):
        call_kwargs = {}
        call_kwargs.update(extra_params or {})
        call_kwargs.update(kwargs)
        try:
            response, used_model = self._chat_with_fallback(
                models=models,
                messages=messages,
                **call_kwargs
            )
            logger.info(f"  [{label}] Used model: {used_model}")
            return response, used_model
        except Exception as e:
            logger.error(f"[{label}] All candidate models failed: {e}")
            return None, None

    def _message_content_text(self, response):
        """Return assistant content as plain text across OpenAI/OpenRouter response variants."""
        try:
            content = response.choices[0].message.content
        except Exception:
            return ""
        return self._content_to_text(content)

    def _content_to_text(self, content):
        """Normalize raw message content variants into plain text."""
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    text = item.get("text")
                    if text is None and isinstance(item.get("content"), str):
                        text = item.get("content")
                    if text is not None:
                        parts.append(str(text))
                else:
                    text = getattr(item, "text", None)
                    if text is not None:
                        parts.append(str(text))
            return "\n".join([p for p in parts if p]).strip()
        if isinstance(content, dict):
            for key in ("text", "content", "output_text"):
                if content.get(key) is not None:
                    return str(content.get(key))
            return json.dumps(content, ensure_ascii=False)
        return str(content)

    def _clean_generated_note(self, content, prefer_abstract_start=False):
        content = self._message_content_text(content) if hasattr(content, "choices") else self._content_to_text(content)
        content = re.sub(r'^\s*```(?:markdown|md)?\s*\n', '', content)
        content = re.sub(r'\n```\s*$', '', content.strip())
        content = re.sub(r"```json\s*(\{[\s\S]*?\"project_page\"[\s\S]*?\})\s*```", "", content, flags=re.DOTALL)
        content = re.sub(r"^\s*(\{[\s\S]*?\"project_page\"[\s\S]*?\})\s*", "", content, flags=re.MULTILINE)
        content = re.sub(r'^0\.\s*\*\*Metadata Extraction\*\*[^\n]*\n+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^#\s+.*Deep Analysis Report:.*?\n+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^##\s+.*Academic Quality & Innovation\s*\n+', '', content, flags=re.MULTILINE)
        if prefer_abstract_start:
            abstract_idx = content.find("## Abstract")
            if abstract_idx > 0:
                content = content[abstract_idx:]
        return re.sub(r'\n{3,}', '\n\n', content).strip()

    def _maybe_refine_analysis_note(self, paper, draft_note, paper_text, models_to_try, extra_params):
        analysis_cfg = self.config.get('analysis', {})
        if not analysis_cfg.get('refinement_pass_enabled', True):
            return draft_note, None

        refinement_template = self.prompts.get('analysis', {}).get('refinement_user')
        if not refinement_template:
            return draft_note, None

        max_draft_chars = int(analysis_cfg.get('refinement_max_chars', 45000))
        max_excerpt_chars = int(analysis_cfg.get('refinement_paper_excerpt_chars', 12000))
        draft_for_review = draft_note[:max_draft_chars]
        paper_excerpt = paper_text[:max_excerpt_chars]

        try:
            refinement_prompt = refinement_template.format(
                paper_title=paper.get('title', ''),
                paper_excerpt=paper_excerpt,
                draft_note=draft_for_review,
            )
        except Exception as e:
            logger.warning(f"[Refinement] Prompt formatting failed, keeping Round 1 draft: {e}")
            return draft_note, None

        logger.info("  [Refinement] Improving note structure, formulas, and readability...")
        messages_refine = [
            {
                "role": "system",
                "content": (
                    "You are a meticulous research-note editor. Improve clarity, factual caution, "
                    "Obsidian readability, and mathematical explanation without inventing unsupported facts."
                )
            },
            {"role": "user", "content": refinement_prompt}
        ]
        response_refine, used_model = self._run_with_model_fallback(
            label="Refinement",
            models=models_to_try,
            messages=messages_refine,
            extra_params=extra_params,
        )
        if response_refine is None:
            logger.warning("[Refinement] Keeping Round 1 draft because refinement failed.")
            return draft_note, None

        refined = self._clean_generated_note(
            self._message_content_text(response_refine),
            prefer_abstract_start=True,
        )
        if not refined or len(refined) < max(800, len(draft_note) * 0.35):
            logger.warning("[Refinement] Output looked incomplete, keeping Round 1 draft.")
            return draft_note, used_model

        return refined, used_model

    def _screening_fallback_payload(self, paper, reason, stage="detailed"):
        short_title_fallback = self._short_title_from_title(paper.get('title', ''))
        base = {
            "score": 0.0,
            "relevance": 0.0,
            "novelty": 0.0,
            "rigor": 0.0,
            "evidence": 0.0,
            "reproducibility": 0.0,
            "confidence": 0.0,
            "red_flags": [],
            "innovation": "Analysis failed",
            "limitations": "Analysis failed",
            "reason": str(reason),
            "tags": [],
            "short_title": short_title_fallback,
            "screening_stage": stage,
        }
        if stage == "coarse":
            base.update({
                "coarse_score": 0.0,
                "method_completeness": 0.0,
                "should_rescreen": False,
            })
        return base

    def coarse_screen_paper(self, paper):
        taxonomy_str = self._taxonomy_prompt()
        keywords = ', '.join(self.config['search']['keywords'])

        # Get prompt from prompts.yaml or use inline fallback
        system_prompt = self.prompts.get('screening', {}).get('coarse_system',
            "You are a careful research triage assistant. Be conservative, fast, and structured.")
        user_template = self.prompts.get('screening', {}).get('coarse_user', """
        You are performing the FIRST-PASS coarse screening for a robotics/AI paper pipeline.
        Evaluate only whether this paper is promising enough to enter a stricter second-stage review for these interests: {keywords}.

        Title: {title}
        Abstract: {abstract}

        {taxonomy_block}

        Score each dimension from 1.0-10.0 using one decimal place:
        - relevance: how well the paper matches the target interests.
        - evidence: how much concrete empirical/theoretical support is visible from the abstract.
        - method_completeness: whether the abstract describes a real method with enough mechanism detail to justify deeper review.

        Decision goal:
        - This is NOT the final accept/reject decision.
        - Be recall-oriented for high-potential work, but still filter obvious weak matches, shallow papers, and poorly supported work.
        - If the abstract is vague, underspecified, or clearly off-topic, set should_rescreen to false.

        Output requirements:
        - coarse_score: overall coarse priority for second-stage review.
        - should_rescreen: true only if this paper is worth spending a stronger model on.
        - reason: exactly 1 concise sentence stating why it should or should not enter second-stage review.

        Return JSON only:
        {{
            "coarse_score": number,
            "relevance": number,
            "evidence": number,
            "method_completeness": number,
            "should_rescreen": bool,
            "reason": "string"
        }}
        """)

        prompt = user_template.format(
            keywords=keywords,
            title=paper['title'],
            abstract=paper['abstract'],
            taxonomy_block=taxonomy_str
        )

        try:
            models = self._openrouter_model_candidates(self.model_flash, "model_flash")
            response, used_model = self._chat_with_fallback(
                models=models,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                **self._screening_extra_params()
            )

            data = json.loads(self._sanitize_json(self._message_content_text(response)), strict=False)
            relevance = self._clamp_score(data.get("relevance", data.get("coarse_score", 5)))
            evidence = self._clamp_score(data.get("evidence", data.get("coarse_score", 5)))
            method_completeness = self._clamp_score(data.get("method_completeness", data.get("coarse_score", 5)))
            coarse_score = coarse_screening_score(relevance, evidence, method_completeness)
            should_rescreen = data.get("should_rescreen")
            if not isinstance(should_rescreen, bool):
                should_rescreen = coarse_score >= 6 and relevance >= 6 and (evidence >= 5 or method_completeness >= 6)

            return {
                "coarse_score": coarse_score,
                "score": coarse_score,
                "relevance": relevance,
                "evidence": evidence,
                "method_completeness": method_completeness,
                "should_rescreen": should_rescreen,
                "reason": data.get("reason", ""),
                "short_title": self._short_title_from_title(paper.get('title', '')),
                "screening_stage": "coarse",
                "used_model": used_model,
            }
        except Exception as e:
            logger.error(f"Error coarse-screening paper {paper['title']}: {e}")
            return self._screening_fallback_payload(paper, e, stage="coarse")

    def screen_paper(self, paper):
        taxonomy_str = self._taxonomy_prompt()
        doc_excerpt = (paper.get('screening_document_excerpt') or '').strip()
        doc_context_block = ""
        if doc_excerpt:
            doc_context_block = f"""
        Additional document excerpt (from first PDF pages; may include methods/results details):
        {doc_excerpt}
        """
        keywords = ', '.join(self.config['search']['keywords'])

        system_prompt = self.prompts.get('screening', {}).get('detailed_system',
            "You are a senior research reviewer. Be objective, critical, conservative, and use consistent scoring standards.")
        user_template = self.prompts.get('screening', {}).get('detailed_user', """
        You are performing the SECOND-PASS rigorous screening for a robotics/AI research workflow.
        This paper has already passed a coarse triage stage. Your job is to make a high-quality final screening judgment.
        Evaluate expected research value for these interests: {keywords}.

        Title: {title}
        Abstract: {abstract}
        {doc_context_block}

        {taxonomy_block}

        Score each dimension from 1.0-10.0 using one decimal place:
        - relevance: fit to the target interests and application scope.
        - novelty: originality versus common baseline ideas.
        - rigor: methodological soundness and evaluation quality.
        - evidence: strength of empirical/theoretical support in the abstract.
        - reproducibility: clarity of setup, assumptions, and implementability signal.

        Overall score guidance:
        - 9-10: high relevance + high novelty + high rigor + strong evidence.
        - 7-8: strong paper with minor gaps.
        - 5-6: useful but incremental/partially matched.
        - 1-4: weak match or weak evidence/rigor.

        Calibration constraints:
        - treat the final score as a research-priority score, not as a paper-acceptance score.
        - do not let novelty alone compensate for poor relevance, weak evidence, or unclear methodology.
        - if relevance <= 4, overall score must be <= 6.
        - if rigor <= 4 or evidence <= 4, overall score must be <= 7.
        - if confidence <= 4, overall score must be <= 7.
        - if abstract lacks concrete method/evaluation details, reduce confidence and avoid optimistic scoring.
        - keep scoring conservative and discriminative.
        - if additional document excerpt is provided, use it as supporting evidence for rigor/evidence/reproducibility.
        - use red_flags for concrete risks only: missing baselines, vague evaluation, data leakage risk, unsupported claims, unclear task setup, weak reproducibility, or mismatch with the target research interests.
        - if abstract and excerpt conflict, prefer concrete technical details from the excerpt and lower confidence if inconsistency is severe.

        Output requirements:
        - innovation: exactly 1 sentence, concrete and technical.
        - limitations: exactly 1 sentence, concrete and technical.
        - reason: 1 concise sentence mentioning key drivers of score.
        - tags: 3-5 specific tags.
          - if concept matches taxonomy tag/alias above, MUST use the standard tag name.
          - use underscores; avoid generic tags like AI/Robotics.
        - short_title:
          - if title contains ":", use text before ":".
          - otherwise use full title.
          - replace spaces with underscores.

        Return JSON only:
        {{
            "score": number,
            "relevance": number,
            "novelty": number,
            "rigor": number,
            "evidence": number,
            "reproducibility": number,
            "confidence": number,
            "red_flags": ["string"],
            "innovation": "string",
            "limitations": "string",
            "reason": "string",
            "tags": ["string", "string", "string"],
            "short_title": "string"
        }}
        """)

        prompt = user_template.format(
            keywords=keywords,
            title=paper['title'],
            abstract=paper['abstract'],
            doc_context_block=doc_context_block,
            taxonomy_block=taxonomy_str
        )

        try:
            models = self._openrouter_model_candidates(self.model_screening_pro, "model_screening_pro")
            response, used_model = self._chat_with_fallback(
                models=models,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                **self._screening_extra_params()
            )

            content = self._message_content_text(response)
            cleaned_content = self._sanitize_json(content)
            data = json.loads(cleaned_content, strict=False)

            relevance = self._clamp_score(data.get("relevance", data.get("score", 5)))
            novelty = self._clamp_score(data.get("novelty", data.get("score", 5)))
            rigor = self._clamp_score(data.get("rigor", data.get("score", 5)))
            evidence = self._clamp_score(data.get("evidence", data.get("score", 5)))
            reproducibility = self._clamp_score(data.get("reproducibility", data.get("score", 5)))
            confidence = self._clamp_score(data.get("confidence", 6))
            red_flags = normalize_red_flags(data.get("red_flags", []))

            weights = self.config.get("analysis", {}).get("screening_weights", {})
            calibrated_score = calibrated_screening_score(
                relevance=relevance,
                novelty=novelty,
                rigor=rigor,
                evidence=evidence,
                reproducibility=reproducibility,
                confidence=confidence,
                red_flags=red_flags,
                weights=weights,
            )

            data["score"] = calibrated_score
            data["relevance"] = relevance
            data["novelty"] = novelty
            data["rigor"] = rigor
            data["evidence"] = evidence
            data["reproducibility"] = reproducibility
            data["confidence"] = confidence
            data["red_flags"] = red_flags
            data["short_title"] = data.get("short_title") or self._short_title_from_title(paper.get('title', ''))
            data["screening_stage"] = "detailed"
            data["used_model"] = used_model
            return data

        except Exception as e:
            logger.error(f"Error screening paper {paper['title']}: {e}")
            return self._screening_fallback_payload(paper, e, stage="detailed")

    def analyze_from_abstract(self, paper, rag_context=""):
        system_role = self.prompts.get('analysis', {}).get('system_role') or \
                      self.config.get('analysis', {}).get('prompts', {}).get('system_role', '')
        user_template = self.prompts.get('analysis', {}).get('abstract_fallback_user', """
        Generate a concise deep-analysis fallback report using only the title, abstract, and related notes context.
        If evidence is missing from abstract, explicitly mark as "Unknown from abstract".

        Title: {title}
        Abstract: {abstract}

        Related Notes Context:
        {rag_context}

        Output structure:
        1) Core Snapshot
        2) Technical Decomposition (only what can be inferred)
        3) Evidence & Metrics (unknown values explicitly marked)
        4) Critical Assessment
        """)
        prompt = user_template.format(
            title=paper.get('title', ''),
            abstract=paper.get('abstract', ''),
            rag_context=rag_context
        )

        extra_params = self._openrouter_extra_params("analysis")

        models = [self.model_pro]
        if self.provider == 'openrouter':
            models = self._openrouter_model_candidates(self.model_pro, "model_pro")

        response, used_model = self._chat_with_fallback(
            models=models,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            **extra_params
        )
        content = self._clean_generated_note(self._message_content_text(response))
        return f"{content}\n\n---\n*Generated from abstract fallback (model: {used_model})*"

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
        Intelligently extracts the model/logic architecture diagram from a research paper PDF.

        Strategy:
          Phase 1 — Full-text scan with two-tier keyword scoring to rank pages by
                    likelihood of containing an architecture figure.
          Phase 2 — Render top candidate pages as high-res images and ask a Vision LLM
                    to pick the best architecture/framework diagram.

        Returns (saved_path, caption) or (None, "").
        """
        try:
            doc = fitz.open(pdf_path)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # ── Phase 1: Full-text page scoring ──────────────────────────────
            STRONG_KW = re.compile(
                r'(architecture|framework|overview|pipeline|system design|'
                r'model overview|method overview|proposed method|our approach|'
                r'overall structure|our method|our framework|our pipeline|'
                r'proposed framework|proposed architecture|system overview)',
                re.IGNORECASE
            )
            WEAK_KW = re.compile(
                r'(module|network|workflow|diagram|schematic|block diagram|'
                r'inference|training pipeline|encoder|decoder|backbone|'
                r'data flow|processing pipeline)',
                re.IGNORECASE
            )
            FIG_CAPTION = re.compile(
                r'(Figure|Fig\.)\s*\d+', re.IGNORECASE
            )

            page_scores = []  # (page_index, score)
            for i in range(len(doc)):
                text = doc[i].get_text()
                score = 0
                has_fig = bool(FIG_CAPTION.search(text))
                strong_hits = len(STRONG_KW.findall(text))
                weak_hits = len(WEAK_KW.findall(text))
                if has_fig and strong_hits:
                    score = 10 + strong_hits
                elif strong_hits:
                    score = 5 + strong_hits
                elif has_fig and weak_hits:
                    score = 2 + weak_hits
                if score > 0:
                    page_scores.append((i, score))

            # Sort by score descending, take top 5 pages
            page_scores.sort(key=lambda x: x[1], reverse=True)
            target_pages = [p[0] for p in page_scores[:5]]

            # Fallback: if nothing matched, use pages 1-3 (skip page 0 which is often the title/teaser)
            if not target_pages:
                target_pages = list(range(min(1, len(doc)), min(4, len(doc))))

            # ── Phase 2: Render candidate pages ──────────────────────────────
            candidates = []
            for page_num in target_pages:
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5))
                img_bytes = pix.tobytes("png")
                candidates.append({
                    "bytes": img_bytes,
                    "ext": "png",
                    "source": f"Page {page_num + 1}",
                    "type": "rendered_page"
                })

            if not candidates:
                logger.warning("No candidate pages could be rendered.")
                return None, ""

            # ── Phase 3: Vision LLM selection ────────────────────────────────
            vision_prompt = self.prompts.get('analysis', {}).get('vision_select_user', """You are an expert at reading research papers. I will show you several rendered pages from a PDF.

Your task: find the page that contains the **model / method architecture diagram** — the figure that shows the overall structure of the proposed approach, with components, modules, data flow arrows, and technical labels.

**What counts as an architecture diagram:**
- Block diagrams showing model components and their connections
- Flowcharts depicting the method pipeline (input → processing stages → output)
- System schematics with named modules, arrows, and tensor/data annotations
- Training/inference pipeline overviews

**What does NOT count (reject these):**
- Teaser/splash images showing qualitative results, photos, or 3D renders
- Bar charts, line plots, scatter plots, or any quantitative result figures
- Tables (comparison tables, ablation tables)
- Qualitative comparison grids (side-by-side result images)
- Title pages or author information pages

**Rules:**
1. If multiple pages contain architecture-like figures, prefer the one showing the OVERALL method (not a sub-module detail).
2. If NO page contains a clear architecture diagram, return index -1.
3. Do NOT guess — only select a page if you can clearly see a structural diagram.

**Output:** Return ONLY a JSON object:
{"index": <int or -1>, "caption": "<figure caption if readable, else brief description>"}""")

            vision_messages = [{
                "role": "user",
                "content": [{"type": "text", "text": vision_prompt}]
            }]

            for idx, item in enumerate(candidates):
                b64_img = base64.b64encode(item["bytes"]).decode('utf-8')
                vision_messages[0]["content"].append({
                    "type": "text",
                    "text": f"[Page candidate {idx} — {item['source']}]:"
                })
                vision_messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{item['ext']};base64,{b64_img}"}
                })

            try:
                extra_params = self._openrouter_extra_params("vision")

                # Try dedicated non-OpenAI/Claude/Gemini vision models.
                models_to_try = [self.model_pro]
                if self.provider == 'openrouter':
                    models_to_try = self._openrouter_model_candidates(
                        getattr(self, "model_vision", self.model_pro),
                        "model_vision"
                    )
                response, _ = self._run_with_model_fallback(
                    label="Vision Select",
                    models=models_to_try,
                    messages=vision_messages,
                    extra_params=extra_params,
                    max_tokens=200,
                )

                if response is None:
                    raise RuntimeError("All vision models failed")

                choice_text = self._message_content_text(response).strip()
                cleaned_json = self._sanitize_json(choice_text)
                data = json.loads(cleaned_json, strict=False)

                best_idx = data.get("index", -1)
                caption = data.get("caption", "Architecture Diagram")

                if 0 <= best_idx < len(candidates):
                    chosen = candidates[best_idx]
                    logger.info(f"Vision selected {chosen['source']} as architecture diagram.")
                    saved_path = self._save_image(chosen, pdf_path, output_folder)
                    return saved_path, caption
                elif best_idx == -1:
                    logger.info("Vision LLM determined no architecture diagram exists in this paper.")
                    return None, ""

            except Exception as e:
                logger.error(f"Vision selection error: {e}")

            # Fallback: save the highest-scored page
            logger.info("Vision selection failed. Saving top-scored page as fallback.")
            saved_path = self._save_image(candidates[0], pdf_path, output_folder)
            return saved_path, "Architecture Diagram (fallback)"

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

    def _extract_figures_from_pdf(self, pdf_path, max_figures=5):
        """
        Extracts meaningful figure images from a PDF using PyMuPDF.
        Returns list of dicts: [{"bytes": ..., "ext": ..., "page": ..., "label": ...}]
        Filters out icons, logos, solid backgrounds via _is_valid_image.
        """
        figures = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(min(len(doc), 15)):
                page = doc.load_page(page_num)
                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]
                    try:
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        if self._is_valid_image(image_bytes):
                            figures.append({
                                "bytes": image_bytes,
                                "ext": base_image["ext"],
                                "page": page_num + 1,
                                "label": f"Figure from page {page_num + 1}"
                            })
                    except Exception:
                        continue
            doc.close()
        except Exception as e:
            logger.error(f"Error extracting figures from PDF: {e}")

        # Sort by size descending (larger images are more likely to be key figures)
        figures.sort(key=lambda x: len(x["bytes"]), reverse=True)
        return figures[:max_figures]

    def _extract_text_from_pdf_fitz(self, pdf_path, max_pages=12):
        """
        Extracts clean text from PDF using PyMuPDF (fitz).
        More reliable than pypdf for most academic papers.
        Stops before references section to save tokens.
        """
        try:
            doc = fitz.open(pdf_path)
            pages_text = []
            for i in range(min(len(doc), max_pages)):
                text = doc[i].get_text()
                # Stop if we hit the references section
                ref_match = re.search(r'^(References|Bibliography|REFERENCES)\s*$', text, re.MULTILINE)
                if ref_match:
                    pages_text.append(text[:ref_match.start()])
                    break
                pages_text.append(text)
            doc.close()
            full_text = "\n\n".join(pages_text)
            # Clean up excessive whitespace
            full_text = re.sub(r'\n{3,}', '\n\n', full_text)
            return full_text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with fitz: {e}")
            return ""

    def analyze_full_paper_iterative(self, paper, pdf_path, existing_notes_list, rag_context=""):
        """
        Performs a multi-round deep analysis using extracted text + selective figure images.

        Token-efficient approach:
          - Paper text is extracted as plain text via PyMuPDF (cheap text tokens)
          - Only key figures (filtered, max 5) are sent as images (expensive vision tokens)
          - Compared to sending 8 full-page renders, this saves 50-70% of token cost
        """
        logger.info(f"Starting Iterative Deep Analysis for: {paper['title']}")

        # Step 1: Extract text from PDF
        paper_text = self._extract_text_from_pdf_fitz(pdf_path, max_pages=12)
        if not paper_text:
            logger.warning("fitz text extraction failed, falling back to pypdf...")
            paper_text = self.extract_text_from_pdf(pdf_path)

        if not paper_text or len(paper_text) < 200:
            logger.error("Text extraction failed or too short. Falling back to full-page vision mode.")
            return self._analyze_full_paper_vision_fallback(paper, pdf_path, existing_notes_list, rag_context)

        # Step 2: Extract key figures from PDF
        figures = self._extract_figures_from_pdf(pdf_path, max_figures=5)
        logger.info(f"  Extracted {len(figures)} key figures from PDF.")

        # Step 3: Build messages — text as text, figures as images
        text_intro = (
            f"Below is the full text of the paper titled '{paper['title']}', "
            f"followed by {len(figures)} key figures extracted from the paper.\n\n"
            f"--- PAPER TEXT START ---\n{paper_text}\n--- PAPER TEXT END ---"
        )

        user_content = [{"type": "text", "text": text_intro}]

        for idx, fig in enumerate(figures):
            b64_img = base64.b64encode(fig["bytes"]).decode('utf-8')
            user_content.append({
                "type": "text",
                "text": f"\n[Figure {idx + 1} — {fig['label']}]:"
            })
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/{fig['ext']};base64,{b64_img}"}
            })

        base_messages = [{"role": "user", "content": user_content}]

        # --- Round 1: Comprehensive Analysis ---
        logger.info(f"  [Round 1] Academic quality & innovation assessment...")

        system_role = self.prompts.get('analysis', {}).get('system_role') or \
                      self.config.get('analysis', {}).get('prompts', {}).get('system_role', '')
        deep_analysis_prompt = self.prompts.get('analysis', {}).get('deep_analysis') or \
                               self.config.get('analysis', {}).get('prompts', {}).get('deep_analysis', '')
        round1_suffix = self.prompts.get('analysis', {}).get('round1_suffix', """
        **Context**: The paper text is provided above as plain text. Key figures are provided as images — refer to them when discussing architecture, data flow, or visual results. If a figure shows the method pipeline, describe it in detail within the Technical Decomposition section.

        **Mandatory Formatting**:
        - Create a section exactly named "## 📌 Abstract".
        - Under it, first place the complete English abstract from the paper.
        - After the abstract, add one short paragraph that explains the abstract in simpler English.
        - All section titles and prose must be in English.

        **Quality Gate — Self-check before outputting**:
        - Does every subsection contain at least one multi-sentence paragraph (not just bullets)?
        - Does the Technical Decomposition section trace the full pipeline from input to output?
        - Are all loss functions written in LaTeX with every variable defined?
        - Does the Critical Assessment name specific failure scenarios, not generic concerns?
        - If any answer is "no", revise that section before outputting.
        """)

        round1_prompt = f"{deep_analysis_prompt}\n\n{round1_suffix}"

        messages_r1 = [{"role": "system", "content": system_role}] + base_messages + [
            {"role": "user", "content": round1_prompt}
        ]

        extra_params = self._openrouter_extra_params("analysis")

        response_r1 = None
        used_model_round1 = self.model_pro
        models_to_try = [self.model_pro]
        if self.provider == 'openrouter':
            models_to_try = self._openrouter_model_candidates(self.model_pro, "model_pro")

        response_r1, used_model_round1 = self._run_with_model_fallback(
            label="Round 1",
            models=models_to_try,
            messages=messages_r1,
            extra_params=extra_params,
        )

        if response_r1 is None:
            logger.error("[Round 1] All models failed. Aborting.")
            return "Analysis Failed: All models unavailable."

        r1_content = self._message_content_text(response_r1)

        # Extract Metadata JSON (robust matching for various malformed formats)
        metadata = {}
        try:
            json_match = None
            # Pattern 1: Standard ```json {...} ```
            json_match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", r1_content, re.DOTALL)

            if not json_match:
                # Pattern 2: Without code fence, complete JSON object
                json_match = re.search(r"^\s*(\{[\s\S]*?\"project_page\"[\s\S]*?\})\s*$", r1_content, re.MULTILINE)

            if not json_match:
                # Pattern 3: Incomplete JSON (missing opening brace), try to reconstruct
                partial_match = re.search(r'^\s*"publication_date":\s*"[^"]*",\s*\n\s*"institutions":\s*\[[\s\S]*?\],\s*\n\s*"github":\s*"[^"]*",\s*\n\s*"project_page":\s*"[^"]*"\s*\n\s*\}', r1_content, re.MULTILINE)
                if partial_match:
                    # Reconstruct by adding opening brace
                    json_str = "{" + partial_match.group(0).strip()
                    try:
                        metadata = json.loads(json_str)
                        r1_content = r1_content.replace(partial_match.group(0), "").strip()
                        json_match = True  # Mark as handled
                    except Exception:
                        pass

            if json_match and not isinstance(json_match, bool):
                json_str = json_match.group(1).strip()
                metadata = json.loads(json_str)
                r1_content = r1_content.replace(json_match.group(0), "").strip()
                json_match = True

            if json_match:
                # Remove any leading "0. **Metadata Extraction**" header
                r1_content = re.sub(r'^0\.\s*\*\*Metadata Extraction\*\*[^\n]*\n+', '', r1_content, flags=re.MULTILINE)
                # Remove stray ```json or ``` markers
                r1_content = re.sub(r'^```json\s*\n', '', r1_content, flags=re.MULTILINE)
                r1_content = re.sub(r'^```\s*\n', '', r1_content, flags=re.MULTILINE)
                paper['metadata'] = metadata
                logger.info(f"  Extracted metadata: {metadata.get('institutions', [])} | {metadata.get('publication_date', 'Unknown')}")
        except Exception as e:
            logger.warning(f"Failed to extract metadata JSON: {e}")

        # Clean up any remaining markdown artifacts
        r1_content = re.sub(r'^#\s+🚀\s+Deep Analysis Report:.*?\n+', '', r1_content, flags=re.MULTILINE)
        r1_content = re.sub(r'^##\s+📊\s+Academic Quality & Innovation\s*\n+', '', r1_content, flags=re.MULTILINE)
        # Collapse excessive blank lines
        r1_content = re.sub(r'\n{3,}', '\n\n', r1_content).strip()

        r1_content, refinement_model = self._maybe_refine_analysis_note(
            paper=paper,
            draft_note=r1_content,
            paper_text=paper_text,
            models_to_try=models_to_try,
            extra_params=extra_params,
        )

        max_iterations = int(self.config.get('analysis', {}).get('max_iterations', 2))
        max_iterations = max(1, max_iterations)

        r2_content = ""
        if max_iterations >= 2:
            logger.info(f"  [Round 2] Knowledge graph and connections...")

            context_notes = rag_context if rag_context else ', '.join(existing_notes_list[:50])

            round2_template = self.prompts.get('analysis', {}).get('round2_user', """
            Based on the comprehensive analysis you produced above, now perform a Connection & Refinement step.

            ═══════════════════════════════════════════════════════════════
            WRITING RULES (same as Round 1 — do NOT regress to bullet-point skeletons)
            ═══════════════════════════════════════════════════════════════
            - Every task below must be answered in coherent paragraphs (≥3 sentences each).
            - Bullet points are allowed ONLY for structured data (link lists, Mermaid code).
            - Always close the reasoning loop: claim → evidence → implication.
            ═══════════════════════════════════════════════════════════════

            Output language: English for all prose.
            Keep proprietary names and technical terms in original English (method/model/dataset/loss/module/API/benchmark names, metric abbreviations like mAP/FID/IoU, and math symbols).
            Keep [[Wiki-Link]] filenames and Mermaid node IDs in English-safe format.

            {context_notes}

            **Task 1: Differential Analysis & Connections**
            For each of the TOP 3 most relevant papers from my knowledge base (listed above), write a dedicated paragraph that covers:
            - What specific technical component or research question is shared between this paper and the related note.
            - How this paper's approach differs from or improves upon the related note's method.
            - What the implication of this difference is.
            - Use [[Wiki-Link]] format for all note references.

            **Task 2: Mermaid Knowledge Graph**
            Generate a Mermaid JS code block (`graph LR`) that visualizes:
            - The paper's core method pipeline (input → key modules → output)
            - Connections to related work from the knowledge base (as dashed links)
            - **STRICT MERMAID RULES**:
              1. Use ONLY English characters and numbers for Node IDs. No spaces or special chars in IDs.
              2. Put descriptive text in quotes or brackets (e.g., A["Descriptive Text"]).
              3. DO NOT use Chinese characters anywhere in the Mermaid block.
              4. Ensure all parentheses are balanced.
              5. Do NOT output literal "\\\\n". Use "<br/>" for line breaks in labels.

            **Task 3: Future Directions**
            For each of 3 research directions, write a full paragraph (not bullets) containing:
            - A specific finding or limitation from this paper that motivates the direction.
            - A concrete experiment design that could be executed in 1-2 weeks.
            - The primary risk that could invalidate this direction and an early diagnostic to detect it.
            - How this direction connects to broader trends in the field.
            """)
            round2_prompt = round2_template.format(context_notes=context_notes)

            # Round 2 only needs the refined note and knowledge-base context.
            messages_r2 = [
                {"role": "system", "content": system_role},
                {"role": "user", "content": f"Here is the refined reading note:\n\n{r1_content}"},
                {"role": "user", "content": round2_prompt}
            ]

            response_r2, used_model_round2 = self._run_with_model_fallback(
                label="Round 2",
                models=models_to_try,
                messages=messages_r2,
                extra_params=extra_params,
            )

            if response_r2 is None:
                logger.error("[Round 2] All models failed.")
            else:
                r2_content = self._message_content_text(response_r2)
                # Strip any stray section headers the model may have added
                r2_content = re.sub(r'^##\s+🔗\s+Knowledge Graph[^\n]*\n+', '', r2_content, flags=re.MULTILINE)
                r2_content = re.sub(r'^Analysis\s*&\s*Connections\s*\n+', '', r2_content, flags=re.MULTILINE)
                r2_content = re.sub(r'^###\s+Task\s+\d+[^\n]*\n', '', r2_content, flags=re.MULTILINE)
                r2_content = re.sub(r'^\*\*Task\s+\d+[^\n]*\n', '', r2_content, flags=re.MULTILINE)
                r2_content = re.sub(r'\n{3,}', '\n\n', r2_content).strip()

        # --- Final Compilation ---
        connections_section = ""
        if r2_content:
            connections_section = f"\n\n## Knowledge Graph & Connections\n\n{r2_content.strip()}"

        refinement_note = f"; refinement: {refinement_model}" if refinement_model else ""
        final_report = f"{r1_content.strip()}{connections_section}\n\n---\n*Analysis by PaperBrain ({used_model_round1}{refinement_note})*"
        return final_report

    def generate_paper_aliases(self, paper, analysis_text=""):
        """
        Uses flash model to generate 5-10 searchable aliases for the paper.
        Returns a list of strings.
        """
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        innovation = paper.get('innovation', '')

        # Take first 500 chars of analysis if provided
        analysis_snippet = analysis_text[:500] if analysis_text else ""

        user_template = self.prompts.get('analysis', {}).get('alias_generation_user', """
        Given the following paper, generate 5-10 concise, searchable aliases that other researchers might use to refer to this work.
        Focus on: method names, key technical terms, acronyms, and distinctive concepts introduced by this paper.
        Aliases should be specific enough to uniquely identify this paper's contributions (avoid generic terms like "robot" or "model").

        Title: {title}
        Abstract: {abstract}
        Key innovation: {innovation}

        Return ONLY a JSON array of strings, e.g.: ["Alias One", "AliasTwo", "Key_Term"]
        Each alias should be 1-4 words. Prefer English. No duplicates.
        """)

        prompt = user_template.format(
            title=title,
            abstract=abstract[:300],
            innovation=innovation
        )

        try:
            models = self._openrouter_model_candidates(self.model_flash, "model_flash")
            response, _ = self._chat_with_fallback(
                models=models,
                messages=[
                    {"role": "system", "content": "You are a research metadata assistant. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                **self._screening_extra_params()
            )

            content = self._message_content_text(response) or ""
            # Extract JSON array
            match = re.search(r'\[.*?\]', content, re.DOTALL)
            if match:
                aliases = json.loads(match.group(0))
                if isinstance(aliases, list):
                    return [str(a).strip() for a in aliases if a][:10]
        except Exception as e:
            logger.warning(f"Alias generation failed: {e}")

        return []

    def _analyze_full_paper_vision_fallback(self, paper, pdf_path, existing_notes_list, rag_context=""):
        """
        Fallback: sends full page renders when text extraction fails.
        This is the old approach, kept as a safety net.
        """
        logger.info("  Using full-page vision fallback mode...")
        images = self.pdf_to_base64_images(pdf_path, max_pages=8)
        if not images:
            return "Failed to read PDF."

        vision_messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": f"This is the paper titled '{paper['title']}'. Please read it carefully page by page."}
            ] + [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}
                for img in images
            ]
        }]

        system_role = self.prompts.get('analysis', {}).get('system_role') or \
                      self.config.get('analysis', {}).get('prompts', {}).get('system_role', '')
        deep_analysis_prompt = self.prompts.get('analysis', {}).get('deep_analysis') or \
                               self.config.get('analysis', {}).get('prompts', ).get('deep_analysis', '')
        vision_suffix = self.prompts.get('analysis', {}).get('vision_fallback_suffix', """
        **Visual Context**: Please refer to the provided images to interpret figures and tables accurately.
        **Mandatory Formatting**:
        - Create a section exactly named "## 📌 Abstract".
        - Under it, first place the complete English abstract from the paper.
        - After the abstract, add one short paragraph that explains the abstract in simpler English.
        - All section titles and prose must be in English.
        """)
        round1_prompt = f"{deep_analysis_prompt}\n\n{vision_suffix}"

        messages_r1 = [{"role": "system", "content": system_role}] + vision_messages + [
            {"role": "user", "content": round1_prompt}
        ]

        extra_params = self._openrouter_extra_params("vision")

        models_to_try = [self.model_pro]
        if self.provider == 'openrouter':
            models_to_try = self._openrouter_model_candidates(self.model_pro, "model_pro")

        response_r1, used_model = self._run_with_model_fallback(
            label="Vision Fallback R1",
            models=models_to_try,
            messages=messages_r1,
            extra_params=extra_params,
        )

        if response_r1 is None:
            return "Analysis Failed: All models unavailable."

        r1_content = self._message_content_text(response_r1)

        metadata = {}
        try:
            json_match = None
            json_match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", r1_content, re.DOTALL)
            if not json_match:
                json_match = re.search(r"^\s*(\{[\s\S]*?\"project_page\"[\s\S]*?\})\s*$", r1_content, re.MULTILINE)
            if not json_match:
                partial_match = re.search(r'^\s*"publication_date":\s*"[^"]*",\s*\n\s*"institutions":\s*\[[\s\S]*?\],\s*\n\s*"github":\s*"[^"]*",\s*\n\s*"project_page":\s*"[^"]*"\s*\n\s*\}', r1_content, re.MULTILINE)
                if partial_match:
                    try:
                        metadata = json.loads("{" + partial_match.group(0).strip())
                        r1_content = r1_content.replace(partial_match.group(0), "").strip()
                        json_match = True
                    except Exception:
                        pass
            if json_match and not isinstance(json_match, bool):
                metadata = json.loads(json_match.group(1).strip())
                r1_content = r1_content.replace(json_match.group(0), "").strip()
                json_match = True
            if json_match:
                r1_content = re.sub(r'^0\.\s*\*\*Metadata Extraction\*\*[^\n]*\n+', '', r1_content, flags=re.MULTILINE)
                r1_content = re.sub(r'^```json\s*\n', '', r1_content, flags=re.MULTILINE)
                r1_content = re.sub(r'^```\s*\n', '', r1_content, flags=re.MULTILINE)
                paper['metadata'] = metadata
        except Exception:
            pass

        r1_content = self._clean_generated_note(r1_content, prefer_abstract_start=True)

        r1_content, refinement_model = self._maybe_refine_analysis_note(
            paper=paper,
            draft_note=r1_content,
            paper_text="Vision fallback mode. Full reliable text excerpt is not available.",
            models_to_try=models_to_try,
            extra_params=self._openrouter_extra_params("analysis"),
        )

        refinement_note = f"; refinement: {refinement_model}" if refinement_model else ""
        return f"{r1_content.strip()}\n\n---\n*Analysis by PaperBrain ({used_model or self.model_pro}{refinement_note}) - Vision Fallback Mode*"
