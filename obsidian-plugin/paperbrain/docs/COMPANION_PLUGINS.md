# Companion Obsidian plugins

PaperBrain Console has no required Obsidian plugin dependencies. The first ten
community plugins below are enabled in the development vault and were checked
with PaperBrain Console 0.5.1. The final two are installed locally but are not
currently enabled, so their integration is not claimed as tested. Install only
the capabilities that fit your workflow.

| Plugin | Local version | Status | PaperBrain workflow | Notes |
| --- | ---: | --- | --- | --- |
| BRAT (`obsidian42-brat`) | 2.0.2 | Enabled and checked | Install and update PaperBrain from GitHub Releases | Uses the latest compatible GitHub Release. |
| Dataview (`dataview`) | 0.5.68 | Enabled and checked | Query PaperBrain note properties and build research queues | PaperBrain-generated Markdown remains usable without Dataview. |
| Audio Player (`obsidian-audio-player`) | 0.1.1 | Enabled and checked | Play generated podcast audio with richer controls | Optional; Obsidian's native audio element remains supported. |
| floating toc (`floating-toc`) | 2.7.1 | Enabled and checked | Navigate long deep-analysis notes and research briefs | Most useful in reading views, not the console itself. |
| Highlightr (`highlightr-plugin`) | 1.2.2 | Enabled and checked | Add manual evidence and review highlights to generated notes | Highlights are user annotations and are not overwritten intentionally by PaperBrain. |
| Style Settings (`obsidian-style-settings`) | 1.0.9 | Enabled and checked | Tune the active Obsidian theme around the console | PaperBrain uses Obsidian theme variables and does not require a specific theme. |
| Immersive Translate (`immersive-translate`) | 0.0.2 | Enabled and checked | Translate generated research notes | Its floating controls can cover narrow panels; collapse the overlay while operating the console. |
| Smart Connections (`smart-connections`) | 4.1.8 | Enabled and checked | Explore semantic relationships among PaperBrain notes | Indexing and model/privacy settings belong to Smart Connections. |
| Copilot (`copilot`) | 3.2.3 | Enabled and checked | Ask follow-up questions across generated notes | Uses its own provider configuration and may incur separate model charges. |
| Claudian (`realclaudian`) | 2.0.24 | Enabled and checked | Advanced coding-agent workflows inside the vault | High-permission power-user tool; review its command and file-write permissions separately. |
| Translay Translator (`aqu-translay-translator`) | 0.8.4 | Installed, currently disabled | Translate note and interface text through a floating overlay | Uses its own local or cloud translation resources; its floating control may need to be moved away from a narrow console. |
| Components (`components`) | 3.1.260325 | Installed, currently disabled | Build reusable Obsidian content components | Separately licensed and configured; PaperBrain does not depend on component rendering. |

The exact tested snapshot is also available in
[`companion-plugins.json`](companion-plugins.json) for tooling and release
audits. Version numbers document compatibility; they are not hard pins.

## Installation boundaries

- Install each companion from Obsidian Community plugins or its own official
  release channel. Do not copy another plugin's files into PaperBrain's folder.
- PaperBrain does not call companion plugin APIs, so disabling one cannot break
  the pipeline, console, notes, or artifacts.
- Each companion has its own license, data handling, network behavior, model
  costs, and update policy. Review those terms independently.
- When diagnosing layout issues, first close translation overlays and other
  floating controls, then test PaperBrain with the default Obsidian theme.
