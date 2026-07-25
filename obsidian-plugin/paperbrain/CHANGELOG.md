# Changelog

All notable changes to this project are documented in this file. Releases
follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.6.1] - 2026-07-25

### Fixed

- Settings sections now place their headings above their controls so long
  descriptions and wide controls cannot overlap in wide settings windows.

## [0.6.0] - 2026-07-25

### Added

- Research discovery settings for editing local interest keywords and the full
  official arXiv category catalog without duplicating preferences in plugin data.
- Searchable grouped category selection with group toggles, defaults, clear,
  and an All arXiv mode.

### Changed

- Discovery preferences are validated and written to the backend YAML config
  through a same-directory temporary file with rollback on replacement failure.
- Settings are organized into Research discovery, Runtime & updates, Network &
  provider, and Advanced sections with responsive theme-native styling.
- New installations now pin PaperBrain backend 0.3.7 and its published wheel
  checksum.

## [0.5.1] - 2026-07-24

### Added

- One update check in settings for the latest stable PaperBrain Console and
  managed backend wheel, with separate update actions.
- Verified Console self-updates that replace only the three runtime assets,
  roll back failed replacements, preserve local settings, and require restart.

### Changed

- Managed backend updates reuse the existing hash-verified wheel installer and
  leave Python source checkouts under developer control.

### Fixed

- In-app backend installation now passes the selected proxy environment to the
  actual download and child-process plan, not only to its confirmation dialog.

## [0.5.0] - 2026-07-24

### Added

- Proxy modes for inheriting the Obsidian environment, using one manual
  credential-free HTTP(S) proxy, or forcing direct connections.
- A connection test covering the plugin downloader and the backend's live
  Hugging Face and arXiv diagnostics without model requests.

### Changed

- In-app installation and backend runs now share the selected proxy
  environment. Terminal installation continues to inherit its own shell.
- The installer now pins PaperBrain backend 0.3.6.
- GitHub Release publishing now marks versioned releases as stable.

## [0.4.7] - 2026-07-24

### Changed

- Plugin settings now contain a permanent **API key file** action for opening
  the local `.env` used by OpenRouter or Doubao. It remains available after
  runtime detection hides the initial setup guide.
- The action falls back to `~/.paperbrain/config/.env` before a saved config
  path exists and reports the expected path when backend setup is incomplete.

## [0.4.6] - 2026-07-24

### Fixed

- The macOS/Linux terminal installer now reads the Conda environment list with
  the base Python executable instead of taking the last `conda run` output
  line. Conda versions that append a blank line no longer hide an existing or
  newly created `wd` environment.
- The terminal installer switches to the user's home directory before starting
  Conda, so it also remains valid when BRAT replaced the plugin directory from
  which the terminal was opened.

## [0.4.5] - 2026-07-24

### Added

- A recommended terminal installation flow that generates copyable, verified
  commands for Windows PowerShell, macOS Terminal, and Linux terminals.
- Versioned PowerShell and Bash installer assets that inherit the terminal's
  proxy environment while preserving the same pinned downloads, SHA-256
  checks, Conda reuse, private Miniforge fallback, and fastest-source probe as
  the in-app installer.

### Changed

- Setup detection now records the installed `wd` CLI and default configuration
  after a terminal installation. The existing in-app installer remains
  available as a separate choice.

## [0.4.4] - 2026-07-24

### Changed

- The backend installation log viewport is taller, increasing its maximum
  height from 240px to 400px.

## [0.4.3] - 2026-07-24

### Changed

- The backend installation log now follows the newest output line as progress
  updates while retaining the complete scrollback.

## [0.4.2] - 2026-07-24

### Fixed

- The plugin now resolves the selected dependency source and passes it to both
  the installation confirmation and backend installer. Version 0.4.1 omitted
  this value, causing every one-click backend installation to fail before any
  download began.
- A bundle-level regression test now verifies the complete Auto-source wiring
  from the plugin entry point to the backend installer.

## [0.4.1] - 2026-07-23

### Changed

