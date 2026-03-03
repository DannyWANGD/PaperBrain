![[Pasted image 20260303220047.png]]
![[Pasted image 20260303220453.png]]
![[Pasted image 20260303220300.png]]
![[Pasted image 20260303220437.png]]
# PaperBrain 🤖📄 - Your Automated Research Intelligence Hub

PaperBrain is an automated paper analysis pipeline designed for researchers. It daily fetches the latest cutting-edge papers from arXiv and Hugging Face Daily Papers, uses the **Doubao Large Model (Doubao Pro/Lite)** for intelligent screening and deep interpretation, and seamlessly syncs the results to your **Obsidian** knowledge base.

Now featuring a **Visual Dashboard**, **Mobile Notifications**, and **Knowledge Gardening** capabilities!

## 🚀 Core Features

*   **Multi-source Automatic Fetching**:
    *   **ArXiv**: Precise date-based retrieval for configured categories (e.g., `cs.RO`, `cs.AI`) and keywords.
    *   **Hugging Face Daily Papers**: Captures community trending papers for the specified date.
*   **Intelligent Screening (Lite Model)**:
    *   Uses a lightweight model to quickly score massive paper abstracts (1-10 scale).
    *   Filters out irrelevant content based on your research interests (Keywords).
    *   **Auto-Tagging**: Automatically assigns standardized tags based on a taxonomy (e.g., `#World_Model`, `#Sim2Real`).
*   **Deep Visual Analysis (Pro Model)**:
    *   **Visual Enhancement**: Automatically extracts Architecture Diagrams or flowcharts from PDF papers.
    *   **Deep Interpretation**: Generates a comprehensive deep report including innovations, limitations, methodology, and mathematical formulas.
    *   **Metadata Extraction**: Automatically extracts key information such as publishing institutions, GitHub links, project homepages, etc.
*   **Knowledge Gardening 🌱**:
    *   **Auto-Backlinking**: When a new paper is analyzed, PaperBrain automatically scans your existing notes and appends backlinks to old notes that are conceptually related (e.g., "New paper X discusses Y which is relevant to this note").
    *   **Taxonomy Management**: Uses a `tags.yaml` file to ensure tag consistency across your vault.
*   **Deep Obsidian Integration**:
    *   **Dashboard**: A `Dashboard.md` featuring DataviewJS visualizations (Trends, Charts, Progress Bars).
    *   **Daily Digest**: Generates a daily brief summarizing all relevant papers of the day.
    *   **Research Notes**: Generates independent Markdown notes for each intensively read paper, containing complete metadata (Frontmatter) and Mermaid knowledge graphs.
*   **Mobile Notifications (Bark)**:
    *   Push daily summaries of high-value papers directly to your iPhone via the **Bark** app.

## 📂 Directory Structure

```text
d:\PaperBrain\
├── README.md                # Project Documentation
├── Dashboard.md             # [New] Visual Research Dashboard
├── script/                  # Core Codebase
│   ├── config.yaml          # Configuration (API Key, Paths, Keywords, Bark URL)
│   ├── tags.yaml            # [New] Tag Taxonomy Definition
│   ├── main.py              # Main Orchestrator
│   ├── run_daily.bat        # Windows Batch Runner
│   ├── requirements.txt     # Dependencies
│   └── src/                 # Source Modules (scraper, analyser, gardener, notifier...)
├── Daily_Papers/            # [Auto-generated] Daily Paper Digests
├── Research_Notes/          # [Auto-generated] Deep Analysis Notes
├── PDFs/                    # [Auto-generated] Paper PDF Archives
└── Assets/                  # [Auto-generated] Extracted Architecture Images
```

## 🛠️ Installation & Configuration

### 1. Environment Setup
Ensure Python 3.8+ and Conda are installed.

```bash
cd script
conda create -n wd python=3.10
conda activate wd
pip install -r requirements.txt
```

### 2. Configuration (`config.yaml`)
Find `config.yaml` in the `script` directory and modify the following key configurations:

```yaml
doubao:
  api_key: "YOUR_DOUBAO_API_KEY"  # Required
  model_flash: "ep-..."           # Lite Model Endpoint ID (for screening)
  model_pro: "ep-..."             # Pro Model Endpoint ID (for deep analysis)
  threshold_score: 7              # Minimum score to trigger deep analysis

obsidian:
  vault_path: "../"               # Obsidian Vault Root
  daily_digest_folder: "Daily_Papers"
  detailed_notes_folder: "Research_Notes"

notification:
  enabled: true
  bark_url: "https://api.day.app/YOUR_KEY/" # iOS Bark Notification URL

search:
  keywords:                       # Customize your research interests
    - "World Model"
    - "Embodied AI"
    - "Robot Manipulation"
  arxiv_categories:               # ArXiv Categories to watch
    - "cs.RO"
    - "cs.AI"
```

### 3. Taxonomy (`tags.yaml`)
Define your standard tags in `script/tags.yaml` to keep your knowledge graph clean:

```yaml
taxonomy:
  - name: "World_Model"
    aliases: ["World Models", "Predictive Model"]
    description: "Models that predict future states..."
```

## 🖥️ Usage

### Method 1: Run for a Specific Date (Manual Mode)
Ideal for backfilling or checking specific days.

```bash
cd script
# Run for yesterday (default)
python main.py --run-now

# Run for a specific date
python main.py --run-now --date 2024-02-26
```

### Method 2: Daily Scheduler (Daemon)
The program will run continuously and automatically execute tasks at a specified time (default 12:00) every day.

```bash
cd script
python main.py
```

### Method 3: Windows Batch Script
Simply double-click `script/run_daily.bat`. It handles Conda activation and execution automatically.

## 📝 Output Note Standard

Generated Obsidian notes will contain rich metadata (Frontmatter), facilitating retrieval using the Dataview plugin:

```yaml
---
tags:
  - paper
  - Robot_Manipulation
  - World_Model
aliases:
  - "Solaris"
  - "Solaris: Building a Multiplayer Video World Model in Minecraft"
url: http://arxiv.org/abs/2602.xxxxx
pdf_url: http://arxiv.org/pdf/2602.xxxxx
local_pdf: "[[Solaris.pdf]]"
github: "https://github.com/..."
institutions:
  - "University of Toronto"
  - "NVIDIA"
publication_date: "2024-02-26"
score: 9
---
```

## 🧠 Advanced Features

*   **Dashboard.md**: A control center for your research. Requires **Dataview** plugin (Enable "Enable JavaScript Queries" in settings).
*   **Smart Retry**: Automatically attempts multiple mirrors (arxiv.org, export.arxiv.org) when downloading PDFs.
*   **Architecture Diagram Extraction**: Uses multimodal vision capabilities to automatically identify and capture the core system architecture diagram.

---
*Powered by Doubao & PaperBrain Team*
