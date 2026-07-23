"""Central path resolution for PaperBrain.

All project-relative paths are resolved from the repository root. Vault
subfolders are resolved from the configured Obsidian vault root.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _normalize(path: Path) -> str:
    return str(path.expanduser().resolve())


def _is_source_checkout(repo_root: Path, script_dir: Path | None = None) -> bool:
    script_dir = script_dir or repo_root / "script"
    return (repo_root / "pyproject.toml").is_file() and script_dir.name == "script"


def _relative_base(repo_root: Path, script_dir: Path | None = None) -> Path:
    return repo_root if _is_source_checkout(repo_root, script_dir) else Path.cwd()


@dataclass(frozen=True)
class PaperBrainPaths:
    repo_root: Path
    script_dir: Path
    config_path: Path
    prompts_path: Path
    vault_path: Path
    cache_dir: Path
    pdf_cache_dir: Path
    arxiv_cache_dir: Path
    huggingface_cache_dir: Path
    logs_dir: Path
    diagnostics_dir: Path
    temp_pdf_dir: Path
    daily_digest_dir: Path
    notes_dir: Path
    pdf_dir: Path
    assets_dir: Path
    research_index_dir: Path
    research_brief_dir: Path
    run_records_dir: Path

    @classmethod
    def default(cls, config_path: str | Path | None = None, config: dict | None = None) -> "PaperBrainPaths":
        script_dir = Path(__file__).resolve().parents[1]
        package_root = script_dir.parent
        repo_root = _relative_base(package_root, script_dir)
        config_path = cls.resolve_config_path(config_path, repo_root=package_root, script_dir=script_dir)
        prompts_path = cls.resolve_prompts_path(None, repo_root=package_root, script_dir=script_dir)
        vault_path = cls.resolve_vault_path(config or {}, repo_root=package_root)
        return cls.from_roots(repo_root, script_dir, config_path, prompts_path, vault_path, config or {})

    @classmethod
    def from_config(
        cls,
        config: dict,
        config_path: str | Path | None = None,
        prompts_path: str | Path | None = None,
    ) -> "PaperBrainPaths":
        script_dir = Path(__file__).resolve().parents[1]
        package_root = script_dir.parent
        repo_root = _relative_base(package_root, script_dir)
        config_path = cls.resolve_config_path(config_path, repo_root=package_root, script_dir=script_dir)
        prompts_path = cls.resolve_prompts_path(prompts_path, repo_root=package_root, script_dir=script_dir)
        vault_path = cls.resolve_vault_path(config, repo_root=package_root)
        return cls.from_roots(repo_root, script_dir, config_path, prompts_path, vault_path, config)

    @classmethod
    def from_roots(
        cls,
        repo_root: Path,
        script_dir: Path,
        config_path: Path,
        prompts_path: Path,
        vault_path: Path,
        config: dict,
    ) -> "PaperBrainPaths":
        obsidian = config.get("obsidian", {}) if isinstance(config, dict) else {}
        cache_dir = vault_path / "Cache"
        return cls(
            repo_root=repo_root,
            script_dir=script_dir,
            config_path=config_path,
            prompts_path=prompts_path,
            vault_path=vault_path,
            cache_dir=cache_dir,
            pdf_cache_dir=cache_dir / "pdfs",
            arxiv_cache_dir=cache_dir / "arxiv",
            huggingface_cache_dir=cache_dir / "huggingface",
            logs_dir=cache_dir / "logs",
            diagnostics_dir=cache_dir / "diagnostics",
            temp_pdf_dir=cache_dir / "temp_pdfs",
            daily_digest_dir=vault_path / obsidian.get("daily_digest_folder", "Daily_Papers"),
            notes_dir=vault_path / obsidian.get("detailed_notes_folder", "Research_Notes"),
            pdf_dir=vault_path / obsidian.get("pdf_storage_folder", "PDFs"),
            assets_dir=vault_path / "Assets",
            research_index_dir=vault_path / obsidian.get("research_index_folder", "Research_Index"),
            research_brief_dir=vault_path / obsidian.get("research_brief_folder", "Research_Briefs"),
            run_records_dir=vault_path / "Run_Records",
        )

    @staticmethod
    def resolve_config_path(
        value: str | Path | None = None,
        repo_root: Path | None = None,
        script_dir: Path | None = None,
    ) -> Path:
        script_dir = script_dir or Path(__file__).resolve().parents[1]
        repo_root = repo_root or script_dir.parent
        selected = value or os.getenv("PAPERBRAIN_CONFIG_PATH")
        if selected:
            path = Path(selected).expanduser()
            return path.resolve() if path.is_absolute() else (_relative_base(repo_root, script_dir) / path).resolve()
        preferred = script_dir / "config" / "config.yaml"
        installed_resource = script_dir / "paperbrain_config" / "config.yaml"
        fallback = script_dir / "config.yaml"
        if preferred.exists():
            return preferred.resolve()
        if installed_resource.exists():
            return installed_resource.resolve()
        return fallback.resolve()

    @staticmethod
    def resolve_prompts_path(
        value: str | Path | None,
        repo_root: Path | None = None,
        script_dir: Path | None = None,
    ) -> Path:
        script_dir = script_dir or Path(__file__).resolve().parents[1]
        repo_root = repo_root or script_dir.parent
        if value:
            path = Path(value).expanduser()
            return path.resolve() if path.is_absolute() else (_relative_base(repo_root, script_dir) / path).resolve()
        preferred = script_dir / "config" / "prompts.yaml"
        installed_resource = script_dir / "paperbrain_config" / "prompts.yaml"
        fallback = script_dir / "prompts.yaml"
        if preferred.exists():
            return preferred.resolve()
        if installed_resource.exists():
            return installed_resource.resolve()
        return fallback.resolve()

    @staticmethod
    def resolve_vault_path(config: dict, repo_root: Path | None = None) -> Path:
        repo_root = repo_root or Path(__file__).resolve().parents[2]
        obsidian = config.get("obsidian", {}) if isinstance(config, dict) else {}
        raw = os.getenv("PAPERBRAIN_VAULT_PATH") or obsidian.get("vault_path") or "."
        path = Path(str(raw)).expanduser()
        return path.resolve() if path.is_absolute() else (_relative_base(repo_root) / path).resolve()

    @classmethod
    def from_config_dict(cls, config: dict) -> "PaperBrainPaths":
        existing = (config or {}).get("_paperbrain_paths")
        if isinstance(existing, dict) and existing.get("repo_root"):
            return cls.from_config(
                config,
                config_path=existing.get("config_path"),
                prompts_path=existing.get("prompts_path"),
            )
        return cls.from_config(config)

    def run_id(self, date_key: str, provider: str, single_paper: bool = False) -> str:
        return str(date_key)

    def legacy_run_id(self, date_key: str, provider: str, single_paper: bool = False) -> str:
        suffix = "single" if single_paper else provider
        return f"{date_key}-{suffix}"

    def run_dir(self, date_key: str, provider: str, single_paper: bool = False) -> Path:
        return self.run_records_dir / self.run_id(date_key, provider, single_paper)

    def state_path(self, date_key: str, provider: str, single_paper: bool = False) -> Path:
        return self.run_dir(date_key, provider, single_paper) / "state.json"

    def legacy_state_path(self, date_key: str, provider: str, single_paper: bool = False) -> Path:
        return self.run_records_dir / f"{self.run_id(date_key, provider, single_paper)}-run-state.json"

    def screening_report_path(self, date_key: str, provider: str, single_paper: bool = False) -> Path:
        return self.run_dir(date_key, provider, single_paper) / "screening_report.md"

    def log_summary_path(self, date_key: str, provider: str, single_paper: bool = False) -> Path:
        return self.run_dir(date_key, provider, single_paper) / "log_summary.md"

    def errors_path(self, date_key: str, provider: str, single_paper: bool = False) -> Path:
        return self.run_dir(date_key, provider, single_paper) / "errors.json"

    @property
    def pdf_cooldown_path(self) -> Path:
        return self.pdf_cache_dir / "arxiv_pdf_cooldown.json"

    @property
    def log_path(self) -> Path:
        return self.logs_dir / "paperbrain.log"

    def as_dict(self) -> dict:
        return {
            "repo_root": _normalize(self.repo_root),
            "script_dir": _normalize(self.script_dir),
            "config_path": _normalize(self.config_path),
            "prompts_path": _normalize(self.prompts_path),
            "vault_path": _normalize(self.vault_path),
            "cache_dir": _normalize(self.cache_dir),
            "pdf_cache_dir": _normalize(self.pdf_cache_dir),
            "arxiv_cache_dir": _normalize(self.arxiv_cache_dir),
            "huggingface_cache_dir": _normalize(self.huggingface_cache_dir),
            "logs_dir": _normalize(self.logs_dir),
            "diagnostics_dir": _normalize(self.diagnostics_dir),
            "temp_pdf_dir": _normalize(self.temp_pdf_dir),
            "daily_digest_dir": _normalize(self.daily_digest_dir),
            "notes_dir": _normalize(self.notes_dir),
            "pdf_dir": _normalize(self.pdf_dir),
            "assets_dir": _normalize(self.assets_dir),
            "research_index_dir": _normalize(self.research_index_dir),
            "research_brief_dir": _normalize(self.research_brief_dir),
            "run_records_dir": _normalize(self.run_records_dir),
        }