- Backend dependency downloads default to an actual, hash-verified 1.6 MB wheel
  speed test across official PyPI, Alibaba Cloud, USTC, and Tsinghua TUNA, then
  use only the fastest working source. Any source or one credential-free HTTPS
  index can be fixed manually.
- Newly created `wd` environments require pip 24 or later.

### Fixed

- The installer now validates that an existing `wd` uses Python 3.9 or later
  and pip 24 or later before downloading or modifying backend files.

## [0.4.0] - 2026-07-23

### Added

- A confirmed, one-click backend installer that prioritizes an existing Conda
  installation and creates or reuses its isolated `wd` environment.
- Automatic private Miniforge 26.3.2-2 installation when Conda is unavailable,
  without system PATH changes, shell initialization, or administrator access.
- Fixed release manifests and SHA-256 verification for every Miniforge,
  PaperBrain wheel, and locked-requirements download.
- Managed configuration bootstrap under `~/.paperbrain/config`, with existing
  files and API key values preserved.
- Installer lifecycle tests covering existing Conda reuse, the no-Conda path,
  environment creation, and checksum rejection.

### Changed

- New-computer setup now starts with **Install backend** inside Obsidian; a
  repository clone and terminal-based Python installation are no longer part of
  the normal BRAT flow.
- Setup and security documentation now disclose installer destinations,
  network sources, supported architectures, cleanup, and external-runtime
  behavior.

## [0.3.0] - 2026-07-23

### Added

- Plugin-level process management that keeps a run alive when its console view
  is closed and restores the active context when the view is reopened.
- Inline three-step setup guidance with constrained backend and `wd` Conda
  detection plus offline config, environment, and provider diagnostics.
- First paid-run disclosure and an explicit confirmation before every forced
  state reset.
- Compact paper summary cards for narrow Obsidian sidebars.
- A documented, machine-readable snapshot of optional companion Obsidian
  plugins tested in the PaperBrain development vault.

### Changed

- Simplified the primary settings to runtime status, backend directory, `wd`
  Python, and default provider; specialist overrides now live under Advanced.
- Replaced fixed status colors and very small uppercase text with Obsidian theme
  variables, readable type, keyboard-accessible tabs, and reduced-motion rules.
- Made state, history, and brief reads asynchronous, prevented overlapping
  polls, and skipped unchanged state files by timestamp and size.

### Fixed

- Closing the console no longer terminates a background run.
- Runs that finish without an open console retain their final result and issue
  a concise Obsidian notice.
- Poll-driven refreshes retain the active panel, input focus, and scroll
  position.

## [0.2.0] - 2026-07-22

### Added

- Standalone plugin repository with reproducible builds, tests, and automated
  GitHub Release assets.
- Support for an installed `paperbrain` command as well as a local Python
  backend checkout.
- Separate backend and Obsidian vault path settings with configuration checks.
- Explicit documentation of the backend, network, privacy, cost, process, and
  file-access requirements.

### Changed

- Removed developer-machine paths and detected the active desktop vault by
  default.
- Made local calendar dates independent of UTC conversion.
- Made child-process cancellation, shutdown, output handling, and exit status
  reporting deterministic.

### Security

- Non-zero exits, invalid JSON results, and backend `ok: false` payloads are no
  longer presented as successful runs.
- Backend command, exit-code, and compatibility metadata are validated before
  a result can be presented as successful.
- Clipboard diagnostics redact configured paths and common credential patterns
  and use an explicit privacy-aware action label.
- Cancellation timers are bound to one process, and plugin shutdown terminates
  every child process owned by the plugin.

[Unreleased]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.6.1...HEAD
[0.6.1]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.5.1...0.6.0
[0.5.1]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.7...0.5.0
[0.4.7]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.6...0.4.7
[0.4.6]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.5...0.4.6
[0.4.5]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.4...0.4.5
[0.4.4]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.3...0.4.4
[0.4.3]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/DannyWANGD/obsidian-paperbrain/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/DannyWANGD/obsidian-paperbrain/releases/tag/0.2.0
