<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white" />
  <img src="https://img.shields.io/badge/LLM-OpenRouter%20%7C%20Doubao-FF6600" />
  <img src="https://img.shields.io/badge/Workflow-Auto%20Research-00A86B" />
</p>

# PaperBrain

> From paper stream to knowledge graph.  
> 自动抓取、分层筛选、深度分析、主题聚合、播客生成，一站式沉淀到 Obsidian。

<p align="center">
  <img src="./paperbrain_arch.png" alt="PaperBrain Architecture" width="900" />
</p>

## 为什么是 PaperBrain
- 面向 Embodied AI / Robotics / VLA / World Model 的研究自动化流水线。
- 两阶段筛选控制成本：`model_flash` 粗筛，`model_screening_pro` 精筛。
- 深度分析整合 PDF 文本、关键图像、历史笔记 RAG，输出可直接学习的技术报告。
- 自动维护 Obsidian 知识库：日报、单篇笔记、主题页、回链、播客音频。

## 功能介绍

### 1) 智能抓取与去重
- 支持 arXiv 与 Hugging Face Daily Papers 双源抓取，可按日期批量运行，也可单篇 `--arxiv-url` 精准分析。
- 抓取阶段自动做关键词过滤与标题去重，减少无关论文和重复条目。
- 网络请求内置重试与退避策略，降低限流/抖动带来的任务失败概率。

### 2) 两阶段论文筛选
- Stage-1 粗筛聚焦召回，快速筛出可能高价值论文，控制总体调用成本。
- Stage-2 精筛做多维评分（relevance/novelty/rigor/evidence/reproducibility），形成更稳定的优先级排序。
- 二阶段支持可配置 PDF 摘录注入（前 N 页 + 字符上限），避免只看摘要造成误判。

### 3) 深度分析引擎
- 自动下载 PDF，提取关键架构图，并结合历史笔记做 RAG 上下文增强。
- 支持多轮分析生成“可学习型”报告，覆盖方法、公式、实验、局限与后续研究方向。
- 具备视觉 fallback 路径：文本抽取失败时可回退到图像阅读流程。

### 4) 知识库自动化沉淀
- 自动生成 `Research_Notes` 单篇笔记与 `Daily_Papers` 日报，并维护 frontmatter 元数据。
- 主题页增量更新：新笔记写入后自动刷新相关 `Research_Themes`，无需每次全量重建。
- 知识园丁会尝试为已有笔记追加 related work 回链，持续增强笔记间连接密度。

### 5) 可配置提示词与主题系统
- 筛选、分析、主题增强提示词统一在 `script/prompts.yaml` 管理，便于快速实验和版本演进。
- 主题树定义位于 `script/themes.yaml`，支持按研究方向扩展或重构主题体系。
- 标签体系由 `script/tags.yaml` 管理，利于后续统计、检索与主题归档。

### 6) 播客与传播能力
- 自动为高分论文生成播客文稿与音频，降低信息消费门槛。
- 支持对指定笔记单独生成播客，适合对外分享和团队同步。

## 核心流程

```text
arXiv + HuggingFace Daily Papers
        │
        ▼
Stage-1 Coarse Screening (model_flash)
        │
        ▼
Stage-2 Rigorous Screening (model_screening_pro)
  └─ 可选注入 PDF 前几页文本作为额外证据
        │
        ▼
Deep Analysis (model_pro)
  └─ PDF文本 + 架构图 + RAG上下文 + 多轮分析
        │
        ▼
Obsidian Outputs
  ├─ Research_Notes
  ├─ Research_Themes (增量更新)
  ├─ Daily_Papers
  ├─ Assets / PDFs
  └─ Podcasts
```

## 项目结构

