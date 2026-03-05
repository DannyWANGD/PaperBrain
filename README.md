# PaperBrain 🤖📄 - Automated Research Intelligence Hub

[中文说明](#paperbrain---自动化科研情报中枢) | [English](#english)

---

<a name="english"></a>
## 🇬🇧 English

**PaperBrain** is an automated research pipeline that transforms the way you consume academic literature. It daily fetches the latest papers from **ArXiv** and **Hugging Face**, uses **LLMs (Claude/Gemini/Doubao)** for intelligent screening and deep analysis, and seamlessly syncs structured knowledge to your **Obsidian** vault.

Now featuring **Context-Aware RAG** and **AI Podcasts**!

### 🚀 Core Features

*   **Intelligent Screening**: Automatically filters hundreds of daily papers using a fast LLM (Gemini Flash), scoring them based on your research interests.
*   **Deep Analysis**: For high-scoring papers, performs a rigorous, engineering-centric analysis (Methodology, Math, Architecture) using SOTA models (Claude 3.7 Sonnet).
*   **Visual Extraction**: Automatically extracts architecture diagrams from PDFs.
*   **Context-Aware RAG**: Before analyzing a new paper, it retrieves relevant notes from your existing knowledge base to provide **differential analysis** (e.g., "Unlike your previous note on X, this paper uses Y...").
*   **AI Podcast**: Generates a 10-minute "Deep Dive" audio briefing (Lex Fridman style) for the day's top paper, pushed to your phone.
*   **Obsidian Integration**: Auto-generates Markdown notes with Frontmatter, Mermaid graphs, and backlinks.
*   **Mobile Notifications**: Pushes summaries and podcast links via **Bark**.

### 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/PaperBrain.git
    cd PaperBrain/script
    ```

2.  **Install Dependencies**
    ```bash
    conda create -n wd python=3.10
    conda activate wd
    pip install -r requirements.txt
    ```

3.  **Configuration (.env)**
    Copy the example env file and fill in your API keys:
    ```bash
    cp .env.example .env
    ```
    Edit `.env`:
    ```ini
    DOUBAO_API_KEY=your_key
    OPENROUTER_API_KEY=your_key
    BARK_URL=your_bark_url
    ```

4.  **Customize Config**
    Edit `config.yaml` to set your **Research Keywords** and **ArXiv Categories**.

### 🖥️ Usage

*   **Run Immediately (Manual)**:
    ```bash
    python main.py --run-now --provider openrouter
    ```

*   **Generate Podcast for a Specific Note**:
    ```bash
    python generate_podcast.py "Solaris.md" --provider openrouter
    ```

*   **Auto-Schedule**:
    Use Windows Task Scheduler to run `script/run_daily.bat` every morning at 8:00 AM.

---

<a name="paperbrain---自动化科研情报中枢"></a>
## 🇨🇳 PaperBrain - 自动化科研情报中枢

**PaperBrain** 是一个专为研究人员设计的全自动科研情报系统。它每天自动从 ArXiv 和 Hugging Face 抓取最新论文，利用大模型进行智能筛选和深度解读，并将结构化的知识同步到您的 **Obsidian** 知识库中。

新增 **上下文感知 (RAG)** 与 **AI 播客生成** 功能！

### 🚀 核心功能

*   **智能筛选**: 使用轻量级模型 (Gemini Flash) 快速扫描数百篇论文摘要，根据您的研究兴趣打分（1-10分）。
*   **深度分析**: 对高分论文使用 SOTA 模型 (Claude 3.7 Sonnet) 进行工程化深读，提取数学公式、创新点和系统架构。
*   **视觉提取**: 自动从 PDF 中提取架构图和关键图表。
*   **上下文感知 (RAG)**: 在分析新论文前，自动检索您知识库中的旧笔记，进行**差异化对比分析**（例如：“这篇论文的方法解决了你之前记录的 [Note A] 中的梯度消失问题”）。
*   **AI 播客**: 为当天最重要的论文生成一段 10 分钟的深度解读音频（类似 NotebookLM），风格自然幽默，支持手机端收听。
*   **Obsidian 深度集成**: 自动生成包含元数据、Mermaid 知识图谱和双向链接的 Markdown 笔记。
*   **移动端通知**: 通过 **Bark** 推送每日日报和播客音频。

### 🛠️ 安装指南

1.  **克隆项目**
    ```bash
    git clone https://github.com/YourUsername/PaperBrain.git
    cd PaperBrain/script
    ```

2.  **安装依赖**
    ```bash
    conda create -n wd python=3.10
    conda activate wd
    pip install -r requirements.txt
    ```

3.  **配置密钥 (.env)**
    复制示例环境文件并填入 API Key：
    ```bash
    cp .env.example .env
    ```
    编辑 `.env` 文件：
    ```ini
    DOUBAO_API_KEY=your_key_here      # 豆包 API Key
    OPENROUTER_API_KEY=your_key_here  # OpenRouter API Key (推荐使用)
    BARK_URL=your_bark_url            # Bark 推送链接
    ```

4.  **个性化配置**
    编辑 `config.yaml`，修改 `keywords`（研究关键词）和 `arxiv_categories`（关注的 ArXiv 分区）。

### 🖥️ 使用方法

*   **立即运行 (手动模式)**:
    ```bash
    python main.py --run-now --provider openrouter
    ```

*   **为特定笔记生成播客**:
    ```bash
    python generate_podcast.py "Solaris.md" --provider openrouter
    ```
    *(注：文件名需为 Research_Notes 目录下的现有笔记)*

*   **每日自动运行**:
    使用 Windows 任务计划程序，设置每天早上 8:00 运行 `script/run_daily.bat`。

### 📂 目录结构

```text
PaperBrain/
├── README.md                # 项目文档
├── script/                  # 核心代码
│   ├── .env                 # [机密] API 密钥配置 (不要提交到 GitHub)
│   ├── config.yaml          # 通用配置 (路径、关键词、Prompt)
│   ├── main.py              # 主程序入口
│   ├── generate_podcast.py  # 独立播客生成工具
│   ├── run_daily.bat        # Windows 批处理启动脚本
│   ├── src/                 # 源代码模块
│   │   ├── scraper.py       # 论文抓取
│   │   ├── analyser.py      # AI 分析核心 (Screening & Deep Analysis)
│   │   ├── knowledge_base.py# RAG 检索模块
│   │   ├── podcaster.py     # 播客生成模块 (TTS)
│   │   ├── obsidian_writer.py # Markdown 写入与文件管理
│   │   └── ...
└── ...
```

---
*Powered by PaperBrain Team & LLMs*
