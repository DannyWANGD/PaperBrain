# PaperBrain — 协作开发上下文

> 最后同步：2026-04-20 | 适用范围：`D:\PaperBrain` 全仓库

---

## 1. 项目目标

面向 Embodied AI / Robotics / VLA / World Model 方向，构建从"论文抓取 → 多阶段筛选 → 深度分析 → 主题聚合 → 播客生成"的自动化研究工作流，产物沉淀到本地 Obsidian Vault。

---

## 2. 架构速览

### 入口脚本

| 脚本 | 用途 |
|---|---|
| `script/main.py` | 主流程与调度 |
| `script/rebuild_theme_pages.py` | 主题母页全量重建（含 AI 增强） |
| `script/enrich_empty_themes.py` | 仅补全 AI 区块为空的主题页 |

### 核心模块（`script/src/`）

| 模块 | 职责 |
|---|---|
| `config_loader.py` | 配置加载与 `${ENV}` 变量替换 |
| `scraper.py` | arXiv + Hugging Face 论文抓取 |
| `analyser.py` | 粗筛 / 精筛 / 深度分析 / 图像提取 |
| `obsidian_writer.py` | 日报与单篇笔记写入，含 arXiv ID 去重 |
| `theme_manager.py` | 主题母页构建与增量更新 |
| `knowledge_base.py` | 轻量 RAG 检索 |
| `gardener.py` | 知识回链与链接整理 |
| `podcaster.py` | 播客文稿与音频生成 |

### 主链路

1. 读取 `config.yaml`
2. 抓取论文（批量按日期/分类，或单篇 `--arxiv-url`）
3. Stage-1 粗筛（`model_flash`，recall 导向）→ Stage-2 精筛（`model_screening_pro`，多维评分）
4. 深度分析候选：9/10 分全保留，8 分择优
5. 高价值论文：下载 PDF → RAG → 提图 → 多轮深度分析 → 写 Obsidian 笔记 → 增量更新主题页
6. 写日报 → 知识园丁 → 播客（可选）

### 评分权重（精筛）

| 维度 | 权重 |
|---|---|
| relevance | 0.30 |
| novelty | 0.23 |
| rigor | 0.22 |
| evidence | 0.15 |
| reproducibility | 0.10 |

含低相关 / 低证据 / 低 rigor 压分规则。

### Obsidian 目录约定

`Daily_Papers/` · `Research_Notes/` · `Research_Themes/` · `PDFs/` · `Assets/` · `Podcasts/`

---

## 3. 功能详解

### 论文抓取（`scraper.py`）
- 从 arXiv API 按关键词 + 分类（cs.RO / cs.AI / cs.LG / cs.CV）批量抓取论文
- 支持按目标日期过滤，默认抓取昨日新论文
- 从 Hugging Face Daily Papers 页面抓取当日精选论文
- 合并两个来源的结果，按标题去重
- 支持单篇模式：通过 arXiv URL 或 ID 直接抓取指定论文
- 所有请求内置指数退避重试（最多 4 次，基础等待 5s，最大 45s，含随机抖动）

### Stage-1 粗筛（`analyser.py` → `screen_papers`）
- 用 flash 轻量模型对所有抓取论文快速打分，以 recall 为导向（宁可多留不漏掉）
- 对每篇论文评估五个维度：相关性、新颖性、严谨性、证据充分性、可复现性
- 按加权公式计算综合分（权重见配置），低于阈值的论文直接淘汰
- 含低相关 / 低证据 / 低 rigor 的额外压分规则，防止偏科高分通过

### Stage-2 精筛（`analyser.py` → `screen_papers_second_stage`）
- 对粗筛通过的 top-K 篇论文用 pro 模型做精细评分
- 可选注入 PDF 摘录上下文（前 N 页，最多 5000 字符），提升 rigor/evidence 判断准确性
- 为每篇论文生成简短标题（`short_title`）和创新点摘要（`innovation_summary`）
- 输出最终排序结果，供深度分析阶段使用

### PDF 下载（`main.py` → `download_pdf`）
- 对精筛通过的论文自动下载 PDF 到本地 `PDFs/` 目录
- 支持多种 arXiv URL 格式（`/abs/`、`/pdf/`、`export.arxiv.org`）自动转换
- 内置 3 次重试，失败时尝试备用 URL 格式
- 含 URL scheme 安全校验，防止非法路径注入

