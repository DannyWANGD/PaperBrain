# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| 0.4.x | Yes |
| 0.3.x | Yes |
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

Both the in-app installer and the versioned terminal installers execute only
fixed Miniforge and PaperBrain release assets after SHA-256 verification and
explicit user action. The generated terminal command also verifies its
PowerShell or Bash installer asset before execution. Reports involving checksum
validation, installer path ownership, process execution, package sources, or
managed-runtime cleanup are security issues for this plugin.
