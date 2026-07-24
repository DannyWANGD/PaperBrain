# Contributing

Thank you for improving PaperBrain Console. Keep changes focused on the
Obsidian plugin; the Python pipeline is maintained separately.

## Development

Requirements:

- Node.js 18 or later (Node.js 24 is used in CI)
- npm 10 or later
- Obsidian desktop 1.5.0 or later for manual testing

Install dependencies and run the release checks:

```bash
npm ci
npm run check
```

For manual testing, place or link this repository in a non-critical test vault
at `.obsidian/plugins/paperbrain`, build the plugin, reload Obsidian, and enable
PaperBrain Console. Do not develop against your only copy of a production
vault.

## Pull Requests

- Describe the user-visible behavior and any migration impact.
- Add or update automated tests for changed date, command, payload, or process
  behavior.
- Verify both the installed-command and local-checkout backend modes when the
  launch contract changes.
- Keep generated `main.js`, local settings, logs, and vault content out of the
  commit.
- Confirm that no API keys, paper files, personal notes, or machine-specific
  paths are included.

By contributing, you agree that your contribution is licensed under the MIT
License in this repository.