### 深度分析（`analyser.py` → `analyze_paper`）
- 用 pro 模型对高价值论文（9/10 分全保留，8 分择优）做全面深度分析
- 从 PDF 提取正文文本（优先 PyMuPDF，失败自动 fallback 到 pypdf）
- 从 PDF 提取架构图等关键图像，编码为 base64 供视觉模型分析
- 结合 RAG 检索到的已有笔记上下文，生成有纵深的分析内容
- 输出中文分析正文 + 英文元数据（机构、GitHub 链接、项目主页、发表日期等）
- 解析模型输出时容忍脏 JSON，失败时返回结构化 fallback，不中断流程

### RAG 检索（`knowledge_base.py` → `retrieve_context`）
- 扫描 `Research_Notes/` 下所有已有笔记，提取标题与摘要
- 将笔记列表发给 flash 模型，由模型判断哪些笔记与当前论文相关
- 返回相关笔记的格式化上下文字符串，注入深度分析提示词
- 无需向量数据库，依赖长上下文模型直接做语义匹配

### Obsidian 笔记写入（`obsidian_writer.py`）
- 为每篇深度分析论文生成结构化 Markdown 笔记，写入 `Research_Notes/`
- 笔记包含 YAML frontmatter（标签、别名、arXiv URL、机构、GitHub 等元数据）
- 嵌入本地 PDF 链接和提取的架构图
- 按 arXiv ID 去重：若同一篇论文已有笔记则跳过，不重复写入
- 每日生成日报文件写入 `Daily_Papers/`，汇总当日所有通过筛选的论文列表
- 文件名自动清洗（去除非法字符，限制 100 字符长度）

### 主题系统（`theme_manager.py`）
- 维护 16 个核心研究主题（涵盖 Embodied AI、VLA、World Model、RL、Diffusion Policy 等）
- 每个主题定义关键词与正则规则，自动将新笔记归类到匹配主题
- 增量更新：新论文写入后只更新受影响的主题页，不全量重建
- 全量重建：手动触发 `rebuild_theme_pages.py`，重新生成所有主题母页
- 每个主题页由 AI 生成洞察摘要、趋势分析、研究方向建议（`theme_enrichment`）
- 生成 `Theme_Index.md` 导航页，含主题间关联关系
- AI 增强失败时优雅降级，保留已有内容不丢失

### 知识园丁（`gardener.py` → `prune_and_graft`）
- 从新论文的摘要和创新点中提取关键概念
- 在已有笔记的别名（aliases）中匹配相关概念
- 向匹配到的已有笔记追加反向链接（backlink），注明来源论文和创新点
- 防止重复添加同一链接
- 自动维护笔记间的知识图谱，无需手动整理

### 播客生成（`podcaster.py`）
- 用 pro 模型将论文分析内容改写为播客口播脚本
- 按目标时长计算字数（130–170 词/分钟），默认生成 5 分钟播客
- 清洗 Markdown 格式符号后，调用 edge-tts 合成语音（en-US-ChristopherNeural 男声）
- 输出 MP3 文件保存到 `Podcasts/` 目录
- 播客生成为可选步骤，可通过 `--no-podcast` 跳过

### 双供应商支持（`analyser.py` / `main.py`）
- 支持 `doubao`（豆包）和 `openrouter` 两个 AI 供应商，通过 `--provider` 参数切换
- 每个供应商独立配置 flash / screening_pro / pro 三档模型
- OpenRouter 调用失败（403/404/区域限制）时自动按候选模型链 fallback，不中断任务
- 所有 API Key 通过环境变量注入，不写死在代码中

---

## 4. 关键配置项

| 配置项 | 说明 |
|---|---|
| `analysis.screening_second_stage_use_pdf_context` | 精筛是否注入 PDF 摘录（默认 false） |
| `analysis.screening_second_stage_pdf_context_pages` | 摘录页数 |
| `analysis.screening_second_stage_pdf_context_max_chars` | 摘录截断字符数 |
| `analysis.threshold_score` | 精筛通过阈值 |
| `analysis.screening_second_stage_top_k` | 精筛候选数量 |

---

## 5. 代码规范

- 函数职责单一，命名语义化，避免过深嵌套。
- 统一用 `logger`，不在主流程散落 `print`。
- 阈值、开关、模型名放入 `config.yaml`，新增逻辑必须保留默认值与降级路径。
- API Key 仅通过环境变量注入，禁止写死。
- 路径操作兼容 Windows。

