# PaperBrain-Doubao 🤖📄

Automated pipeline to fetch, filter, and analyze Robotics & AI papers using Doubao Seed 2.0 (via Volcengine), syncing results to your Obsidian vault.

## 🚀 Features

- **Daily Scraper**: Fetches latest papers from arXiv and Hugging Face Daily Papers.
- **Smart Filtering**: Uses Doubao Seed 2.0 Lite to score papers based on your research interests.
- **Obsidian Sync**:
  - **Daily Digest**: A summary of all relevant papers.
  - **Deep Analysis**: For high-scoring papers, downloads the PDF and uses Doubao Seed 2.0 Pro to generate detailed notes with methodology, innovations, and Sim2Real analysis.
- **Knowledge Linking**: Automatically links new notes to existing concepts in your Obsidian vault.

## 🛠️ Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**:
   Edit `config.yaml`:
   - Add your `doubao.api_key`.
   - Set `obsidian.vault_path` to your local Obsidian vault folder.
   - Customize `search.keywords` for your research focus.

3. **Run Manually**:
   ```bash
   python main.py --run-now
   ```

4. **Run as a Daemon (Local Scheduler)**:
   ```bash
   python main.py
   ```
   This will keep the script running and execute the job daily at the time specified in `config.yaml` (default 08:00).

## ⚙️ Automation

### Option 1: GitHub Actions (Recommended for Cloud)
If you host your Obsidian vault on GitHub (e.g., using Obsidian Git plugin), you can run this workflow automatically.

1. Create `.github/workflows/daily_papers.yml`.
2. Add the content below.
3. Set `GEMINI_API_KEY` in your GitHub Repository Secrets.

```yaml
name: Daily Paper Analysis
on:
  schedule:
    - cron: '0 0 * * *' # Runs at 00:00 UTC daily
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Run Analysis
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python main.py --run-now
        
      - name: Commit and Push changes
        run: |
          git config --global user.name 'PaperBrain Bot'
          git config --global user.email 'bot@paperbrain.com'
          git add Daily_Papers/ Research_Notes/
          git commit -m "📝 Daily paper update" || exit 0
          git push
```

### Option 2: Local Cron / Task Scheduler

**Linux/Mac (Cron)**:
```bash
crontab -e
# Add line:
0 8 * * * cd /path/to/PaperBrain-Gemini && /usr/bin/python3 main.py --run-now >> /tmp/paperbrain.log 2>&1
```

**Windows (Task Scheduler)**:
1. Open Task Scheduler.
2. Create Basic Task -> "Daily Paper Fetch".
3. Trigger: Daily at 08:00.
4. Action: Start a program.
   - Program/script: `python.exe` (path to your python executable)
   - Arguments: `main.py --run-now`
   - Start in: `D:\path\to\PaperBrain-Gemini`
