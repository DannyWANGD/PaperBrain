import os
import re
import json
from collections import Counter, defaultdict
from datetime import datetime
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# Cross-theme relationship map: which themes are related to each other
THEME_RELATIONS = {
    "Theme_Embodied_AI_System":       ["Theme_Robot_Manipulation_General", "Theme_Sim2Real", "Theme_VLA_Policy", "Theme_Foundation_LLM"],
    "Theme_Robot_Manipulation_General": ["Theme_Embodied_AI_System", "Theme_Dexterous_Contact", "Theme_Diffusion_Policy", "Theme_Sim2Real"],
    "Theme_Dexterous_Contact":        ["Theme_Robot_Manipulation_General", "Theme_Sim2Real", "Theme_Imitation_HRI"],
    "Theme_VLA_Policy":               ["Theme_VLA_Reasoning", "Theme_Foundation_LLM", "Theme_Diffusion_Policy", "Theme_World_Model_Dynamics"],
    "Theme_VLA_Reasoning":            ["Theme_VLA_Policy", "Theme_Foundation_LLM", "Theme_Model_Based_Planning"],
    "Theme_World_Model_Dynamics":     ["Theme_Video_World_Model", "Theme_Model_Based_Planning", "Theme_RL_Algorithms"],
    "Theme_Video_World_Model":        ["Theme_World_Model_Dynamics", "Theme_Diffusion_Policy", "Theme_VLA_Policy"],
    "Theme_Model_Based_Planning":     ["Theme_World_Model_Dynamics", "Theme_RL_Algorithms", "Theme_VLA_Reasoning"],
    "Theme_RL_Algorithms":            ["Theme_Reward_Credit", "Theme_Model_Based_Planning", "Theme_Sim2Real"],
    "Theme_Reward_Credit":            ["Theme_RL_Algorithms", "Theme_VLA_Policy"],
    "Theme_Diffusion_Policy":         ["Theme_VLA_Policy", "Theme_Video_World_Model", "Theme_Robot_Manipulation_General"],
    "Theme_Foundation_LLM":           ["Theme_VLA_Policy", "Theme_VLA_Reasoning", "Theme_Multimodal_Perception"],
    "Theme_Sim2Real":                 ["Theme_Embodied_AI_System", "Theme_RL_Algorithms", "Theme_Robot_Manipulation_General"],
    "Theme_3D_Perception":            ["Theme_Embodied_AI_System", "Theme_World_Model_Dynamics", "Theme_Robot_Manipulation_General"],
    "Theme_Imitation_HRI":            ["Theme_Robot_Manipulation_General", "Theme_Foundation_LLM", "Theme_Dexterous_Contact"],
    "Theme_Multimodal_Perception":    ["Theme_Foundation_LLM", "Theme_VLA_Policy", "Theme_3D_Perception"],
}
class ThemeManager:
    def __init__(self, config, provider="openrouter", themes=None, prompts=None):
        self.config = config
        self.provider = provider
        self.prompts = prompts or {}
        self.vault_path = config["obsidian"]["vault_path"]
        self.notes_folder = os.path.join(self.vault_path, config["obsidian"]["detailed_notes_folder"])
        self.themes_folder = os.path.join(self.vault_path, config["obsidian"].get("themes_folder", "Research_Themes"))
        os.makedirs(self.themes_folder, exist_ok=True)
        # Load theme definitions from external yaml if provided, else fall back to hardcoded
        if themes and themes.get("themes"):
            self.theme_defs = themes["themes"]
            self.theme_relations = themes.get("relations", THEME_RELATIONS)
        else:
            self.theme_defs = self._default_theme_definitions()
            self.theme_relations = THEME_RELATIONS
        self.enrich_cfg = self.config.get("theme_enrichment", {})
        self.enrich_enabled = bool(self.enrich_cfg.get("enabled", True))
        self.enrich_model = ""
        self.client = None
        self._init_ai_client()

    def _init_ai_client(self):
        if not self.enrich_enabled:
            return
        try:
            if self.provider == "openrouter":
                api_key = self.config.get("openrouter", {}).get("api_key", "")
                base_url = "https://openrouter.ai/api/v1"
                self.enrich_model = self.enrich_cfg.get("openrouter_model") or self.config.get("openrouter", {}).get("model_flash", "google/gemini-3.1-flash-lite-preview")
            else:
                api_key = self.config.get("doubao", {}).get("api_key", "")
                base_url = "https://ark.cn-beijing.volces.com/api/v3"
                self.enrich_model = self.enrich_cfg.get("doubao_model") or self.config.get("doubao", {}).get("model_flash", "")
            if not api_key or not self.enrich_model:
                self.enrich_enabled = False
                return
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        except Exception:
            self.enrich_enabled = False

    def _safe_json_load(self, text):
        """Parse JSON from model output, handling markdown code fences and truncation."""
        if not text:
            logger.warning("[JSON Parse] Empty response")
            return {}
        # Strip markdown code fences
        text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
        text = re.sub(r"\s*```$", "", text.strip(), flags=re.MULTILINE)
        # Try direct parse first
        try:
            return json.loads(text.strip())
        except Exception as e1:
            logger.debug(f"[JSON Parse] Direct parse failed: {e1}")
        # Extract outermost {...} block (non-greedy)
        m = re.search(r"\{[\s\S]*?\}", text)
        if not m:
            logger.warning("[JSON Parse] No JSON block found")
            return {}
        raw = m.group(0)
        # Clean trailing commas
        raw = re.sub(r',\s*}', '}', raw)
        raw = re.sub(r',\s*]', ']', raw)
        try:
            return json.loads(raw)
        except Exception as e2:
            logger.debug(f"[JSON Parse] Cleaned parse failed: {e2}")
            # Attempt to repair truncated JSON: close open arrays/objects
            repaired = raw
            open_brackets = repaired.count("[") - repaired.count("]")
            open_braces = repaired.count("{") - repaired.count("}")
            # Remove trailing incomplete string/value
            repaired = re.sub(r',?\s*"[^"]*$', "", repaired)
            repaired = re.sub(r',?\s*$', "", repaired)
            repaired += "]" * max(0, open_brackets) + "}" * max(0, open_braces)
            try:
                return json.loads(repaired)
            except Exception as e3:
                logger.warning(f"[JSON Parse] Repair failed: {e3}")
                return {}

    def _build_notes_brief(self, matched_notes):
        top_notes = sorted(matched_notes, key=lambda x: x.get("score", 0), reverse=True)[:12]
        lines = []
        for n in top_notes:
            contrib = n.get("core_contribution", "")[:120].replace("\n", " ")
            lim = n.get("limitations", "")[:80].replace("\n", " ")
            lines.append(
                f"- [{n['note_name']}] score={n.get('score',0)} | "
                f"contribution: {contrib or 'N/A'} | "
                f"limitation: {lim or 'N/A'} | "
                f"tags: {','.join(n.get('tags',[])[:5])}"
            )
        return "\n".join(lines)

    def _call_enrich_api(self, prompt, max_tokens, retries=2):
        """Single API call with retry. Returns raw text or empty string."""
        extra_params = {}
        if self.provider == "openrouter":
            extra_params["extra_headers"] = {
                "HTTP-Referer": "https://paperbrain.ai",
                "X-Title": "PaperBrain"
            }
        temperature = float(self.enrich_cfg.get("temperature", 0.2))
        system_msg = self.prompts.get("theme_enrichment", {}).get(
            "system", "You are a precise research synthesis engine. Output valid JSON only."
        )
        for attempt in range(1, retries + 1):
            try:
                rsp = self.client.chat.completions.create(
                    model=self.enrich_model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **extra_params
                )
                return rsp.choices[0].message.content or ""
            except Exception as e:
                logger.warning(f"[Theme Enrich] API attempt {attempt}/{retries} failed: {e}")
        return ""

    def _to_str_list(self, data, key):
        """Accept list of strings OR list of dicts; always return list of strings."""
        items = data.get(key, [])
        if not isinstance(items, list):
            return []
        result = []
        for item in items:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                parts = []
                for f in ("title", "paper", "name", "work"):
                    if item.get(f):
                        parts.append(f"**{item[f]}**")
                        break
                for f in ("contribution", "note", "description", "significance", "why", "summary"):
                    if item.get(f):
                        parts.append(str(item[f]))
                        break
                if parts:
                    result.append(" — ".join(parts))
        return result

    def _generate_enrichment_batch1(self, theme, notes_brief):
        """Batch 1: landmark_works + frontier_signals + systematic_links"""
        fallback = {"landmark_works": [], "frontier_signals": [], "systematic_links": []}
        tpl = self.prompts.get("theme_enrichment", {}).get("batch1_user", "")
        if tpl:
            prompt = tpl.format(
                theme_title=theme["title"],
                theme_id=theme["id"],
                theme_parent=theme.get("parent", ""),
                theme_keywords=", ".join(theme.get("keywords", [])),
                notes_brief=notes_brief,
            )
        else:
            # inline fallback
            prompt = (
                f"Theme: {theme['title']} (ID: {theme['id']})\n"
                f"Keywords: {', '.join(theme.get('keywords', []))}\n\n"
                f"Papers:\n{notes_brief}\n\n"
                "Return JSON with keys: landmark_works (10-15 real papers), "
                "frontier_signals (3-5 Chinese bullets), systematic_links (3-5 Chinese bullets)."
            )
        raw = self._call_enrich_api(prompt, max_tokens=3000)
        if not raw:
            return fallback
        data = self._safe_json_load(raw)
        return {
            "landmark_works":   self._to_str_list(data, "landmark_works"),
            "frontier_signals": self._to_str_list(data, "frontier_signals"),
            "systematic_links": self._to_str_list(data, "systematic_links"),
        }

    def _generate_enrichment_batch2(self, theme, notes_brief):
        """Batch 2: open_questions + visual_map_mermaid + weekly_actions"""
        fallback = {"open_questions": [], "visual_map_mermaid": "", "weekly_actions": []}
        tpl = self.prompts.get("theme_enrichment", {}).get("batch2_user", "")
        if tpl:
            prompt = tpl.format(
                theme_title=theme["title"],
                theme_id=theme["id"],
                theme_keywords=", ".join(theme.get("keywords", [])),
                notes_brief=notes_brief,
            )
        else:
            prompt = (
                f"Theme: {theme['title']} (ID: {theme['id']})\n"
                f"Keywords: {', '.join(theme.get('keywords', []))}\n\n"
                f"Papers:\n{notes_brief}\n\n"
                "Return JSON with keys: open_questions (3-4 Chinese questions), "
                "visual_map_mermaid (Mermaid graph LR code), weekly_actions (3-4 Chinese suggestions)."
            )
        raw = self._call_enrich_api(prompt, max_tokens=3000)
        if not raw:
            return fallback
        data = self._safe_json_load(raw)
        mermaid = data.get("visual_map_mermaid", "")
        return {
            "open_questions":     self._to_str_list(data, "open_questions"),
            "visual_map_mermaid": mermaid if isinstance(mermaid, str) else "",
            "weekly_actions":     self._to_str_list(data, "weekly_actions"),
        }

    def _generate_ai_enrichment(self, theme, matched_notes):
        """Coordinates two batch requests and merges results."""
        fallback = {
            "landmark_works": [], "frontier_signals": [], "systematic_links": [],
            "open_questions": [], "visual_map_mermaid": "", "weekly_actions": [],
        }
        if not self.enrich_enabled or not self.client or not matched_notes:
            return fallback
        notes_brief = self._build_notes_brief(matched_notes)
        batch1 = self._generate_enrichment_batch1(theme, notes_brief)
        batch2 = self._generate_enrichment_batch2(theme, notes_brief)
        return {**fallback, **batch1, **batch2}

    def _default_theme_definitions(self):
        return [
            # 1. 具身智能系统与平台
            {
                "id": "Theme_Embodied_AI_System",
                "title": "具身智能系统与平台",
                "parent": "Embodied AI",
                "keywords": [
                    "embodied ai", "robot system", "humanoid", "mobile manipulation",
                    "whole-body control", "cross-embodiment", "universal embodiment",
                    "multi-robot", "robot platform", "system integration",
                ],
                "tags": ["Embodied_AI"],
            },
            # 2. 通用机器人操作
            {
                "id": "Theme_Robot_Manipulation_General",
                "title": "通用机器人操作",
                "parent": "Robot Manipulation",
                "keywords": [
                    "robot manipulation", "manipulation", "pick-and-place",
                    "object manipulation", "tabletop", "bimanual", "tool use",
                    "generalist manipulation", "open-world manipulation",
                ],
                "tags": ["Robot_Manipulation", "Embodied_AI"],
            },
            # 3. 灵巧操作与接触丰富任务
            {
                "id": "Theme_Dexterous_Contact",
                "title": "灵巧操作与接触丰富任务",
                "parent": "Robot Manipulation",
                "keywords": [
                    "dexterous", "in-hand", "contact-rich", "grasping", "hand",
                    "tactile", "force control", "assembly", "deformable",
                    "extrinsic dexterity",
                ],
                "tags": ["Robot_Manipulation"],
            },
            # 4. VLA 策略学习与控制
            {
                "id": "Theme_VLA_Policy",
                "title": "VLA 策略学习与控制",
                "parent": "VLA",
                "keywords": [
                    "vision-language-action", "vla", "action model", "openvla",
                    "rt-2", "pi0", "generalist policy", "pretrained policy",
                    "action chunking", "flow matching vla",
                ],
                "tags": ["VLA", "Embodied_AI"],
            },
            # 5. VLA 推理、规划与泛化
            {
                "id": "Theme_VLA_Reasoning",
                "title": "VLA 推理、规划与泛化",
                "parent": "VLA",
                "keywords": [
                    "reasoning", "planning", "chain-of-thought", "affordance",
                    "high-level planning", "task planning", "zero-shot generalization",
                    "open-vocabulary", "language grounding",
                ],
                "tags": ["VLA", "LLM"],
            },
            # 6. 世界模型与潜在动力学
            {
                "id": "Theme_World_Model_Dynamics",
                "title": "世界模型与潜在动力学",
                "parent": "World Model",
                "keywords": [
                    "world model", "latent dynamics", "predictive model",
                    "imagination", "rssm", "latent world model",
                    "model-based", "environment model",
                ],
                "tags": ["World_Model"],
            },
            # 7. 视频生成式世界模型
            {
                "id": "Theme_Video_World_Model",
                "title": "视频生成式世界模型",
                "parent": "World Model",
                "keywords": [
                    "video world model", "video diffusion", "world action model",
                    "action-conditioned video", "video generation", "video prediction",
                    "4d world", "interactive video",
                ],
                "tags": ["World_Model", "Diffusion_Model"],
            },
            # 8. 基于模型的规划与决策
            {
                "id": "Theme_Model_Based_Planning",
                "title": "基于模型的规划与决策",
                "parent": "World Model",
                "keywords": [
                    "model-based planning", "trajectory optimization", "lookahead",
                    "rollout", "mpc", "tree search", "latent planning",
                    "imagination-based planning",
                ],
                "tags": ["World_Model", "Reinforcement_Learning"],
            },
            # 9. 强化学习算法
            {
                "id": "Theme_RL_Algorithms",
                "title": "强化学习算法",
                "parent": "Reinforcement Learning",
                "keywords": [
                    "reinforcement learning", "rl", "ppo", "sac", "grpo",
                    "policy gradient", "actor-critic", "online rl",
                    "offline rl", "model-free rl",
                ],
                "tags": ["Reinforcement_Learning"],
            },
            # 10. 奖励建模与信用分配
            {
                "id": "Theme_Reward_Credit",
                "title": "奖励建模与信用分配",
                "parent": "Reinforcement Learning",
                "keywords": [
                    "reward model", "reward shaping", "credit assignment",
                    "value function", "return decomposition", "intrinsic reward",
                    "vlm reward", "preference learning",
                ],
                "tags": ["Reinforcement_Learning"],
            },
            # 11. 扩散策略与生成式动作
            {
                "id": "Theme_Diffusion_Policy",
                "title": "扩散策略与生成式动作",
                "parent": "Diffusion Model",
                "keywords": [
                    "diffusion policy", "ddpm", "denoising", "flow matching",
                    "score matching", "action diffusion", "dit policy",
                    "consistency policy",
                ],
                "tags": ["Diffusion_Model", "Robot_Manipulation"],
            },
            # 12. 基础模型与 LLM 驱动机器人
            {
                "id": "Theme_Foundation_LLM",
                "title": "基础模型与 LLM 驱动机器人",
                "parent": "Foundation Models",
                "keywords": [
                    "foundation model", "large language model", "llm", "vlm",
                    "multimodal", "gpt", "code as policy", "saycan",
                    "language conditioned", "instruction following",
                ],
                "tags": ["Foundation_Model", "LLM"],
            },
            # 13. Sim-to-Real 迁移
            {
                "id": "Theme_Sim2Real",
                "title": "Sim-to-Real 迁移",
                "parent": "Sim2Real",
                "keywords": [
                    "sim2real", "domain randomization", "sim-to-real",
                    "synthetic data", "domain adaptation", "zero-shot transfer",
                    "physics simulation", "isaac gym", "mujoco",
                ],
                "tags": ["Sim2Real", "Embodied_AI"],
            },
            # 14. 3D/4D 感知与场景表征
            {
                "id": "Theme_3D_Perception",
                "title": "3D/4D 感知与场景表征",
                "parent": "3D Perception",
                "keywords": [
                    "3d gaussian", "gaussian splatting", "nerf", "4d reconstruction",
                    "point cloud", "depth estimation", "3d representation",
                    "scene reconstruction", "monocular", "multi-view", "spatial",
                ],
                "tags": ["3D_Gaussian_Splatting", "Embodied_AI"],
            },
            # 15. 模仿学习与人机交互
            {
                "id": "Theme_Imitation_HRI",
                "title": "模仿学习与人机交互",
                "parent": "Imitation Learning",
                "keywords": [
                    "imitation learning", "behavior cloning", "demonstration",
                    "teleoperation", "human motion", "mocap",
                    "hand-object interaction", "hoi", "egocentric",
                ],
                "tags": ["Robot_Manipulation", "Embodied_AI"],
            },
            # 16. 多模态感知与表征学习
            {
                "id": "Theme_Multimodal_Perception",
                "title": "多模态感知与表征学习",
                "parent": "Foundation Models",
                "keywords": [
                    "multimodal", "visual representation", "vision encoder",
                    "contrastive learning", "clip", "siglip", "visual pretraining",
                    "tactile", "multi-sensor", "situated awareness",
                ],
                "tags": ["Foundation_Model", "Embodied_AI"],
            },
        ]

    def _normalize(self, text):
        t = (text or "").lower()
        t = t.replace("-", "_").replace(" ", "_")
        return re.sub(r"[^a-z0-9_]", "", t)

    def _extract_manual_block(self, content):
        m = re.search(r"<!-- MANUAL_START -->([\s\S]*?)<!-- MANUAL_END -->", content)
        return m.group(1).strip() if m else "- [ ] 在本主题补充 1 个本周实验想法"

    def _parse_note(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = f.read()
        except Exception:
            return None
        front = ""
        body = raw
        fm = re.match(r"^---\n([\s\S]*?)\n---\n([\s\S]*)$", raw)
        if fm:
            front = fm.group(1)
            body = fm.group(2)
        score_match = re.search(r"^score:\s*([0-9]+)", front, re.MULTILINE)
        score = int(score_match.group(1)) if score_match else 0
        url_match = re.search(r"^url:\s*(.+)$", front, re.MULTILINE)
        url = url_match.group(1).strip() if url_match else ""
        pub_match = re.search(r'^publication_date:\s*"?([^"\n]+)"?', front, re.MULTILINE)
        pub = pub_match.group(1).strip() if pub_match else "Unknown"
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(file_path))[0]
        tags = []
        tags_block = re.search(r"^tags:\n([\s\S]*?)(?:\n[a-zA-Z_][a-zA-Z0-9_]*:|\Z)", front, re.MULTILINE)
        if tags_block:
            raw_tags = [t.strip().strip('"') for t in re.findall(r"^\s*-\s*(.+)$", tags_block.group(1), re.MULTILINE)]
            tags = []
            for t in raw_tags:
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t):
                    continue
                tags.append(t)
        note_name = os.path.splitext(os.path.basename(file_path))[0]
        core_contribution = self._extract_section(body,
            "Core Contribution", "核心贡献（Core Contribution）", "核心贡献",
            "Core Snapshot", "1. Core Snapshot", "核心摘要（Core Snapshot）")
        key_results = self._extract_section(body,
            "Key Results", "3. Evidence & Metrics", "证据与指标（Evidence & Metrics）",
            "Benchmark & Baselines", "Key Results & Analysis")
        limitations = self._extract_section(body,
            "Hidden Limitations", "4. Critical Assessment",
            "批判性评估（Critical Assessment）", "局限性", "Hidden Limitations & Risks")
        connections = self._extract_connections(body)
        return {
            "path": file_path,
            "note_name": note_name,
            "title": title,
            "score": score,
            "url": url,
            "pub": pub,
            "tags": tags,
            "body": body,
            "core_contribution": core_contribution,
            "key_results": key_results,
            "limitations": limitations,
            "connections": connections,
        }

    def _extract_section(self, body, *section_names):
        """Extracts the first item/paragraph of a named section, trying each name in order.
        Matches both ## and ### level headings."""
        for section_name in section_names:
            # Match both ## and ### headings, with optional numbering prefix
            pattern = rf"#{2,3}\s+(?:\d+\.?\d*\s+)?{re.escape(section_name)}\s*\n([\s\S]*?)(?:\n#{2,3}\s|\Z)"
            m = re.search(pattern, body, re.IGNORECASE)
            if not m:
                continue
            text = m.group(1).strip()
            if not text:
                continue

            # If the section is a numbered list, extract only the first item cleanly
            numbered = re.match(r"^(\d+\.?\s+)([\s\S]*?)(?=\n\d+\.|\Z)", text)
            if numbered:
                text = numbered.group(2).strip()

            # Truncate at sentence boundary within 300 chars
            if len(text) > 300:
                cut = text[:300]
                last_period = max(cut.rfind(". "), cut.rfind("。"))
                text = cut[:last_period + 1] if last_period > 100 else cut.rstrip() + "..."

            # Strip any trailing orphaned list markers
            text = re.sub(r"\n\d+\.\s*$", "", text).strip()
            return text
        return ""

    def _extract_connections(self, body):
        """Extracts wiki-link connections from Knowledge Graph & Connections section."""
        # Try the actual section header used in saved notes first, then fallback patterns
        section = re.search(
            r"#{2,3}\s+(?:🔗\s*)?(?:Knowledge Graph.*?Connections|Differential Analysis).*?\n([\s\S]*?)(?:\n#{2,3}\s|\n## |\Z)",
            body
        )
        if not section:
            return []
        text = section.group(1)
        links = re.findall(r"\[\[([^\]]+)\]\]", text)
        return list(dict.fromkeys(links))[:5]  # deduplicated, max 5

    def _theme_match(self, note, theme):
        content = f"{note['title']} {' '.join(note['tags'])} {note['body'][:1600]}"
        ncontent = self._normalize(content)
        tag_set = {self._normalize(t) for t in note["tags"]}
        for t in theme["tags"]:
            if self._normalize(t) in tag_set:
                return True
        for kw in theme["keywords"]:
            if self._normalize(kw) in ncontent:
                return True
        return False

    def _build_consensus_lines(self, matched_notes):
        """Build consensus from Core Contribution extraction of high-score notes."""
        top_notes = [n for n in matched_notes if n.get("score", 0) >= 8 and n.get("core_contribution")]
        if not top_notes:
            top_notes = [n for n in matched_notes if n.get("core_contribution")]
        lines = []
        for n in top_notes[:5]:
            contrib = n["core_contribution"].strip()
            if contrib:
                lines.append(f"- **[[{n['note_name']}]]**（Score {n['score']}/10）：{contrib}")
        return lines or ["- 暂无可提取的核心贡献，待深度分析笔记积累后自动汇总。"]

    def _build_conflict_lines(self, matched_notes):
        """Build conflict/limitation lines from Hidden Limitations extraction."""
        top_notes = [n for n in matched_notes if n.get("score", 0) >= 8 and n.get("limitations")]
        if not top_notes:
            top_notes = [n for n in matched_notes if n.get("limitations")]
        lines = []
        for n in top_notes[:5]:
            lim = n["limitations"].strip()
            if lim:
                lines.append(f"- **[[{n['note_name']}]]**：{lim}")
        return lines or ["- 暂未发现显式局限性记录，待深度分析笔记积累后自动汇总。"]

    def _build_connections_section(self, matched_notes):
        """Aggregates cross-paper connections from Differential Analysis sections."""
        conn_map = defaultdict(list)  # target_note -> [source_notes]
        for n in matched_notes:
            for target in n.get("connections", []):
                conn_map[target].append(n["note_name"])
        if not conn_map:
            return ""
        # Sort by how many notes reference the same target
        sorted_conns = sorted(conn_map.items(), key=lambda x: len(x[1]), reverse=True)
        lines = []
        for target, sources in sorted_conns[:8]:
            src_links = ", ".join([f"[[{s}]]" for s in sources[:3]])
            lines.append(f"- [[{target}]] ← 被 {src_links} 等 {len(sources)} 篇引用")
        return "\n".join(lines)

    def _render_template(self, theme, matched_notes, ai_enrichment):
        today = datetime.now().strftime("%Y-%m-%d")
        matched_notes = sorted(matched_notes, key=lambda x: x.get("score", 0), reverse=True)
        total = len(matched_notes)
        avg_score = round(sum([n.get("score", 0) for n in matched_notes]) / total, 2) if total else 0
        top = matched_notes[:12]
        tag_counter = Counter()
        for n in matched_notes:
            tag_counter.update([t for t in n.get("tags", []) if t != "paper"])
        hot_tags = [f"#{t}" for t, _ in tag_counter.most_common(10)]
        top_lines = "\n".join([
            f"- [[{n['note_name']}]] | Score: {n['score']}/10 | {n.get('pub','Unknown')[:10]} | {n['title']}"
            for n in top
        ]) or "- 暂无"

        # Recent: sort by pub date descending, fall back to score order for undated
        dated = sorted([n for n in matched_notes if n.get("pub") and n["pub"] != "Unknown"],
                       key=lambda x: x["pub"], reverse=True)
        undated = [n for n in matched_notes if not n.get("pub") or n["pub"] == "Unknown"]
        recent = (dated + undated)[:8]
        recent_lines = "\n".join([
            f"- [[{n['note_name']}]] | {n.get('pub','Unknown')[:10]} | {n['title']}"
            for n in recent
        ]) or "- 暂无"
        consensus_lines = "\n".join(self._build_consensus_lines(matched_notes))
        conflict_lines = "\n".join(self._build_conflict_lines(matched_notes))
        connections_section = self._build_connections_section(matched_notes)
        frontier_lines = "\n".join([f"- {x}" for x in ai_enrichment.get("frontier_signals", [])]) or "- 暂无"
        system_links_lines = "\n".join([f"- {x}" for x in ai_enrichment.get("systematic_links", [])]) or "- 暂无"
        weekly_actions_lines = "\n".join([f"- [ ] {x}" for x in ai_enrichment.get("weekly_actions", [])]) or "- [ ] 暂无"
        open_questions_lines = "\n".join([f"- {x}" for x in ai_enrichment.get("open_questions", [])]) or "- 暂无"
        mermaid = ai_enrichment.get("visual_map_mermaid", "").strip()
        mermaid_block = f"```mermaid\n{mermaid}\n```" if mermaid else "_暂无_"

        connections_block = f"\n## 🔀 跨论文引用网络\n{connections_section}\n" if connections_section else ""

        # Related themes from loaded relations
        related_ids = self.theme_relations.get(theme["id"], [])
        id_to_title = {t["id"]: t["title"] for t in self.theme_defs}
        if related_ids:
            related_lines = "\n".join(
                f"- [[{rid}|{id_to_title.get(rid, rid)}]]"
                for rid in related_ids
            )
        else:
            related_lines = "- 暂无预设关联主题"

        # Landmark works from AI enrichment
        landmark_lines = "\n".join(
            [f"- {x}" for x in ai_enrichment.get("landmark_works", [])]
        ) or "- 暂无"

        content = f"""---
theme_id: {theme['id']}
theme_title: "{theme['title']}"
parent_keyword: "{theme['parent']}"
updated_at: "{today}"
---

# 🧭 {theme['title']}（{theme['id']}）

## 🎯 主题定义
- 归属上位关键词：**{theme['parent']}**
- 细分关注：{', '.join(theme['keywords'])}
- 标准标签参考：{' '.join([f"#{t}" for t in theme['tags']])}

## 📊 主题仪表盘
- 总论文数：**{total}**
- 平均分：**{avg_score}**
- 高频标签：{' '.join(hot_tags) if hot_tags else '暂无'}

## 🆕 最近新增
{recent_lines}

## ⭐ 核心论文 Top
{top_lines}

## ✅ 核心贡献与共识
{consensus_lines}

## ⚠️ 局限性与关键分歧
{conflict_lines}
{connections_block}
## 🏛️ 领域里程碑工作（AI Enriched）
{landmark_lines}

## 🚀 前沿信号雷达（AI Enriched）
{frontier_lines}

## 🧬 体系化关联补充（AI Enriched）
{system_links_lines}

## ❓ 开放性问题（AI Enriched）
{open_questions_lines}

## 🗺️ 主题关系可视化（AI Enriched）
{mermaid_block}

## 🗓️ 本周推进建议（AI Enriched）
{weekly_actions_lines}

## 🔗 关联主题
{related_lines}
"""
        return content

    def _theme_file_path(self, theme):
        return os.path.join(self.themes_folder, f"{theme['id']}.md")

    def rebuild_theme_pages(self):
        """Full rebuild: re-parses all notes and regenerates all theme pages with AI enrichment."""
        notes = self._load_all_notes()
        theme_to_notes = self._assign_notes_to_themes(notes)
        for theme in self.theme_defs:
            matched = theme_to_notes.get(theme["id"], [])
            ai_enrichment = self._generate_ai_enrichment(theme, matched)
            content = self._render_template(theme, matched, ai_enrichment)
            with open(self._theme_file_path(theme), "w", encoding="utf-8") as f:
                f.write(content)
        self._write_theme_index()
        logger.info(f"Full theme rebuild complete: {self.themes_folder}")

    def _extract_existing_ai_sections(self, filepath):
        """Read existing theme page and extract AI-enriched section content to preserve it."""
        empty = {
            "landmark_works": [], "frontier_signals": [], "systematic_links": [],
            "open_questions": [], "visual_map_mermaid": "", "weekly_actions": [],
        }
        if not os.path.exists(filepath):
            return empty
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return empty

        def _extract_md_section(header_pattern, content):
            m = re.search(rf"## [^\n]*{re.escape(header_pattern)}[^\n]*\n([\s\S]*?)(?=\n## |\Z)", content)
            if not m:
                return ""
            return m.group(1).strip()

        def _lines_to_list(text):
            if not text or text in ("- 暂无", "- [ ] 暂无", "_暂无_"):
                return []
            return [ln.lstrip("- ").lstrip("[ ] ").strip() for ln in text.splitlines() if ln.strip() and ln.strip() not in ("- 暂无", "- [ ] 暂无")]

        landmark_raw = _extract_md_section("领域里程碑工作", content)
        frontier_raw = _extract_md_section("前沿信号雷达", content)
        links_raw    = _extract_md_section("体系化关联补充", content)
        questions_raw = _extract_md_section("开放性问题", content)
        weekly_raw   = _extract_md_section("本周推进建议", content)

        # Extract mermaid block
        mermaid = ""
        mm = re.search(r"## [^\n]*主题关系可视化[^\n]*\n```mermaid\n([\s\S]*?)```", content)
        if mm:
            mermaid = mm.group(1).strip()

        return {
            "landmark_works":   _lines_to_list(landmark_raw),
            "frontier_signals": _lines_to_list(frontier_raw),
            "systematic_links": _lines_to_list(links_raw),
            "open_questions":   _lines_to_list(questions_raw),
            "visual_map_mermaid": mermaid,
            "weekly_actions":   _lines_to_list(weekly_raw),
        }

    def _ai_enrichment_is_empty(self, ai_enrichment):
        """Returns True if all AI sections are empty/placeholder."""
        for key in ("landmark_works", "frontier_signals", "systematic_links",
                    "open_questions", "weekly_actions"):
            if ai_enrichment.get(key):
                return False
        if ai_enrichment.get("visual_map_mermaid"):
            return False
        return True

    def update_after_new_note(self, note_path):
        """
        Incremental update: only regenerates static sections for affected themes.
        Preserves existing AI-enriched sections — only regenerates them if they are empty.
        """
        if not note_path or not os.path.exists(note_path):
            logger.warning(f"update_after_new_note: path not found, falling back to full rebuild. ({note_path})")
            self.rebuild_theme_pages()
            return

        new_note = self._parse_note(note_path)
        if not new_note:
            logger.warning("update_after_new_note: could not parse note, falling back to full rebuild.")
            self.rebuild_theme_pages()
            return

        affected_themes = [t for t in self.theme_defs if self._theme_match(new_note, t)]
        if not affected_themes:
            logger.info(f"update_after_new_note: '{new_note['note_name']}' matched no themes, skipping.")
            return

        logger.info(
            f"update_after_new_note: '{new_note['note_name']}' matched "
            f"{len(affected_themes)} theme(s): {[t['id'] for t in affected_themes]}"
        )

        all_notes = self._load_all_notes()
        theme_to_notes = self._assign_notes_to_themes(all_notes)

        for theme in affected_themes:
            matched = theme_to_notes.get(theme["id"], [])
            theme_path = self._theme_file_path(theme)

            # Preserve existing AI sections; only regenerate if empty
            existing_ai = self._extract_existing_ai_sections(theme_path)
            if self._ai_enrichment_is_empty(existing_ai):
                logger.info(f"  [{theme['id']}] AI sections empty, regenerating...")
                ai_enrichment = self._generate_ai_enrichment(theme, matched)
            else:
                logger.info(f"  [{theme['id']}] Preserving existing AI sections.")
                ai_enrichment = existing_ai

            content = self._render_template(theme, matched, ai_enrichment)
            with open(theme_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"  Updated theme page: {theme['id']}")

        self._write_theme_index()
        logger.info(f"Incremental theme update complete ({len(affected_themes)} page(s) updated).")

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _load_all_notes(self):
        """Scans Research_Notes folder and returns list of parsed note dicts."""
        notes = []
        if os.path.exists(self.notes_folder):
            for fn in os.listdir(self.notes_folder):
                if fn.endswith(".md"):
                    parsed = self._parse_note(os.path.join(self.notes_folder, fn))
                    if parsed:
                        notes.append(parsed)
        return notes

    def _assign_notes_to_themes(self, notes):
        """Returns a dict mapping theme_id -> list of matching note dicts."""
        theme_to_notes = defaultdict(list)
        for note in notes:
            for theme in self.theme_defs:
                if self._theme_match(note, theme):
                    theme_to_notes[theme["id"]].append(note)
        return theme_to_notes

    def _write_theme_index(self):
        """Writes the Theme_Index.md file (no AI call)."""
        index_path = os.path.join(self.themes_folder, "Theme_Index.md")
        lines = [f"- [[{t['id']}]] | {t['title']} | Parent: {t['parent']}" for t in self.theme_defs]
        index_content = f"# 🗂️ Theme Index\n\n## 主题导航\n{os.linesep.join(lines)}\n"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