### 容错要求（必须遵守）

- 外部调用（arXiv / OpenRouter / 下载）必须可重试或可降级，禁止单点失败中断全流程。
- 解析模型输出必须容忍脏 JSON（先清洗再解析），失败时返回结构化 fallback payload。
- PDF 处理失败允许跳过单篇，保留总体任务继续执行。
- OpenRouter 模型不可用时按候选模型链自动 fallback。
- 任何新增异常分支都要带可定位日志（论文标题、阶段、原因）。

### 修改边界

- 优先修改：`script/` 下源码与配置。
- 禁止随意改动：历史知识产物（`Research_Notes/` 等）、`.env`、与本次任务无关的已有改动。
- 禁止：批量删除、强制覆盖、重置历史产物。

---

## 6. 常用命令

```bash
# 环境初始化
cd script && conda create -n wd python=3.10 -y && conda activate wd && pip install -r requirements.txt

# ── 主流程 ──────────────────────────────────────────────────────

# 立即执行主流程（默认分析昨日论文）
python main.py --run-now --provider openrouter

# 指定日期分析
python main.py --run-now --date 2026-03-20 --provider openrouter

# 单篇论文分析（通过 arXiv URL 或 ID）
python main.py --run-now --arxiv-url https://arxiv.org/abs/2503.10631 --provider openrouter
python main.py --run-now --arxiv-url 2503.10631 --provider openrouter

# 禁用播客生成
python main.py --run-now --provider openrouter --no-podcast

# 自定义播客时长（默认 5 分钟）
python main.py --run-now --provider openrouter --podcast-minutes 10

# 定时调度模式（每天 12:00 自动运行，不加 --run-now）
python main.py --provider openrouter

# ── 主题系统 ──────────────────────────────────────────────────────

# 全量重建所有主题母页（含 AI 增强）
python rebuild_theme_pages.py --provider openrouter

# 仅补全 AI 区块为空的主题页
python enrich_empty_themes.py --provider openrouter

# ── 播客生成 ──────────────────────────────────────────────────────

# 为指定笔记生成播客（笔记文件名不含 .md 后缀）
python generate_podcast.py "Paper_Title_Here" --provider openrouter --duration 8

# ── 配置编辑 ──────────────────────────────────────────────────────

# 编辑主题定义（增删主题、修改关键词）
notepad themes.yaml

# 编辑提示词（调整 AI 行为）
notepad prompts.yaml

# 编辑核心配置（模型、阈值、筛选参数）
notepad config.yaml
```

**参数说明**

- `--run-now`：立即执行，不加此参数则进入定时调度模式
- `--provider`：AI 供应商，`doubao`（豆包）或 `openrouter`
- `--date`：目标日期 `YYYY-MM-DD`，默认为昨日
- `--arxiv-url`：单篇模式，传入 arXiv URL 或 ID
- `--no-podcast`：跳过播客生成
- `--podcast-minutes`：播客时长（分钟），默认 5

**注意事项**

- 单篇模式（`--arxiv-url`）会跳过批量抓取，直接分析指定论文
- 定时调度模式下，程序会持续运行等待每日 12:00 触发（配置见 `config.yaml` 的 `schedule.time`）
- 主题页在每篇论文分析后自动增量更新，无需手动触发全量重建
- 全量重建主题页会重新生成所有 AI 增强内容，耗时较长且消耗 token

---

## 7. 常见报错

| 现象 | 原因 | 处理 |
|---|---|---|
| arXiv 429/503 | 限流 | 已内置指数退避；减少 `max_results`，错峰运行 |
| OpenRouter 403/404 | 模型不可用或区域限制 | 依赖 fallback 链；确认模型名与地区可用性 |
| 精筛 JSON 解析失败 | 模型输出非标准 JSON | `_sanitize_json` + fallback payload；收紧提示词 |
| PDF 文本为空/乱码 | `fitz` 抽取失败 | 自动 fallback `pypdf`；仍失败则跳过，仅用摘要 |
| 主题页 AI 区块为空 | 生成时截断或结构异常 | `python script/enrich_empty_themes.py --provider openrouter` |

---

## 8. 新对话确认清单

开始任务前优先确认：

