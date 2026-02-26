# PaperBrain 🤖📄 - Your Automated Research Intelligence Hub

PaperBrain is an automated paper analysis pipeline designed for researchers. It daily fetches the latest cutting-edge papers from arXiv and Hugging Face Daily Papers, uses the Doubao Large Model (Doubao Pro/Lite) for intelligent screening and deep interpretation, and seamlessly syncs the results to your Obsidian knowledge base.

## 🚀 Core Features

*   **Multi-source Automatic Fetching**:
    *   **ArXiv**: Real-time retrieval based on configured categories (e.g., cs.RO, cs.AI) and keywords.
    *   **Hugging Face Daily Papers**: Captures community trending papers.
*   **Intelligent Screening (Lite Model)**:
    *   Uses a lightweight model to quickly score massive paper abstracts (1-10 scale).
    *   Filters out irrelevant content based on your research interests (Keywords).
*   **Deep Visual Analysis (Pro Model)**:
    *   Automatically downloads PDFs for high-scoring papers (default >5).
    *   **Visual Enhancement**: Automatically extracts Architecture Diagrams or flowcharts from papers.
    *   **Deep Interpretation**: Generates a comprehensive deep report including innovations, limitations, methodology, and mathematical formulas.
    *   **Metadata Extraction**: Automatically extracts key information such as publishing institutions, GitHub links, project homepages, etc.
*   **Deep Obsidian Integration**:
    *   **Daily Digest**: Generates a daily brief summarizing all relevant papers of the day.
    *   **Research Notes**: Generates independent Markdown notes for each intensively read paper, containing complete metadata (Frontmatter).
    *   **Local PDF Management**: Automatically renames and archives PDF files to a specified directory.

## 📂 Directory Structure

```text
d:\PaperBrain\
├── README.md                # Project Documentation
├── script/                  # Core Codebase
│   ├── config.yaml          # Configuration (API Key, Paths, Keywords)
│   ├── main.py              # Main Entry Point
│   ├── requirements.txt     # Dependencies
│   └── src/                 # Source Modules
├── Daily_Papers/            # [Auto-generated] Daily Paper Digests
├── Research_Notes/          # [Auto-generated] Deep Analysis Notes
├── PDFs/                    # [Auto-generated] Paper PDF Archives
└── Assets/                  # [Auto-generated] Extracted Architecture Images
```

## 🛠️ Installation & Configuration

### 1. Environment Setup
Ensure Python 3.8+ is installed.

```bash
cd script
pip install -r requirements.txt
```

### 2. Configuration (`config.yaml`)
Find `config.yaml` in the `script` directory and modify the following key configurations:

```yaml
doubao:
  api_key: "YOUR_DOUBAO_API_KEY"  # Required
  model_flash: "ep-..."           # Lite Model Endpoint ID (for screening)
  model_pro: "ep-..."             # Pro Model Endpoint ID (for deep analysis)
  threshold_score: 5              # Minimum score to trigger deep analysis

obsidian:
  vault_path: "../"               # Obsidian Vault Root (relative to script path)
  daily_digest_folder: "Daily_Papers"
  detailed_notes_folder: "Research_Notes"
  pdf_storage_folder: "PDFs"

search:
  keywords:                       # Customize your research interests
    - "World Model"
    - "Embodied AI"
    - "Robot Manipulation"
  arxiv_categories:               # ArXiv Categories to watch
    - "cs.RO"
    - "cs.AI"
```

## 🖥️ Usage

### Method 1: Run Immediately (Manual Mode)
If you want to fetch and analyze today's papers immediately:

```bash
cd script
python main.py --run-now
```

### Method 2: Background Daemon (Auto-Schedule)
The program will run continuously and automatically execute tasks at a specified time (default 12:00) every day:

```bash
cd script
python main.py
```

## 📝 Output Note Standard

Generated Obsidian notes will contain rich metadata (Frontmatter), facilitating retrieval using the Dataview plugin:

```yaml
---
tags:
  - paper
  - Robot-Manipulation
  - World-Model
  - 2024-02-26
aliases:
  - "Solaris: Building a Multiplayer Video World Model in Minecraft"
url: http://arxiv.org/abs/2602.xxxxx
pdf_url: http://arxiv.org/pdf/2602.xxxxx
local_pdf: "[[Solaris Building a Multiplayer Video World Model in Minecraft.pdf]]"
github: "https://github.com/..."
project_page: "https://..."
institutions:
  - "University of Toronto"
  - "NVIDIA"
publication_date: "2024-02-26"
---
```

## 🧠 Advanced Features

*   **Architecture Diagram Extraction**: Uses multimodal vision capabilities to automatically identify and capture the core system architecture diagram of the paper, embedding it directly into the note.
*   **Smart Retry**: Automatically attempts multiple mirrors (arxiv.org, export.arxiv.org) when downloading PDFs to improve success rates.
*   **Deduplication Mechanism**: Automatically filters duplicate papers to avoid redundancy.

---
*Powered by Doubao & PaperBrain Team*