```text
PaperBrain/
├── Daily_Papers/                  # 每日摘要
├── Research_Notes/                # 单篇深度笔记
├── Research_Themes/               # 主题母页 + Theme_Index
├── PDFs/                          # 下载的论文 PDF
├── Assets/                        # 提取的架构图
├── Podcasts/                      # 生成的播客音频
├── script/
│   ├── main.py                    # 主流程入口
│   ├── rebuild_theme_pages.py     # 全量重建主题页
│   ├── enrich_empty_themes.py     # 仅补齐空 AI 区块
│   ├── generate_podcast.py        # 指定笔记生成播客
│   ├── config.yaml                # 运行配置
│   ├── prompts.yaml               # 全量提示词配置
│   ├── themes.yaml                # 主题定义配置
│   ├── tags.yaml                  # 标准标签体系
│   └── src/
│       ├── scraper.py
│       ├── analyser.py
│       ├── knowledge_base.py
│       ├── obsidian_writer.py
│       ├── theme_manager.py
│       ├── gardener.py
│       ├── podcaster.py
│       └── config_loader.py
├── CLAUDE.md                      # 协作文档与变更日志
└── README.md
```

## 快速开始

### 1) 安装环境

```bash
cd script
conda create -n wd python=3.10 -y
conda activate wd
pip install -r requirements.txt
```

### 2) 配置密钥

复制并填写环境变量：

```bash
copy .env.example .env
```

`script/.env` 至少包含：

```env
DOUBAO_API_KEY=your_key
OPENROUTER_API_KEY=your_key
# 可选：BARK_URL=...
```

### 3) 运行主流程

从仓库根目录执行：

```bash
# 立即执行（默认抓取昨天）
python script/main.py --run-now --provider openrouter

# 指定日期
python script/main.py --run-now --date 2026-03-20 --provider openrouter

# 单篇论文模式（URL 或 arXiv ID）
python script/main.py --run-now --provider openrouter --arxiv-url https://arxiv.org/abs/2603.19199
```

## 配置说明（重点）

- `script/config.yaml`
  - 模型与阈值：`doubao.*` / `openrouter.*`
  - 筛选策略：`analysis.screening_second_stage_top_k`
  - 二阶段 PDF 证据注入：
    - `analysis.screening_second_stage_use_pdf_context`
    - `analysis.screening_second_stage_pdf_context_pages`
    - `analysis.screening_second_stage_pdf_context_max_chars`
  - 输出目录：`obsidian.*`
- `script/prompts.yaml`
  - 粗筛、精筛、深度分析、别名生成等提示词统一管理。
- `script/themes.yaml`
  - 主题树定义（可直接扩展和重命名）。

## 常用命令

```bash
# 全量重建主题母页
python script/rebuild_theme_pages.py --provider openrouter

# 仅补全空 AI 区块
python script/enrich_empty_themes.py --provider openrouter

# 对指定笔记生成播客
python script/generate_podcast.py "FASTER.md" --provider openrouter --minutes 6
```

## 输出产物

- `Research_Notes/*.md`：单篇技术深析（含摘要、方法拆解、证据、批判评估）。
- `Research_Themes/*.md`：主题聚合页（增量更新）。
- `Daily_Papers/*.md`：每日筛选摘要。
- `Assets/*_arch.(png|jpeg)`：论文架构图。
- `Podcasts/*.mp3`：Top 论文播客。

## 稳定性与容错

- arXiv 限流（429/503）内置指数退避。
- OpenRouter 模型不可用（403/404/地区限制）自动 fallback。
- JSON 脏输出有清洗与降级 payload。
- PDF 文本抽取失败自动 fallback 到备用解析路径。

## 安全

- API Key 仅本地 `.env` 使用，不入库。
- 所有输出默认落地到本地 Obsidian Vault。
- 详细策略见 [SECURITY.md](SECURITY.md)。

## 协作开发

- 项目上下文、约束和变更历史见 [CLAUDE.md](./CLAUDE.md)。
- 欢迎提交 Issue / PR，一起把研究工作流做成真正可复用的开源工具链。
