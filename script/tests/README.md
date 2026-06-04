# PaperBrain Test Layers

PaperBrain keeps tests under `script/tests/` and runs them through:

```bash
python script/paperbrain.py check
```

Current layers:

- Pure function tests: scoring, identity normalization, selection logic.
- File-system tests: run state, Obsidian note writing, digest upsert, date fixes.
- Network mock tests: arXiv and Hugging Face cache/fallback behavior with mocked HTTP responses.
- Pipeline helper tests: fetch/screen/deep-selection orchestration helpers without live LLM calls.
- CLI/tooling tests: command parsing, JSON stdout, path resolution, doctor/check helpers.

Live network or live LLM probes should stay out of unit tests. Use explicit doctor commands for those:

```bash
python script/paperbrain.py doctor arxiv --live
python script/paperbrain.py doctor llm --provider openrouter --live
```
