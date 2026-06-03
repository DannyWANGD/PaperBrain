# PaperBrain Development Context

Last updated: 2026-06-02

## Goal

PaperBrain is an Obsidian-first research assistant for tracking frontier Embodied AI / Robotics / VLA / World Model papers. The workflow is:

1. Fetch papers from arXiv and Hugging Face Daily Papers.
2. Run two-stage LLM screening.
3. Download PDFs for high-value candidates.
4. Extract text and key architecture figures.
5. Generate deep technical notes with RAG context.
6. Write Obsidian notes and daily digests.
7. Maintain backlinks and a generated research index.
8. Optionally generate podcasts.

## Important Architecture Change

The old `Research_Themes` / `theme_manager.py` system has been removed.

Paper organization is now handled by `Research_Index`:

- `script/src/research_indexer.py` scans `Research_Notes`.
- It rewrites frontmatter with structured properties and nested tags.
- It generates:
  - `Research_Index/Research_Index.md`
  - `Research_Index/Tag_Guide.md`
  - `Research_Index/Reading_Queue.md`
  - `Research_Index/Paper_Library.base`

Use tags/properties/Bases as the main organization layer:

- `domain/...`
- `method/...`
- `task/...`
- `type/...`
- `impact/...`
- `status/...`

## Main Files

| File | Purpose |
|---|---|
| `script/main.py` | Main scheduled/immediate workflow |
| `script/build_research_index.py` | Rebuild Research_Index |
| `script/src/scraper.py` | arXiv and Hugging Face fetcher |
| `script/src/analyser.py` | LLM screening, deep analysis, PDF figure extraction |
| `script/src/obsidian_writer.py` | Daily digest and paper note writer |
| `script/src/research_indexer.py` | Obsidian tags/properties/Bases indexer |
| `script/src/knowledge_base.py` | Lightweight RAG over existing notes |
| `script/src/gardener.py` | Backlink maintenance |
| `script/src/podcaster.py` | Podcast generation |
| `script/config/config.yaml` | Models, thresholds, paths |
| `script/config/prompts.yaml` | LLM prompts |
| `script/config/tags.yaml` | Tag taxonomy |

## Model Policy

OpenRouter should avoid Claude / OpenAI / Gemini by default because of user regional issues.

Preferred model families:

- DeepSeek V4 Pro / V4 Flash
- Qwen3.7 Max / Qwen3.6 Flash / Qwen3-VL
- Z.ai GLM 5.1 / GLM 5V
- Moonshot Kimi K2.6 / K2.5
- xAI Grok 4.3 as high-performance fallback

Vision calls should use Qwen-VL / GLM-V / Kimi-style multimodal models, not Gemini/OpenAI vision models.

## Common Commands

```bash
python script/main.py --run-now --provider openrouter
python script/main.py --run-now --date 2026-03-20 --provider openrouter
python script/main.py --run-now --provider openrouter --arxiv-url https://arxiv.org/abs/2603.19199
python script/main.py --run-now --provider openrouter --no-podcast
python script/build_research_index.py
python script/build_research_index.py --no-update-notes
python script/generate_podcast.py "FASTER.md" --provider openrouter --minutes 6
```

## Editing Boundaries

- Prefer modifying `script/` source/config and generated `Research_Index/` artifacts.
- Do not delete historical `Research_Notes`, `PDFs`, `Assets`, `Daily_Papers`, or `Podcasts` unless explicitly requested.
- The user explicitly requested removal of old `Research_Themes`, and that directory/code path has been removed.
- API keys must remain in `.env` only.
- Keep Windows path compatibility.

## Known Follow-Ups

- Add regression tests for LLM JSON sanitization and indexer frontmatter rewriting.
- Add JSON schema / `response_format` to high-value JSON calls where supported.
- Add a low-confidence tag review queue.
- Consider normalizing PDF filenames through `ObsidianWriter.get_pdf_path_from_paper()`.
