# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please open an issue or contact the maintainer directly. We appreciate your help in making this project safer.

## Privacy & Data Usage

**Important:** This tool processes academic papers and generates content using third-party AI services.

1.  **Data Transmission**:
    *   **ArXiv / Hugging Face**: Search queries and paper metadata are sent to these services.
    *   **LLM Providers (OpenAI, Anthropic, Doubao, etc.)**: Paper titles, abstracts, and full PDF text are sent to the configured AI provider for analysis.
    *   **Text-to-Speech (Microsoft Edge)**: Generated podcast scripts are sent to Microsoft's servers for audio synthesis.

2.  **Local Data**:
    *   API Keys are stored locally in `.env` and are **never** uploaded to this repository.
    *   Downloaded PDFs and generated Markdown notes are stored locally in your Obsidian vault.

## Configuration Security

*   **API Keys**: Never commit your `.env` file or `config.yaml` with real keys to version control. The `.gitignore` file is configured to exclude these by default.
*   **Path Traversal**: The tool sanitizes filenames to prevent overwriting critical system files, but you should verify the `output` directory permissions.

## Dependency Management

This project relies on several open-source libraries (`requests`, `arxiv`, `openai`, `edge-tts`). We recommend regularly updating dependencies to patch known vulnerabilities:

```bash
pip install --upgrade -r requirements.txt
```
