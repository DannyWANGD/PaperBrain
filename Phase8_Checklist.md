# Phase 8: Runtime UX and Failure Audit

Updated: 2026-06-04

## Checklist

- [x] Runtime plugin sync risk: source plugin and `.obsidian/plugins/paperbrain` can diverge. Synced `manifest.json`, `main.js`, and `styles.css` into the Obsidian runtime folder and syntax-checked the runtime `main.js`.
- [x] Timeline empty-state risk: a run with no saved papers should still show stage cards and useful status. Timeline now always renders the seven stages and a live status band.
- [x] Ambiguous Paper Queue risk: early stages used to show only `No saved papers for this run.` or a table with weak context. Paper Queue now shows stage-aware empty text, queue metrics, coarse-score fallback, PDF/Note/Digest/Deep counts, and warning/error counts.
- [x] Log-driven progress risk: plugin progress depended too much on plain-text output guessing. Run-state logs now include `event_type`, `status`, and `ts`; the plugin prefers these structured events and keeps stdout/stderr hints as a fallback.
- [x] Artifacts scroll reset risk: polling and log updates rebuilt the whole panel and forced the view back to the top. The plugin now captures and restores per-panel scroll position after render.
- [x] Old run-state compatibility risk: historical logs may not have `event_type/status/ts`. The plugin handles both old and new log shapes.
- [x] Digest refresh risk: current visible run state did not include the new event fields. Re-ran digest-only for `2026-06-03/openrouter`, updating `state.json`, `log_summary.md`, and `PaperDigest` without re-running screening or deep analysis.
- [x] Queue interpretation risk: final score is absent during fetch/coarse stages. Queue sorting and display now use final `score` when present, otherwise `coarse_score`, otherwise `new`.
- [x] UI density risk: status feedback could become decorative or noisy. Added compact metrics and subtle status pulses instead of large cards or explanatory blocks.
- [x] Validation risk: changes could break Python state writing or plugin JavaScript. Ran focused Python tests, Python compile check, source `node --check`, and runtime `node --check`.

## Remaining Manual Acceptance

- [ ] Reload Obsidian and confirm the Timeline panel visually matches the current theme.
- [ ] During a real long run, confirm the active stage advances as expected from Fetch through Digest/Index/Podcast.
- [ ] Scroll halfway down Artifacts while a command is running and confirm refreshes no longer jump the panel to the top.
