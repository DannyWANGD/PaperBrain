# PaperBrain 🤖📄 - Automated Research Intelligence Hub

[中文说明](#paperbrain---自动化科研情报中枢) | [English](#english)

---

<a name="english"></a>
## 🇬🇧 English

**PaperBrain** is a fully automated research intelligence pipeline that turns daily paper streams into actionable research notes.  
In one run, it completes a full loop: **Fetch → Screen → Deep Analyze → Link to Your Knowledge Base → Notify/Podcast**.

*   **It Thinks**: Uses strong reasoning models for engineering-level analysis (method, math, evidence, limitations).
*   **It Remembers**: Uses **Context-Aware RAG** to compare new papers with your existing notes.
*   **It Speaks**: Generates a **~5-minute Deep Dive Podcast by default** (duration configurable via CLI).
*   **It Organizes**: Writes structured Markdown notes, metadata, and graph-ready links into **Obsidian**.

### 🚀 Core Features

*   **Intelligent Screening**: Fast first-pass scoring on large daily paper sets.
*   **Deep Analysis**: Detailed report for high-value papers (problem gap, method, formulas, evidence, critique).
*   **Context-Aware RAG**: Differential analysis against your prior notes.
*   **Strict Link Policy**: `[[Note]]` links are used **only** when a detailed note file exists; otherwise, it uses an ArXiv web link.
*   **Visual Extraction**: Automatic architecture figure extraction from PDFs.
*   **AI Podcast + Mobile Push**: Audio briefing generation and Bark notifications.

### 🏁 Getting Started (Zero to Hero)

#### Prerequisites
*   **OS**: Windows / macOS / Linux
*   **Python**: 3.10+ (Conda recommended)
*   **Obsidian**: For the best knowledge base experience.

#### Step 1: Installation
Clone the repository and set up the environment:

```bash
git clone https://github.com/YourUsername/PaperBrain.git
cd PaperBrain/script

# Create Conda environment
conda create -n wd python=3.10
conda activate wd

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: API Configuration
PaperBrain uses **OpenRouter** (recommended) or Doubao for LLM inference.

1.  Copy the example env file:
    ```bash
    cp .env.example .env
    ```
2.  Edit `.env` and fill in your keys:
    ```ini
    # Recommended: Use OpenRouter for access to Claude 3.7 / Gemini Pro
    OPENROUTER_API_KEY=sk-or-v1-your-key-here
    
    # Optional: For Bark Mobile Notifications (iOS)
    BARK_URL=https://api.day.app/your-token/
    ```

#### Step 3: Customize Your Research Interests
Edit `config.yaml` to define what you care about:

```yaml
search:
  keywords:
    - "World Model"
    - "Embodied AI"
    - "Humanoid Robot"
  arxiv_categories:
    - "cs.RO"
    - "cs.AI"
```

#### Step 4: Run It!

**Option A: Run Immediately (Manual Mode)**
```bash
# Default: Generates Podcast (~5 minutes)
python main.py --run-now --provider openrouter

# Skip Podcast (faster)
python main.py --run-now --provider openrouter --no-podcast

# Custom podcast duration (e.g., 10 minutes)
python main.py --run-now --provider openrouter --podcast-minutes 10
```

**Option B: Generate Podcast for Existing Note**
```bash
# Great for revisiting old papers!
python generate_podcast.py "Solaris.md" --provider openrouter

# Custom duration for single-note podcast
python generate_podcast.py "Solaris.md" --provider openrouter --minutes 12
```

**Option C: Auto-Schedule (Windows)**
Use **Task Scheduler** to run `script/run_daily.bat` every morning at 8:00 AM.
*   *Action*: Start a program
*   *Program*: `D:\PaperBrain\script\run_daily.bat`
*   *Start in*: `D:\PaperBrain\script\` (Crucial!)

### 🔒 Privacy & Security

This tool processes data locally and interacts with third-party AI services.
*   **API Keys**: Stored in `.env` (git-ignored). Never shared.
*   **Data Transmission**: Paper content is sent to ArXiv (search), Hugging Face (metadata), OpenAI/Anthropic (analysis), and Microsoft (TTS).
*   **See [SECURITY.md](SECURITY.md)** for full details.

---

<a name="paperbrain---自动化科研情报中枢"></a>
## 🇨🇳 PaperBrain - 自动化科研情报中枢

**PaperBrain** 不只是“论文抓取器”，而是一个完整的**自动化科研工作流引擎**。  
一次运行会自动完成：**抓取 → 筛选 → 深度分析 → 知识库关联 → 推送/播客**。

它每天自动从 ArXiv 和 Hugging Face 抓取最新论文，利用 **快慢思考 (System 1 & 2)** 架构进行筛选和深度解读，并将结构化的知识（公式、图谱、代码审计）同步到您的 **Obsidian** 知识库中。

### ✨ 核心亮点（清晰版）

1.  **智能筛选 + 深度分析双层架构**：
    *   第一层：快速筛选大批论文，给出相关性评分。
    *   第二层：只对高价值论文生成深度报告，重点输出方法、公式、实验和局限。

2.  **上下文感知 RAG 差异化分析**：
    *   新论文分析前，先检索您已有笔记。
    *   报告会明确写出“与既有工作相比，哪里变好、哪里仍不足”。

3.  **严格链接策略（避免误跳转）**：
    *   只有真正生成了深度笔记的论文，才使用 `[[内联链接]]`。
    *   未生成深度笔记的论文，一律使用 ArXiv 网页链接。

4.  **AI 播客与移动推送**：
    *   默认生成约 5 分钟英文深度播客（可通过命令行参数调整时长）；
    *   通过 Bark 推送摘要和播客就绪提醒。

### 🏁 快速上手指南

#### 准备工作
*   推荐安装 **Anaconda** 或 Miniconda。
*   推荐使用 **Obsidian** 作为知识库前端。

#### 第一步：安装项目
```bash
# 1. 克隆代码
git clone https://github.com/YourUsername/PaperBrain.git
cd PaperBrain/script

# 2. 创建环境
conda create -n wd python=3.10
conda activate wd

# 3. 安装依赖 (包含 PyTorch, Edge-TTS 等)
pip install -r requirements.txt
```

#### 第二步：配置密钥
为了保护隐私，我们使用 `.env` 文件存储密钥。

1.  复制模板：
    ```bash
    cp .env.example .env
    ```
2.  编辑 `.env` 文件（使用记事本或 VS Code）：
    ```ini
    # 推荐使用 OpenRouter (可访问 Claude 3.7, Gemini Pro 等 SOTA 模型)
    OPENROUTER_API_KEY=sk-or-v1-your-key-here
    
    # 选填：Bark 推送链接 (iOS App Store 下载 Bark)
    BARK_URL=https://api.day.app/your-token/
    ```

#### 第三步：定义研究方向
打开 `config.yaml`，修改您的关注领域：

```yaml
search:
  keywords:
    - "World Model"
    - "Embodied AI"
    - "Humanoid Robot"
  arxiv_categories:
    - "cs.RO"  # 机器人
    - "cs.CV"  # 计算机视觉
```

#### 第四步：运行！

**方式一：立即运行 (手动)**
```bash
# 默认模式：包含播客生成（默认约 5 分钟）
python main.py --run-now --provider openrouter

# 纯文本模式：不生成播客 (速度更快)
python main.py --run-now --provider openrouter --no-podcast

# 自定义播客时长（示例：10分钟）
python main.py --run-now --provider openrouter --podcast-minutes 10
```

**方式二：为特定笔记生成播客**
想听听以前读过的某篇论文？
```bash
python generate_podcast.py "Solaris.md" --provider openrouter

# 自定义该篇播客时长（示例：12分钟）
python generate_podcast.py "Solaris.md" --provider openrouter --minutes 12
```

**方式三：每日自动运行 (Windows)**
使用 Windows 自带的 **任务计划程序 (Task Scheduler)**：
1.  创建基本任务 -> 每天上午 8:00。
2.  操作：启动程序 -> 选择 `D:\PaperBrain\script\run_daily.bat`。
3.  **关键点**：在“起始于 (Start in)”一栏中，**必须**填入脚本所在目录 `D:\PaperBrain\script\`，否则会报错。

### 🔒 隐私与安全

本项目注重您的数据隐私与密钥安全。
*   **API 密钥**：仅存储在本地 `.env` 文件中（默认被 git 忽略），绝不上传。
*   **数据传输**：论文内容仅发送至 ArXiv (搜索)、Hugging Face (元数据)、OpenAI/Anthropic (分析) 及 Microsoft (语音合成) 用于生成报告。
*   **详见 [SECURITY.md](SECURITY.md)** 了解完整安全策略。

---
*Powered by PaperBrain Team & LLMs*
