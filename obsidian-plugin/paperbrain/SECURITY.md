# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| 0.6.x | Yes |
| 0.5.x | Yes |
| 0.4.x | No |
| 0.3.x | No |
| 0.2.x | No |
| Earlier versions | No |

## Reporting a Vulnerability

Do not open a public issue for a suspected vulnerability or include secrets,
private paper content, vault data, or exploit details in public discussions.

Use GitHub's private vulnerability reporting for this repository:

https://github.com/DannyWANGD/obsidian-paperbrain/security/advisories/new

Include the affected plugin and backend versions, operating system, impact,
reproduction steps, and a minimal proof of concept with private data removed.
The maintainer aims to acknowledge a report within seven days and will publish
remediation guidance after a fix is available.

Issues in the Python PaperBrain backend should be reported privately to that
project rather than in this plugin repository.

The Console updater, in-app backend installer, and versioned terminal installers
use expected GitHub Release assets after SHA-256 verification and explicit user
action. Console updates replace only `main.js`, `manifest.json`, and
`styles.css`; failed replacements are rolled back. The generated terminal
command also verifies its PowerShell or Bash installer before execution.
Reports involving update or checksum validation, installer path ownership,
process execution, package sources, or managed-runtime cleanup are security
issues for this plugin.
