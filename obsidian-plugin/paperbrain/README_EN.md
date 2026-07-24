# PaperBrain Console

[简体中文](README.md) | **English**

PaperBrain Console is the Obsidian desktop interface for the
[PaperBrain Python pipeline](https://github.com/DannyWANGD/PaperBrain). It
installs the backend, starts or stops runs, shows progress, and opens the
digests, research notes, PDFs, figures, and audio written to the active vault.

The plugin is desktop-only because it starts local processes. Plugin `0.5.1`
initially installs PaperBrain backend `0.3.6`; its settings can then check and
update both stable components.

## Quick Start

1. Install and enable BRAT. Choose **Add beta plugin** and enter
   `https://github.com/DannyWANGD/obsidian-paperbrain`.
2. Enable **PaperBrain Console**, open the console, and select the recommended
   **Terminal install (recommended)**.
3. Select Windows, macOS, or Linux, copy the command, and run it in your own
   terminal. Return to the plugin and select **Detect again** when it finishes.
4. Select **Open API key file**, enter your API key, and save the file.
5. Select **Validate setup**. When validation passes, choose a run mode and
   select **Run**.

You can instead select **Install inside Obsidian** to keep the existing one-click
flow. Both methods reuse Conda when possible and otherwise install isolated
Miniforge. Neither requires a backend checkout or preinstalled Python.

## Requirements

- Obsidian desktop 1.5.0 or later
- Approximately 1 GB of free disk space
- Access to GitHub Releases, conda-forge, and at least one Python package index
- An OpenRouter or Doubao account and API key

Advanced users can provide a PaperBrain 0.3.x backend with Python 3.9 or later.

## Install The Plugin

BRAT is recommended because it installs and updates the plugin from a single
GitHub Release.

For manual installation, download `main.js`, `manifest.json`, and `styles.css`
from the same [Release](https://github.com/DannyWANGD/obsidian-paperbrain/releases).
Place them in `<vault>/.obsidian/plugins/paperbrain/`, then reload Obsidian.
`checksums.txt` is an optional integrity record. GitHub's generated Source code
archives do not replace the three runtime files.

## Backend Installation

The recommended **Terminal install (recommended)** action generates a command
for Windows, macOS, or Linux. Running it in your own terminal lets downloads
inherit that shell's `HTTP_PROXY`, `HTTPS_PROXY`, and related network settings.
The command downloads `install-backend.ps1` on Windows or `install-backend.sh`
on macOS/Linux from the matching plugin Release and verifies its fixed SHA-256
before execution.

Select **Install inside Obsidian** when you do not want to use a terminal. Both
installation methods:

1. Detects and reuses an existing Conda installation when available.
2. Creates or reuses an environment named `wd`. A new environment uses Python
   3.10. An existing environment must use Python 3.9 or later and pip 24 or
   later; otherwise installation stops before backend assets are downloaded.
3. If Conda is unavailable, downloads and verifies Miniforge 26.3.2-2 from
   conda-forge and installs it under `~/.paperbrain/runtime/miniforge3`. This
   private installation does not modify system PATH, initialize a shell, or
   require administrator access.
4. Downloads the wheel and hash-locked dependencies from the `backend-0.3.6`
   Release and verifies their SHA-256 checksums.
5. In the default **Auto** mode, downloads the same fixed 1.6 MB probe wheel
   from official PyPI, Alibaba Cloud, USTC, and Tsinghua TUNA. Only sources
   that pass SHA-256 verification are timed. All locked dependencies are then
   installed from the fastest valid source without mixing indexes. A source
   can also be selected manually.
6. Creates configuration under `~/.paperbrain/config` for the active vault.
   Existing configuration and `.env` files are preserved.

Running the copied command confirms terminal installation; in-app installation
uses a confirmation dialog. Temporary files are removed after success or
failure. After terminal installation, select **Detect again** so the plugin can
record the `wd` Python, CLI, and default configuration paths.

| Item | Windows | macOS / Linux |
| --- | --- | --- |
| Private Miniforge | `%USERPROFILE%\.paperbrain\runtime\miniforge3` | `~/.paperbrain/runtime/miniforge3` |
| Configuration and API key | `%USERPROFILE%\.paperbrain\config` | `~/.paperbrain/config` |
| Generated content | Active Obsidian vault | Active Obsidian vault |

To remove the private runtime, close Obsidian and delete
`~/.paperbrain/runtime/miniforge3`. Delete `~/.paperbrain/config` only when its
configuration and API key are no longer needed. Do not delete an external
Conda installation that the plugin merely reused.

## API Key And Settings

**Open API key file** opens `~/.paperbrain/config/.env`. Configure only the
provider you use:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
# DOUBAO_API_KEY=your_doubao_api_key
```

API keys are not stored in Obsidian plugin settings. **Validate setup** runs
`doctor config`, `doctor env`, and `doctor llm` locally without `--live`, so it
does not make a model request.

Important settings:

- **Dependency download source** defaults to Auto. You can instead select
  PyPI, Alibaba Cloud, USTC, TUNA, or one credential-free HTTPS simple index.
- **Network proxy** inherits the environment that started Obsidian by default.
  You can instead provide a credential-free `http://` or `https://` proxy with
  an explicit port, or select Direct to clear proxies. **Test connection**
  checks the plugin downloader and, when available, the backend's Hugging Face
  and arXiv connections without calling a model.
- **Software updates** checks the Console and managed wheel together. A Console
  update replaces only verified `main.js`, `manifest.json`, and `styles.css`
  files and takes effect after restarting Obsidian. A backend update uses pip in
  the same `wd` environment and preserves configuration. Source mode is never
  overwritten.
- **Default provider** selects the provider used for new runs.
- **API key file** always opens the local `.env` file; API keys are not stored
  in Obsidian plugin settings.
- **Advanced** contains source-backend, CLI, config, vault, podcast, and
  cancellation settings.

## Data, Network, And Cost

- The plugin has no telemetry, advertising, or paid features. It stores local
  runtime settings only.
- It starts a local backend process and reads run records and generated files
  in the active vault.
- The backend accesses arXiv, Hugging Face, and the selected model provider.
  Depending on the run mode, paper metadata, extracted PDF text, or rendered
  pages may be sent to the provider and may incur charges.
- The backend writes digests, notes, PDFs, assets, indexes, caches, and run
  records to the configured vault. Back up important vaults.

See [SECURITY.md](SECURITY.md) for permissions, network boundaries, and
reporting. The MIT License covers the plugin code only. The backend, papers,
model services, and generated or downloaded content retain their own licenses
and terms.

## Compatibility

| Plugin | Backend | Obsidian |
| --- | --- | --- |
| 0.5.1 | Initial installer pins 0.3.6; compatible 0.3.x wheels can be updated | 1.5.0 or later, desktop |

## Troubleshooting

- **Terminal installation failed:** keep the terminal output, confirm proxy and
  GitHub access, then run the same command again.
- **In-app installation failed:** keep the console open, retry
  **Install inside Obsidian**, and inspect the failed stage and final error.
- **Every package index failed:** confirm network access or select a known
  working source in settings.
- **`paperbrain` was not found:** set CLI executable to its absolute path in
  the `wd` environment.
- **Validation failed:** confirm **Vault path** and check the API key in
  `~/.paperbrain/config/.env`.
- **Python-script mode failed:** confirm that the backend directory contains
  `script/paperbrain.py`.

## Optional Companion Plugins

PaperBrain Console has no required Obsidian plugin dependencies. These plugins
can be added as needed:

| Plugin | ID | Use |
| --- | --- | --- |
| BRAT | `obsidian42-brat` | Install and update PaperBrain from GitHub Releases |
| Dataview | `dataview` | Query paper properties and build reading or reproduction queues |
| Audio Player | `obsidian-audio-player` | Play generated podcast audio |
| floating toc | `floating-toc` | Navigate long research notes and briefs |
| Highlightr | `highlightr-plugin` | Mark evidence and review points manually |
| Style Settings | `obsidian-style-settings` | Configure Obsidian themes |
| Immersive Translate | `immersive-translate` | Translate generated research notes |
| Smart Connections | `smart-connections` | Explore semantic relationships between notes |
| Copilot | `copilot` | Ask follow-up questions about vault content |
| Claudian | `realclaudian` | Run coding-agent workflows in the vault |
| Translay Translator | `aqu-translay-translator` | Translate notes and interface text |
| Components | `components` | Build reusable Obsidian content components |

See [Companion plugins](docs/COMPANION_PLUGINS.md) for installation notes and
caveats.

## Development And Releases

```bash
npm ci
npm run check
```

Source lives under `src/`. The Release workflow builds `main.js`. The release
tag must match `manifest.json`, and each Release must include `main.js`,
`manifest.json`, `styles.css`, `install-backend.ps1`, `install-backend.sh`, and
`checksums.txt`.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and
[CHANGELOG.md](CHANGELOG.md) for project policies.
