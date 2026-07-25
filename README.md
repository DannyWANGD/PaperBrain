# PaperBrain 2.0

![PaperBrain architecture](paperbrain_arch.png)

<p align="center">
  <img alt="Python 3.9+" src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white">
  <img alt="Obsidian first" src="https://img.shields.io/badge/Obsidian-first-7C3AED?logo=obsidian&logoColor=white">
  <img alt="OpenRouter" src="https://img.shields.io/badge/OpenRouter-ready-111827">
  <img alt="arXiv" src="https://img.shields.io/badge/arXiv-tracking-B31B1B?logo=arxiv&logoColor=white">
  <img alt="Tests" src="https://img.shields.io/badge/tests-unittest-0F766E">
</p>

PaperBrain 2.0 is an Obsidian-first research assistant for tracking frontier papers in robotics, embodied AI, VLA, world models, reinforcement learning, and robot manipulation.

It turns a noisy daily paper stream into a durable local knowledge base: scored paper digests, deep reading notes, PDFs, architecture figures, searchable Obsidian properties, research queues, open questions, weekly/monthly briefs, and optional podcast summaries.

`arXiv` / `Hugging Face` / `OpenRouter` / `Obsidian` / `Research Notes` / `Weekly Briefs`

## 📚 Contents

- [Why PaperBrain](#why-paperbrain)
- [Core Workflow](#core-workflow)
- [Quick Start](#quick-start)
- [Daily Usage](#daily-usage)
- [Research Index And Briefs](#research-index-and-briefs)
- [Vault Structure](#vault-structure)
- [Key Concepts](#key-concepts)
- [Configuration](#configuration)
- [Maintenance Commands](#maintenance-commands)
- [Development Checks](#development-checks)

## <a id="why-paperbrain"></a> 🧭 Why PaperBrain

Research tracking usually fails in two places: too many papers arrive every day, and even useful papers become hard to retrieve after the first reading. PaperBrain is built to keep the daily workflow small while preserving the evidence behind every decision.

It is designed for a researcher who wants to:

- 🔎 **Monitor** arXiv and Hugging Face papers in a focused research area.
- 🧪 **Screen** many papers but deeply read only the strongest ones.
- 🧾 **Audit** every scoring decision and rerun interrupted jobs.
- 📖 **Study** with Obsidian notes that preserve IDs, tags, formulas, links, and follow-up questions.
- 🧠 **Synthesize** a week or month as a coherent research trend rather than disconnected summaries.

| Signal | What PaperBrain Gives You |
| --- | --- |
| 🔎 Search | Date-based arXiv and Hugging Face paper collection |
| 🧪 Triage | Two-stage scoring with full screening records |
| 📖 Reading | Deep Obsidian notes with formulas, links, figures, and questions |
| 🧠 Memory | Stable `paper_id`, normalized tags, queues, and Bases views |
| 🗓️ Synthesis | Daily digests plus weekly, monthly, and range-based research briefs |

## <a id="core-workflow"></a> 🧬 Core Workflow

```text
arXiv + Hugging Face Daily Papers
  -> canonical paper identity
  -> two-stage screening
  -> full screening record
  -> daily digest
  -> selected deep analysis notes
  -> Research_Index + Obsidian tags/Bases
  -> Research_Briefs + open questions
  -> backlinks + optional podcast
```

The daily digest is broad: by default, it includes every paper with `score >= 7.0`, then quality-backfills from the remaining papers until it reaches 5 entries when the hard-threshold pool is too small. Deep analysis is stricter: PaperBrain selects the strongest 1-2 papers above the lower threshold, then adds any extra papers above the upper threshold.

## <a id="quick-start"></a> ⚡ Quick Start

PaperBrain supports Python 3.9 or later. For a fresh checkout, use the dedicated Python 3.10 `wd` environment below. Every backend command in this README assumes that `wd` is active.

### 1. Create The Recommended Environment

```powershell
cd <path-to-PaperBrain>
conda create -n wd python=3.10 -y
conda activate wd
python -m pip install --upgrade pip
python -m pip install -e .
```

The editable install brings in the backend dependencies and registers the `paperbrain` command while keeping this checkout as the active source tree.

For an exact release dependency graph, stay in the same `wd` environment and use these two commands instead of `python -m pip install -e .`:

```powershell
python -m pip install --require-hashes -r script/requirements.lock
python -m pip install --no-deps -e .
```

### 2. Configure One LLM Provider

Create `script/.env` from the template. On Windows PowerShell:

```powershell
Copy-Item script\config\.env.example script\.env
```

On macOS or Linux:

```bash
cp script/config/.env.example script/.env
```

Add the key for the provider you intend to use. You do not need to configure both providers:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
# DOUBAO_API_KEY=your_doubao_api_key_here
```

### 3. Validate Before Spending Tokens

```powershell
paperbrain doctor config
paperbrain doctor env
paperbrain doctor network --live
paperbrain doctor llm --provider openrouter
```

Diagnostics are local by default. `doctor network --live` checks Hugging Face and arXiv without invoking a model; the LLM live check is the only diagnostic that can incur provider usage.

### 4. Run The Pipeline

```powershell
paperbrain run --provider openrouter
```

To process a specific paper date instead of today:

```powershell
paperbrain run --date 2026-06-01 --provider openrouter
```

### 5. Connect Obsidian

For this checkout on Windows, sync the built plugin files into the vault:

```powershell
powershell -ExecutionPolicy Bypass -File obsidian-plugin\sync_plugin.ps1
```

Open the repository root as an Obsidian vault, enable **PaperBrain Console** under Community plugins, and set its backend checkout path to this repository. If Obsidian cannot find the CLI, run `where.exe paperbrain` inside the active `wd` environment and use that absolute path in the plugin settings.

## <a id="daily-usage"></a> 🗓️ Daily Usage

### 🚀 Run Modes

| Mode | Goal | Command |
| --- | --- | --- |
| 🗓️ Daily | Today | `paperbrain run --provider openrouter` |
| 📅 Calendar | Specific date | `paperbrain run --date 2026-06-01 --provider openrouter` |
| 🧰 Debug | Fetch only | `paperbrain fetch --date 2026-06-01 --provider openrouter` |
| 🧪 Debug | Screening only | `paperbrain screen --date 2026-06-01 --provider openrouter` |
| 📖 Debug | Deep analysis only path | `paperbrain deep --date 2026-06-01 --provider openrouter` |
| 🔁 Resume | Continue previous run | `paperbrain run --date 2026-06-01 --provider openrouter --resume` |
| ♻️ Reset | Clean rerun | `paperbrain run --date 2026-06-01 --provider openrouter --force` |
| 🎧 Audio | Skip podcast | `paperbrain run --provider openrouter --no-podcast` |
| 🎯 Focus | Single paper | `paperbrain run --provider openrouter --arxiv-url https://arxiv.org/abs/2606.02486` |
| 📰 Digest | Digest only | `paperbrain digest --date 2026-05-22 --provider openrouter` |

The unified CLI writes human logs and progress to stderr, and writes the final machine-readable JSON summary to stdout. The JSON includes `exit_code`, `run_dir`, `state_path`, `artifacts`, and any structured `errors`.

### 📌 What To Check After A Run

| Type | Output | Purpose |
| --- | --- | --- |
| 📰 Digest | `Daily_Papers/YYYY-MM-DD-PaperDigest.md` | Daily map of threshold papers, with quality backfill when sparse |
| 🧾 Audit | `Run_Records/YYYY-MM-DD-openrouter/screening_report.md` | Human-readable screening audit |
| 💾 State | `Run_Records/YYYY-MM-DD-openrouter/state.json` | Resume state and machine-readable screening data |
| 🧯 Errors | `Run_Records/YYYY-MM-DD-openrouter/errors.json` | Structured error objects with retry guidance |
| 🪵 Logs | `Run_Records/YYYY-MM-DD-openrouter/log_summary.md` | Compact stage/artifact log summary |
| 📖 Notes | `Research_Notes/*.md` | Deep analysis notes for selected papers |
| 🧭 Index | `Research_Index/Research_Index.md` | Obsidian research dashboard |
| 📊 Base | `Research_Index/Paper_Library.base` | Obsidian Bases table view |

Each digest entry includes score, innovation, limitations, note/web link, authors, institutions, and tags/source when available.

## <a id="research-index-and-briefs"></a> 🧭 Research Index And Briefs

Rebuild the Obsidian index and normalize note frontmatter:

```bash
paperbrain index
```

Regenerate index files without rewriting notes:

```bash
paperbrain index --no-update-notes
```

Generate a weekly brief:

```bash
paperbrain brief --mode week --week 2026-W23
```

Generate a monthly brief:

```bash
paperbrain brief --mode month --month 2026-06
```

Generate a custom or rolling range:

```bash
paperbrain brief --mode range --from-date 2026-06-01 --to-date 2026-06-07
paperbrain brief --mode range --last-days 14 --date 2026-06-03
```

Briefs are written to `Research_Briefs/` and use this structure:

```text
1. Executive Summary
2. Top Papers This Period
3. Research Trend Map
4. Novel Signals
5. Repeated Patterns And Saturation
6. Evidence Quality
7. Reading Plan For Next Period
8. Open Research Questions
9. Manual Notes
```

## <a id="vault-structure"></a> 🗂️ Vault Structure

```text
Daily_Papers/       daily paper digests
Research_Notes/     deep paper notes
Research_Index/     library index, queues, Bases view, tag guide
Research_Briefs/    weekly, monthly, and custom-range synthesis briefs
Run_Records/        per-run directories with state, reports, logs, and errors
PDFs/               downloaded papers
Assets/             extracted figures and architecture images
Podcasts/           optional audio summaries
script/             pipeline code
```

## <a id="key-concepts"></a> 🔑 Key Concepts

### 🪪 Paper Identity

Each paper is tracked by a stable `paper_id`, usually in the form `arxiv:2606.02486`. File names, short titles, and aliases can change; `paper_id` is the identity anchor.

### 📅 Date Semantics

`publication_date` means the authoritative published/listed date from arXiv or Hugging Face. It is the date used for daily digests and time-range briefs.

If the AI metadata extractor sees a different date in the paper PDF or project page, PaperBrain stores it separately as `metadata_publication_date`.

### 🏷️ Obsidian Tags And Properties

The indexer maintains Obsidian-native properties:

```text
paper_id, arxiv_id, score, domains, methods, tasks,
paper_type, impact_band, reading_status, review_status,
priority_score, next_action
```

It also generates nested tags such as:

```text
domain/vla
domain/world_model
method/latent_world_model
method/diffusion_policy
task/manipulation
impact/high_value
status/unread
```

## <a id="configuration"></a> ⚙️ Configuration

Main configuration files:

| File | Purpose |
| --- | --- |
| `script/config/config.yaml` | Model routing, thresholds, search scope, Obsidian paths |
| `script/config/prompts.yaml` | Screening, deep analysis, refinement, vision, and alias prompts |
| `script/config/tags.yaml` | Research taxonomy and tag behavior |
| `script/config/.env.example` | API key template |

Important analysis knobs:

```yaml
analysis:
  daily_digest_min_score: 7.0
  daily_digest_target_min_count: 5
  deep_analysis_lower_threshold: 7.5
  deep_analysis_extra_threshold: 8.8
  daily_deep_analysis_base_max: 2
  screening_second_stage_ratio: 0.25
  screening_second_stage_max_k: 20
```

Research discovery is configured in the same file and is also editable from
PaperBrain Console. At least one keyword is required. Selected mode scans every
paper in the chosen official arXiv categories for the target day; all mode scans
the complete daily arXiv metadata range. Keywords are applied locally to titles
and abstracts before any model call.

```yaml
search:
  keywords:
    - "Robot Manipulation"
    - "Vision Language Action"
  arxiv_category_mode: "selected"  # selected or all
  arxiv_categories:
    - "cs.RO"
    - "cs.AI"
  arxiv_page_size: 200  # 1-2000; legacy max_results is treated as page size
```

The arXiv scanner follows `totalResults` with `start` pagination, caches each
page independently, removes duplicate arXiv IDs, and records page/candidate/
keyword-match counts under the run state's `selection.discovery` field. The
same deterministic Unicode-normalized keyword matcher is used for Hugging Face
Daily Papers.

OpenRouter routing excludes Anthropic, Google, and OpenAI model families across every task. Fast screening uses low-latency DeepSeek/Qwen/StepFun models, while detailed screening, deep analysis, learning resources, podcast writing, and vision use task-specific GLM 5.2, Kimi K3, Grok 4.5, Qwen 3.7, MiniMax M3, and related fallbacks. Learning-resource generation can use OpenRouter web search and therefore may add a small provider-side search charge; control it with `analysis.learning_resources_web_search_enabled`.

## <a id="maintenance-commands"></a> 🛠️ Maintenance Commands

Repair note dates from saved run records if older notes used model-extracted dates:

```bash
python script/fix_publication_dates.py 2026-05-29 2026-06-01 2026-06-02
```

Generate a podcast for an existing note:

```bash
python script/generate_podcast.py "AHEAD for Dynamic VLA Manipulation.md" --provider openrouter --minutes 6
```

Primary command entry points:

| Entry | Status | Use |
| --- | --- | --- |
| `paperbrain` | Recommended | Installed unified CLI: `run`, `fetch`, `screen`, `deep`, `digest`, `cancel`, `dry-run`, `bridge`, `index`, `brief`, `doctor`, `check` |
| `script/paperbrain.py` | Source fallback | Direct checkout entry point when the editable CLI is unavailable |
| `script/main.py` | Compatibility wrapper | Old daily entry; prints a migration hint and forwards to `paperbrain.py run` |
| `script/build_research_index.py` | Compatibility wrapper | Old index entry; prints a migration hint and forwards to `paperbrain.py index` |

### Obsidian Plugin

The desktop-only PaperBrain Console plugin is a lightweight control surface. Python remains the source of truth for fetching, screening, deep analysis, digest writing, indexing, run-state, and diagnostics.

Plugin source:

```text
obsidian-plugin/paperbrain/
```

Local Obsidian runtime copy:

```text
.obsidian/plugins/paperbrain/
```

Sync source files into the local plugin directory:

```powershell
powershell -ExecutionPolicy Bypass -File obsidian-plugin\sync_plugin.ps1
```

The plugin calls commands such as:

```powershell
paperbrain digest --date 2026-05-22 --provider openrouter
paperbrain cancel --reason plugin_stop
paperbrain dry-run --mode digest --date 2026-05-22 --provider openrouter
```
| `script/generate_research_brief.py` | Kept maintenance command | Weekly, monthly, and date-range briefs |
| `script/generate_podcast.py` | Kept maintenance command | Podcast from an existing note |
| `script/fix_publication_dates.py` | Kept maintenance command | Repair note dates from run-state data |
| `script/normalize_note_filenames.py` | Kept maintenance command | One-off filename/link normalization |

Organized implementations live in `script/tools/`. The top-level `script/*.py` commands are kept as stable wrappers.

## <a id="development-checks"></a> ✅ Development Checks

```bash
paperbrain doctor
paperbrain check
paperbrain index --no-update-notes
```

Useful focused checks:

```bash
paperbrain check --skip-tests --skip-lint
paperbrain check --strict-lint
paperbrain doctor config
paperbrain doctor env
paperbrain doctor arxiv
paperbrain doctor network
paperbrain doctor llm --provider openrouter
paperbrain doctor obsidian
```

Live probes are opt-in:

```bash
paperbrain doctor arxiv --live
paperbrain doctor network --live
paperbrain doctor llm --provider openrouter --live
```

Tooling files:

| File | Purpose |
| --- | --- |
| `pyproject.toml` | Package metadata, editable `paperbrain` entry point, dependencies, Ruff config |
| `.pre-commit-config.yaml` | Ruff, formatting, trailing whitespace, EOF, and YAML hooks |
| `.github/workflows/paperbrain-check.yml` | CI preview that installs requirements and runs `paperbrain check` |
| `script/tests/README.md` | Test layer map and live-probe boundary |

## 🧩 Operational Notes

- `Run_Records/` makes every screening decision auditable and resumable; each run now has a fixed directory with `state.json`, `screening_report.md`, `log_summary.md`, and `errors.json`.
- `paper_id` prevents aliases and title changes from breaking deduplication.
- Daily digests are broad maps; deep analyses are high-confidence selections.
- The Research Index relies on Obsidian tags, properties, and Bases rather than fixed theme pages.
- If arXiv rate limits the feed API, PaperBrain uses local feed caching, a minimum request interval, exponential backoff, and a cooldown marker under `Cache/arxiv/`. Rerun the same command later rather than repeatedly using `--force`; completed stages are preserved in `Run_Records/` when possible.
- If arXiv rate limits PDF downloads, PaperBrain reuses existing files from `PDFs/` or `Cache/pdfs/`, then falls back to title/abstract-only rigorous screening when the PDF is unavailable.