1. 运行目标：全量日更 / 指定日期 / 单篇分析
2. 供应商与模型策略：`doubao` 或 `openrouter`
3. 成本偏好：是否开启二阶段 PDF 摘录
4. 输出偏好：是否生成播客、是否触发主题页全量重建
5. 阈值策略：`threshold_score` 与 `top_k` 是否调整

---

## 9. 变更日志

> 按时间倒序。每次阶段性改动后必须追加一条。

#### 2026-04-20（系统优化重构）
- 新增 `script/prompts.yaml`：所有 AI 提示词外置，按模块组织（screening / analysis / rag / podcast / theme_enrichment），代码中保留内联 fallback 保证向后兼容
- 新增 `script/themes.yaml`：16 个主题定义 + 关联关系外置，可直接编辑增删主题无需改代码
- 扩展 `script/src/config_loader.py`：新增 `load_prompts()` 和 `load_themes()` 函数
- 重构 `script/src/theme_manager.py`：
  - `__init__` 接收外部 themes/prompts 参数，fallback 到硬编码
  - AI 增强拆分为两批请求（batch1: landmark+frontier+links；batch2: questions+mermaid+actions），每批 max_tokens=3000，各自重试 2 次，互不影响
  - `update_after_new_note` 修复：增量更新只刷新静态区块，保留已有 AI 内容；仅当 AI 区块全空时才重新生成
  - 新增 `_extract_existing_ai_sections`、`_ai_enrichment_is_empty` 辅助方法
  - `_safe_json_load` 改进：分步骤解析并记录具体失败原因，清理尾部逗号
  - `_render_template` 改用 `self.theme_relations` 替代硬编码 `THEME_RELATIONS`
- 修复 `script/enrich_empty_themes.py`：检测范围从 4 个区块补全为 6 个，正则匹配放宽
- 重构 `script/src/analyser.py`：
  - `__init__` 接收 `prompts` 参数
  - 7 个提示词外置（coarse_screen、screen_paper、analyze_from_abstract、vision_select、round1、round2、vision_fallback）
  - `_sanitize_json` 重写：多步骤解析，非贪婪匹配，清理尾部逗号
  - 新增 `generate_paper_aliases()` 方法：用 flash 模型为每篇论文生成 5-10 个可搜索别名
- 重构 `script/src/knowledge_base.py`：接收 `prompts` 参数，外置 RAG 提示词，`scan_notes` 加目录存在性检查
- 重构 `script/src/podcaster.py`：接收 `prompts` 参数，外置播客提示词，`nest_asyncio.apply()` 包 try-except
- 重构 `script/src/gardener.py`：
  - 新增轻量词干化 `_stem()`（无新依赖）
  - 新增分层匹配 `_is_match()`：短别名过滤（<4字符）、单词词边界正则、多词 token overlap（≥70%）
- 扩展 `script/src/obsidian_writer.py`：frontmatter 写入 `arxiv_id` 字段和 `ai_aliases`（AI 生成别名）
- 更新 `script/main.py`：加载并传入 prompts/themes；深度分析后调用别名生成；精筛后清理 temp_pdfs 临时目录
- 更新 `script/rebuild_theme_pages.py` 和 `script/enrich_empty_themes.py`：传入 themes/prompts
- 清理 `script/config.yaml`：移除 `analysis.prompts` 大段提示词（已迁移到 prompts.yaml）
- 影响范围：全部核心模块
- 回滚：删除 prompts.yaml 和 themes.yaml 后所有模块自动 fallback 到内联默认值，不会崩溃
- 下一步：为筛选和深度分析增加最小回归测试；考虑 Methods/Results 定向 PDF 摘录

#### 2026-04-20（初始化）
- 新增根目录 `CLAUDE.md`，合并并规范化原 `script/CLAUDE.md` 内容。
- 新增第 3 节"功能详解"，以无序列表清单描述所有模块的具体行为。
- 二阶段精筛增强：支持可配置 PDF 摘录注入评分。
- 影响：`script/main.py`、`script/src/analyser.py`、`script/config.yaml`
- 回滚：将 `analysis.screening_second_stage_use_pdf_context` 设为 `false`
- 下一步：Methods/Results 定向抽取；增加精筛最小回归校验

#### 2026-03-29
- 阈值配置 provider 化、移除冗余全量重建、若干鲁棒性修复。
