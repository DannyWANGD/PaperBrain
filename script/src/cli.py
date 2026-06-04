"""Unified command line interface for PaperBrain."""

from __future__ import annotations

import argparse
import compileall
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import traceback
import unittest
from importlib import metadata
from datetime import datetime, timedelta
from enum import IntEnum
from pathlib import Path
from urllib.parse import urlparse

from src.config_loader import load_config, load_prompts
from src.paths import PaperBrainPaths


REQUIRED_DEPENDENCIES = {
    "feedparser": "feedparser",
    "arxiv": "arxiv",
    "requests": "requests",
    "yaml": "pyyaml",
    "schedule": "schedule",
    "tqdm": "tqdm",
    "bs4": "beautifulsoup4",
    "pypdf": "pypdf",
    "fitz": "pymupdf",
    "openai": "openai",
    "edge_tts": "edge-tts",
    "nest_asyncio": "nest_asyncio",
    "dotenv": "python-dotenv",
}


class ExitCode(IntEnum):
    OK = 0
    CONFIG_ERROR = 2
    NETWORK_UNAVAILABLE = 3
    LLM_FAILURE = 4
    PDF_UNAVAILABLE = 5
    WRITE_FAILURE = 6
    VALIDATION_FAILED = 7
    UNEXPECTED_ERROR = 70


PIPELINE_COMMANDS = {"run", "fetch", "screen", "deep"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="paperbrain",
        description="PaperBrain local research pipeline CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full daily or single-paper pipeline.")
    _add_pipeline_args(run_parser)
    run_parser.add_argument(
        "--stop-after",
        choices=["fetch", "coarse", "screen", "deep"],
        help="Stop after a pipeline stage; useful for checkpointed runs.",
    )
    run_parser.add_argument("--schedule", action="store_true", help="Run daily using schedule.time from config.yaml.")

    for command, help_text in (
        ("fetch", "Fetch papers and persist run state."),
        ("screen", "Fetch and screen papers, then stop before deep analysis."),
        ("deep", "Fetch, screen, and deep-analyze selected papers, then stop before digest/podcast."),
    ):
        sub = subparsers.add_parser(command, help=help_text)
        _add_pipeline_args(sub)

    index_parser = subparsers.add_parser("index", help="Rebuild the Obsidian research index.")
    index_parser.add_argument(
        "--no-update-notes",
        action="store_true",
        help="Only regenerate index files; do not rewrite note frontmatter.",
    )

    doctor_parser = subparsers.add_parser("doctor", help="Run local diagnostics.")
    doctor_subparsers = doctor_parser.add_subparsers(dest="doctor_command")
    doctor_subparsers.add_parser("config", help="Check YAML, required fields, models, thresholds, and configured paths.")
    doctor_subparsers.add_parser("env", help="Check Python, dependencies, API keys, writable directories, and proxies.")
    arxiv_parser = doctor_subparsers.add_parser("arxiv", help="Check arXiv endpoints, cache, cooldown, and PDF settings.")
    arxiv_parser.add_argument("--live", action="store_true", help="Also perform a small live arXiv request.")
    llm_parser = doctor_subparsers.add_parser("llm", help="Check provider keys, model names, and fallback chains.")
    llm_parser.add_argument("--provider", choices=["doubao", "openrouter"], help="Limit checks to one provider.")
    llm_parser.add_argument("--live", action="store_true", help="Also send a low-cost live LLM probe.")
    doctor_subparsers.add_parser("obsidian", help="Check vault folders and Obsidian output paths.")

    check_parser = subparsers.add_parser("check", help="Run local validation checks.")
    check_parser.add_argument("--skip-tests", action="store_true", help="Compile and import only; skip unit tests.")
    check_parser.add_argument("--skip-lint", action="store_true", help="Skip optional Ruff lint/format checks.")
    check_parser.add_argument("--strict-lint", action="store_true", help="Fail when Ruff is missing or reports issues.")

    return parser


def _add_pipeline_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--date", type=_date_arg, help="Target date in YYYY-MM-DD format; default is yesterday.")
    parser.add_argument(
        "--provider",
        default="doubao",
        choices=["doubao", "openrouter"],
        help="AI provider.",
    )
    parser.add_argument("--arxiv-url", help="Analyze a specific arXiv URL or ID directly.")
    parser.add_argument("--no-podcast", action="store_true", help="Disable podcast generation.")
    parser.add_argument("--podcast-minutes", type=int, default=5, help="Target podcast duration in minutes.")
    parser.add_argument(
        "--resume",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Resume from saved run state when available.",
    )
    parser.add_argument("--force", action="store_true", help="Reset saved run state and recompute all stages.")


def _date_arg(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def legacy_main_args(argv: list[str]) -> list[str]:
    """Translate the old script/main.py arguments to the unified CLI shape."""
    args = list(argv)
    if "--run-now" in args:
        args.remove("--run-now")
        return ["run"] + args
    return ["run", "--schedule"] + args


def main(argv: list[str] | None = None, pipeline_module=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    started = time.monotonic()
    try:
        if args.command in PIPELINE_COMMANDS:
            payload = _run_pipeline(args, pipeline_module=pipeline_module)
        elif args.command == "index":
            payload = _run_index(args)
        elif args.command == "doctor":
            payload = _run_doctor(args)
        elif args.command == "check":
            payload = _run_check(args)
        else:
            parser.error(f"unknown command: {args.command}")

        if payload.get("ok") is False:
            exit_code = ExitCode.VALIDATION_FAILED if args.command == "check" else ExitCode.CONFIG_ERROR
            payload.setdefault("command", args.command)
            payload["elapsed_ms"] = int((time.monotonic() - started) * 1000)
            payload["exit_code"] = int(exit_code)
            _emit_json(payload)
            return int(exit_code)

        payload.setdefault("ok", True)
        payload.setdefault("command", args.command)
        payload["elapsed_ms"] = int((time.monotonic() - started) * 1000)
        payload["exit_code"] = int(ExitCode.OK)
        _emit_json(payload)
        return int(ExitCode.OK)
    except Exception as exc:
        exit_code = _classify_exception(exc)
        payload = {
            "ok": False,
            "command": getattr(args, "command", ""),
            "exit_code": int(exit_code),
            "error": {
                "code": exit_code.name.lower(),
                "message": str(exc),
                "suggestion": _suggestion_for_exit_code(exit_code),
                "exception": exc.__class__.__name__,
                "retryable": exit_code in (ExitCode.NETWORK_UNAVAILABLE, ExitCode.LLM_FAILURE, ExitCode.PDF_UNAVAILABLE),
            },
            "elapsed_ms": int((time.monotonic() - started) * 1000),
        }
        _record_run_error_if_possible(args, payload["error"])
        print(f"[ERR] {payload['error']['message']}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        _emit_json(payload)
        return int(exit_code)


def _pipeline_module(pipeline_module=None):
    if pipeline_module is not None:
        return pipeline_module
    paths = PaperBrainPaths.default()
    script_dir = str(paths.script_dir)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    return importlib.import_module("main")


def _run_pipeline(args, pipeline_module=None) -> dict:
    if getattr(args, "schedule", False):
        return _run_schedule(args, pipeline_module=pipeline_module)

    stop_after = getattr(args, "stop_after", None)
    if args.command == "fetch":
        stop_after = "fetch"
    elif args.command == "screen":
        stop_after = "screen"
    elif args.command == "deep":
        stop_after = "deep"

    pipeline = _pipeline_module(pipeline_module)
    result = pipeline.job(
        target_date=args.date,
        provider=args.provider,
        generate_podcast=not args.no_podcast,
        podcast_minutes=max(1, args.podcast_minutes),
        arxiv_url=args.arxiv_url,
        resume=args.resume,
        force=args.force,
        stop_after=stop_after,
    )
    if isinstance(result, dict):
        result = dict(result)
    else:
        result = {"ok": True}
    result["command"] = args.command
    result["stop_after"] = stop_after
    return result


def _run_schedule(args, pipeline_module=None) -> dict:
    pipeline = _pipeline_module(pipeline_module)
    config = load_config()
    try:
        import schedule
    except ImportError as exc:
        raise RuntimeError("The 'schedule' package is required for scheduled mode.") from exc

    schedule_time = config["schedule"].get("time", "08:00")

    def scheduled_job():
        pipeline.job(
            target_date=None,
            provider=args.provider,
            generate_podcast=not args.no_podcast,
            podcast_minutes=max(1, args.podcast_minutes),
            arxiv_url=args.arxiv_url,
            resume=args.resume,
            force=args.force,
            stop_after=getattr(args, "stop_after", None),
        )

    schedule.every().day.at(schedule_time).do(scheduled_job)
    _emit_json(
        {
            "ok": True,
            "command": args.command,
            "mode": "schedule",
            "schedule_time": schedule_time,
            "exit_code": int(ExitCode.OK),
        }
    )
    while True:
        schedule.run_pending()
        time.sleep(60)


def _run_index(args) -> dict:
    config = load_config()
    from src.research_indexer import ResearchIndexer

    indexer = ResearchIndexer(config)
    notes = indexer.build(update_notes=not args.no_update_notes)
    paths = PaperBrainPaths.from_config_dict(config)
    return {
        "ok": True,
        "command": "index",
        "notes_indexed": len(notes),
        "artifacts": {"research_index": str(paths.research_index_dir)},
    }


def _run_doctor(args) -> dict:
    config = load_config()
    prompts = load_prompts()
    paths = PaperBrainPaths.from_config_dict(config)

    scope = getattr(args, "doctor_command", None) or "all"
    sections = []
    if scope in ("all", "config"):
        sections.append(_doctor_config(config, prompts, paths))
    if scope in ("all", "env"):
        sections.append(_doctor_env(config, paths))
    if scope in ("all", "arxiv"):
        sections.append(_doctor_arxiv(config, paths, live=bool(getattr(args, "live", False))))
    if scope in ("all", "llm"):
        sections.append(
            _doctor_llm(
                config,
                provider=getattr(args, "provider", None),
                live=bool(getattr(args, "live", False)),
            )
        )
    if scope in ("all", "obsidian"):
        sections.append(_doctor_obsidian(paths))

    checks = [check for section in sections for check in section["checks"]]
    ok = all(check["ok"] for check in checks if check["severity"] == "error")
    payload = {
        "ok": ok,
        "command": "doctor",
        "scope": scope,
        "paths": paths.as_dict(),
        "prompts_loaded": bool(prompts),
        "sections": sections,
        "checks": checks,
    }
    latest = _write_diagnostics(paths, payload, scope=scope)
    payload["artifacts"] = {"diagnostics": str(latest)}
    return payload


def _doctor_config(config: dict, prompts: dict, paths: PaperBrainPaths) -> dict:
    checks = [
        _path_check("config_file", paths.config_path, must_exist=True, category="config"),
        _check("prompts_loaded", bool(prompts), "error", "prompts.yaml loaded", "Check script/config/prompts.yaml.", "config"),
    ]

    for section in ("doubao", "openrouter", "analysis", "obsidian", "search", "schedule"):
        checks.append(
            _check(
                f"config_section_{section}",
                isinstance(config.get(section), dict),
                "error",
                f"config section `{section}` exists",
                f"Add `{section}` to script/config/config.yaml.",
                "config",
            )
        )

    obsidian = config.get("obsidian", {})
    for key in ("vault_path", "daily_digest_folder", "detailed_notes_folder", "research_index_folder", "pdf_storage_folder"):
        checks.append(
            _check(
                f"obsidian_{key}",
                bool(obsidian.get(key)),
                "error",
                f"obsidian.{key} is configured",
                f"Set obsidian.{key} in config.yaml.",
                "config",
            )
        )

    search = config.get("search", {})
    checks.append(
        _check(
            "search_keywords",
            bool(search.get("keywords")),
            "error",
            "search.keywords contains at least one keyword",
            "Add focused research keywords to config.yaml.",
            "config",
        )
    )
    checks.append(
        _check(
            "search_categories",
            bool(search.get("arxiv_categories")),
            "error",
            "search.arxiv_categories contains at least one category",
            "Add arXiv categories such as cs.RO or cs.AI.",
            "config",
        )
    )

    analysis = config.get("analysis", {})
    lower = _float_value(analysis.get("deep_analysis_lower_threshold"))
    extra = _float_value(analysis.get("deep_analysis_extra_threshold"))
    checks.append(
        _check(
            "analysis_threshold_order",
            lower is not None and extra is not None and lower <= extra,
            "error",
            "deep analysis thresholds are ordered",
            "Ensure deep_analysis_lower_threshold <= deep_analysis_extra_threshold.",
            "config",
            {"lower": lower, "extra": extra},
        )
    )
    checks.append(
        _check(
            "analysis_stage2_ratio",
            0 < (_float_value(analysis.get("screening_second_stage_ratio")) or 0) <= 1,
            "error",
            "screening_second_stage_ratio is in (0, 1]",
            "Set screening_second_stage_ratio to a conservative fraction such as 0.25.",
            "config",
        )
    )

    for provider in ("doubao", "openrouter"):
        checks.extend(_provider_model_checks(provider, config))

    return _section("config", checks)


def _doctor_env(config: dict, paths: PaperBrainPaths) -> dict:
    version = sys.version_info
    checks = [
        _check(
            "python_version",
            version >= (3, 9),
            "error",
            f"Python {platform.python_version()} is running",
            "Use the wd environment with Python 3.9 or newer; Python 3.10 is still recommended.",
            "env",
            {"executable": sys.executable},
        )
    ]
    checks.extend(_dependency_checks(severity="error", category="env"))
    checks.extend([_provider_check("doubao", config, category="env"), _provider_check("openrouter", config, category="env")])
    for name, path in (
        ("cache", paths.cache_dir),
        ("diagnostics", paths.diagnostics_dir),
        ("run_records", paths.run_records_dir),
        ("research_notes", paths.notes_dir),
        ("pdfs", paths.pdf_dir),
        ("research_index", paths.research_index_dir),
    ):
        checks.append(_writable_dir_check(name, path, category="env"))

    proxy_vars = {key: os.getenv(key, "") for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY")}
    checks.append(
        _check(
            "proxy_environment",
            True,
            "info",
            "proxy environment inspected",
            "",
            "env",
            {key: bool(value) for key, value in proxy_vars.items()},
        )
    )
    return _section("env", checks)


def _doctor_arxiv(config: dict, paths: PaperBrainPaths, live=False) -> dict:
    search = config.get("search", {})
    endpoints = search.get("arxiv_api_endpoints") or []
    checks = [
        _check(
            "arxiv_endpoint_count",
            len(endpoints) >= 1,
            "error",
            f"{len(endpoints)} arXiv endpoint(s) configured",
            "Configure at least one arXiv API endpoint.",
            "arxiv",
        ),
        _check(
            "arxiv_endpoint_fallback",
            len(endpoints) >= 2,
            "warning",
            "multiple arXiv endpoints configured for fallback",
            "Add export.arxiv.org and arxiv.org API endpoints for fallback.",
            "arxiv",
        ),
        _check(
            "arxiv_timeout",
            (_float_value(search.get("arxiv_timeout_seconds")) or 0) > 0,
            "error",
            "arXiv timeout is positive",
            "Set search.arxiv_timeout_seconds to a positive value.",
            "arxiv",
        ),
        _check(
            "arxiv_attempts",
            int(search.get("arxiv_max_attempts", 0) or 0) >= 1,
            "error",
            "arXiv max attempts is at least 1",
            "Set search.arxiv_max_attempts >= 1.",
            "arxiv",
        ),
        _writable_dir_check("arxiv_cache", paths.arxiv_cache_dir, category="arxiv"),
        _writable_dir_check("pdf_cache", paths.pdf_cache_dir, category="arxiv"),
        _cooldown_check("arxiv_api_cooldown", paths.arxiv_cache_dir / "rate_limit_cooldown.json", category="arxiv"),
        _cooldown_check("arxiv_pdf_cooldown", paths.pdf_cooldown_path, category="arxiv"),
    ]
    for index, endpoint in enumerate(endpoints):
        parsed = urlparse(str(endpoint))
        checks.append(
            _check(
                f"arxiv_endpoint_{index + 1}",
                parsed.scheme in ("http", "https") and bool(parsed.netloc),
                "error",
                f"arXiv endpoint is a valid URL: {endpoint}",
                "Use a full http(s) URL.",
                "arxiv",
            )
        )

    checks.append(
        _check(
            "arxiv_abs_fallback",
            True,
            "info",
            "single-paper arXiv abs-page fallback is available in PaperScraper",
            "",
            "arxiv",
        )
    )
    if live:
        checks.append(_live_arxiv_check(config))
        checks.append(_live_arxiv_pdf_check())
    else:
        checks.append(_check("arxiv_live_probe", True, "info", "live arXiv probe skipped", "Run `paperbrain doctor arxiv --live` for a network probe.", "arxiv"))
        checks.append(_check("arxiv_pdf_live_probe", True, "info", "live arXiv PDF probe skipped", "Run `paperbrain doctor arxiv --live` to verify PDF download.", "arxiv"))
    return _section("arxiv", checks)


def _doctor_llm(config: dict, provider=None, live=False) -> dict:
    providers = [provider] if provider else ["doubao", "openrouter"]
    checks = []
    for item in providers:
        checks.append(_provider_check(item, config, category="llm"))
        checks.extend(_provider_model_checks(item, config, category="llm"))
        if live:
            checks.append(_live_llm_check(item, config))
        else:
            checks.append(
                _check(
                    f"{item}_live_probe",
                    True,
                    "info",
                    f"{item} live LLM probe skipped",
                    f"Run `paperbrain doctor llm --provider {item} --live` for a low-cost live probe.",
                    "llm",
                )
            )
    return _section("llm", checks)


def _doctor_obsidian(paths: PaperBrainPaths) -> dict:
    checks = [
        _path_check("vault", paths.vault_path, must_exist=True, category="obsidian"),
        _writable_dir_check("daily_digest", paths.daily_digest_dir, category="obsidian"),
        _writable_dir_check("research_notes", paths.notes_dir, category="obsidian"),
        _writable_dir_check("pdfs", paths.pdf_dir, category="obsidian"),
        _writable_dir_check("assets", paths.assets_dir, category="obsidian"),
        _writable_dir_check("research_index", paths.research_index_dir, category="obsidian"),
        _writable_dir_check("research_briefs", paths.research_brief_dir, category="obsidian"),
    ]
    base_file = paths.research_index_dir / "Paper_Library.base"
    checks.append(
        _check(
            "obsidian_base_file",
            base_file.exists(),
            "warning",
            "Paper_Library.base exists",
            "Run `paperbrain index` to rebuild Obsidian index files.",
            "obsidian",
            {"path": str(base_file)},
        )
    )
    return _section("obsidian", checks)


def _run_check(args) -> dict:
    paths = PaperBrainPaths.default()
    script_dir = str(paths.script_dir)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    config = load_config()
    prompts = load_prompts()
    paths = PaperBrainPaths.from_config_dict(config)
    path_checks = [
        _writable_dir_check("cache", paths.cache_dir, category="check"),
        _writable_dir_check("run_records", paths.run_records_dir, category="check"),
        _writable_dir_check("research_notes", paths.notes_dir, category="check"),
        _writable_dir_check("pdfs", paths.pdf_dir, category="check"),
        _writable_dir_check("research_index", paths.research_index_dir, category="check"),
    ]
    missing_dependencies = [check for check in _dependency_checks(severity="error") if not check["ok"]]
    compile_ok = compileall.compile_dir(script_dir, quiet=1)
    import_ok = False if missing_dependencies else _import_core_modules()
    lint = _run_ruff_checks(paths, skip=args.skip_lint, strict=args.strict_lint)
    tests_ok = True
    tests_run = 0
    failures = 0
    errors = 0
    if not args.skip_tests:
        loader = unittest.TestLoader()
        suite = loader.discover(str(paths.script_dir / "tests"), pattern="test_*.py")
        runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=1)
        result = runner.run(suite)
        tests_ok = result.wasSuccessful()
        tests_run = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)

    paths_ok = all(check["ok"] for check in path_checks if check["severity"] == "error")
    ok = bool(
        compile_ok
        and import_ok
        and bool(prompts)
        and paths_ok
        and tests_ok
        and lint["ok"]
        and not missing_dependencies
    )
    payload = {
        "ok": ok,
        "command": "check",
        "config_ok": True,
        "prompts_ok": bool(prompts),
        "path_checks": path_checks,
        "compile_ok": bool(compile_ok),
        "import_ok": bool(import_ok),
        "lint": lint,
        "missing_dependencies": missing_dependencies,
        "tests_ok": bool(tests_ok),
        "tests_run": tests_run,
        "failures": failures,
        "errors": errors,
    }
    return payload


def _import_core_modules() -> bool:
    modules = [
        "src.config_loader",
        "src.paths",
        "src.paper_identity",
        "src.run_state",
        "src.scraper",
        "src.analyser",
        "src.obsidian_writer",
        "src.research_indexer",
    ]
    for module in modules:
        importlib.import_module(module)
    return True


def _section(name: str, checks: list[dict]) -> dict:
    return {
        "name": name,
        "ok": all(check["ok"] for check in checks if check["severity"] == "error"),
        "checks": checks,
    }


def _check(name: str, ok: bool, severity: str, message: str, suggestion: str = "", category: str = "", data=None) -> dict:
    payload = {
        "name": name,
        "ok": bool(ok),
        "severity": severity,
        "category": category,
        "message": message if ok else f"{message} failed",
        "suggestion": suggestion if (not ok or severity == "info") else "",
    }
    if data is not None:
        payload["data"] = data
    return payload


def _float_value(value):
    try:
        return float(value)
    except Exception:
        return None


def _provider_model_checks(provider: str, config: dict, category: str = "config") -> list[dict]:
    cfg = config.get(provider, {})
    required = ["model_flash", "model_pro"]
    if provider == "openrouter":
        required.extend(["model_screening_pro", "model_podcast", "model_vision"])

    checks = []
    for key in required:
        checks.append(
            _check(
                f"{provider}_{key}",
                bool(cfg.get(key)),
                "error",
                f"{provider}.{key} is configured",
                f"Set {provider}.{key} in config.yaml.",
                category,
            )
        )

    for key in ("model_flash_fallbacks", "model_screening_pro_fallbacks", "model_pro_fallbacks", "model_podcast_fallbacks", "model_vision_fallbacks"):
        if key in cfg:
            checks.append(
                _check(
                    f"{provider}_{key}",
                    isinstance(cfg.get(key), list),
                    "warning",
                    f"{provider}.{key} is a list",
                    f"Make {provider}.{key} a YAML list of model IDs.",
                    category,
                )
            )
    return checks


def _writable_dir_check(name: str, path: Path, category: str) -> dict:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".paperbrain_write_test.tmp"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return _check(name, True, "error", f"{name} directory is writable", "", category, {"path": str(path)})
    except Exception as exc:
        return _check(
            name,
            False,
            "error",
            f"{name} directory is writable",
            "Check filesystem permissions and configured vault/cache paths.",
            category,
            {"path": str(path), "exception": f"{exc.__class__.__name__}: {exc}"},
        )


def _cooldown_check(name: str, path: Path, category: str) -> dict:
    if not path.exists():
        return _check(name, True, "info", f"{name} is not active", "", category, {"path": str(path), "active": False})
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        until_ts = float(data.get("until", 0) or 0)
        remaining = max(0.0, until_ts - time.time())
        return _check(
            name,
            True,
            "warning" if remaining > 0 else "info",
            f"{name} cooldown file is readable",
            "Wait for cooldown to expire before retrying live requests." if remaining > 0 else "",
            category,
            {"path": str(path), "active": remaining > 0, "remaining_seconds": remaining, "reason": data.get("reason", "")},
        )
    except Exception as exc:
        return _check(
            name,
            False,
            "warning",
            f"{name} cooldown file is readable",
            "Delete or repair the cooldown JSON file if it is corrupt.",
            category,
            {"path": str(path), "exception": f"{exc.__class__.__name__}: {exc}"},
        )


def _live_arxiv_check(config: dict) -> dict:
    try:
        import requests

        search = config.get("search", {})
        endpoints = search.get("arxiv_api_endpoints") or ["https://export.arxiv.org/api/query"]
        endpoint = endpoints[0]
        response = requests.get(
            endpoint,
            params={"search_query": "id:2605.25802", "start": 0, "max_results": 1},
            headers={"User-Agent": config.get("arxiv_user_agent", "PaperBrain/1.0 doctor")},
            timeout=min(float(search.get("arxiv_timeout_seconds", 10) or 10), 15.0),
        )
        ok = response.status_code == 200 and "<feed" in response.text[:1000].lower()
        return _check(
            "arxiv_live_probe",
            ok,
            "error",
            f"live arXiv probe returned HTTP {response.status_code}",
            "Check network/proxy settings or wait if arXiv is rate limited.",
            "arxiv",
            {"endpoint": endpoint, "status_code": response.status_code},
        )
    except Exception as exc:
        return _check(
            "arxiv_live_probe",
            False,
            "error",
            "live arXiv probe completed",
            "Check network/proxy settings or retry without --live.",
            "arxiv",
            {"exception": f"{exc.__class__.__name__}: {exc}"},
        )


def _live_arxiv_pdf_check() -> dict:
    url = "https://arxiv.org/pdf/2605.25802.pdf"
    try:
        import requests

        response = requests.get(
            url,
            headers={"User-Agent": "PaperBrain/1.0 doctor", "Accept": "application/pdf"},
            stream=True,
            timeout=30,
        )
        first_chunk = next(response.iter_content(chunk_size=1024), b"") if response.status_code == 200 else b""
        ok = response.status_code == 200 and b"%PDF-" in first_chunk
        response.close()
        return _check(
            "arxiv_pdf_live_probe",
            ok,
            "error",
            f"live arXiv PDF probe returned HTTP {response.status_code}",
            "Check arXiv PDF reachability, rate limits, or local proxy settings.",
            "arxiv",
            {"url": url, "status_code": response.status_code},
        )
    except Exception as exc:
        return _check(
            "arxiv_pdf_live_probe",
            False,
            "error",
            "live arXiv PDF probe completed",
            "Check arXiv PDF reachability, rate limits, or retry without --live.",
            "arxiv",
            {"url": url, "exception": f"{exc.__class__.__name__}: {exc}"},
        )


def _live_llm_check(provider: str, config: dict) -> dict:
    cfg = config.get(provider, {})
    api_key = str(cfg.get("api_key") or "")
    model = cfg.get("model_flash") or cfg.get("model_pro")
    if not api_key or api_key.startswith("${") or not model:
        return _check(
            f"{provider}_live_probe",
            False,
            "error",
            f"{provider} live probe has API key and model",
            f"Configure {provider}.api_key and a flash/pro model before live probing.",
            "llm",
        )
    try:
        if provider == "openrouter":
            import requests

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": "Reply with OK."}],
                    "max_tokens": 5,
                },
                timeout=30,
            )
            ok = response.status_code == 200
            return _check(
                "openrouter_live_probe",
                ok,
                "error",
                f"OpenRouter live probe returned HTTP {response.status_code}",
                "Check OPENROUTER_API_KEY, model availability, and network/proxy settings.",
                "llm",
                {"model": model, "status_code": response.status_code},
            )

        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url="https://ark.cn-beijing.volces.com/api/v3")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with OK."}],
            max_tokens=5,
        )
        ok = bool(response.choices)
        return _check(
            "doubao_live_probe",
            ok,
            "error",
            "Doubao live probe returned a completion",
            "Check DOUBAO_API_KEY, endpoint availability, and model deployment name.",
            "llm",
            {"model": model},
        )
    except Exception as exc:
        return _check(
            f"{provider}_live_probe",
            False,
            "error",
            f"{provider} live probe completed",
            f"Check {provider} API key, model, and network/proxy settings.",
            "llm",
            {"model": model, "exception": f"{exc.__class__.__name__}: {exc}"},
        )


def _write_diagnostics(paths: PaperBrainPaths, payload: dict, scope: str) -> Path:
    paths.diagnostics_dir.mkdir(parents=True, exist_ok=True)
    payload["written_at"] = datetime.now().isoformat(timespec="seconds")
    latest = paths.diagnostics_dir / "latest.json"
    latest.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    scoped = paths.diagnostics_dir / f"{scope}.json"
    scoped.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return latest


def _path_check(name: str, path: Path, must_exist: bool, category: str = "") -> dict:
    exists = path.exists()
    ok = exists or not must_exist
    parent = path if exists and path.is_dir() else path.parent
    writable = parent.exists() and os.access(parent, os.W_OK)
    if not ok:
        message = f"{name} path does not exist: {path}"
    elif not writable:
        message = f"{name} parent is not writable: {parent}"
        ok = False
    else:
        message = f"{name} path is usable"
    return {
        "name": name,
        "ok": ok,
        "severity": "error" if must_exist else "warning",
        "category": category,
        "path": str(path),
        "message": message,
        "suggestion": "Create or correct this path in config.yaml." if not ok else "",
    }


def _provider_check(provider: str, config: dict, category: str = "") -> dict:
    cfg = config.get(provider, {})
    key = str(cfg.get("api_key") or "")
    ok = bool(key and not key.startswith("${"))
    return {
        "name": f"{provider}_api_key",
        "ok": ok,
        "severity": "warning",
        "category": category,
        "message": "API key is configured" if ok else f"{provider} API key is missing or still unresolved",
        "suggestion": "" if ok else f"Set {provider.upper()}_API_KEY in script/.env or script/config/.env.",
    }


def _dependency_checks(severity: str, category: str = "") -> list[dict]:
    import importlib.util

    checks = []
    for module, package in REQUIRED_DEPENDENCIES.items():
        ok = importlib.util.find_spec(module) is not None
        version = ""
        if ok:
            try:
                version = metadata.version(package)
            except Exception:
                version = "unknown"
        checks.append(
            {
                "name": f"dependency_{package}",
                "package": package,
                "module": module,
                "ok": ok,
                "severity": severity,
                "category": category,
                "message": f"{package} is importable" if ok else f"{package} is not installed in this Python environment",
                "suggestion": f"Install dependencies with `pip install -r script/requirements.txt`." if not ok else "",
                "version": version,
            }
        )
    return checks


def _run_ruff_checks(paths: PaperBrainPaths, skip=False, strict=False) -> dict:
    if skip:
        return {"ok": True, "status": "skipped", "strict": strict, "commands": []}

    ruff = shutil.which("ruff")
    if not ruff:
        return {
            "ok": not strict,
            "status": "missing",
            "strict": strict,
            "commands": [],
            "message": "Ruff is not installed in this Python environment.",
            "suggestion": "Install dev tooling with `pip install ruff pre-commit`, or run without --strict-lint.",
        }

    commands = [
        [ruff, "check", "script"],
        [ruff, "format", "--check", "script"],
    ]
    results = []
    all_ok = True
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=str(paths.repo_root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        command_ok = completed.returncode == 0
        all_ok = all_ok and command_ok
        results.append(
            {
                "command": " ".join(command),
                "returncode": completed.returncode,
                "ok": command_ok,
                "stdout": completed.stdout[-4000:],
                "stderr": completed.stderr[-4000:],
            }
        )
    return {
        "ok": all_ok or not strict,
        "status": "passed" if all_ok else "failed",
        "strict": strict,
        "commands": results,
        "message": "Ruff checks passed" if all_ok else "Ruff reported issues",
    }


def _record_run_error_if_possible(args, error: dict) -> None:
    if getattr(args, "command", "") not in PIPELINE_COMMANDS:
        return
    try:
        config = load_config()
        from src.run_state import RunState

        target_date = getattr(args, "date", None) or (datetime.now().date() - timedelta(days=1))
        state = RunState(config, target_date, getattr(args, "provider", "doubao"), single_paper=bool(getattr(args, "arxiv_url", "")))
        state.add_error(
            error.get("code", "unexpected_error"),
            error.get("message", "PaperBrain command failed."),
            suggestion=error.get("suggestion", ""),
            exception=error.get("exception", ""),
            retryable=error.get("retryable", False),
        )
        state.mark_stage("failed")
    except Exception:
        return


def _classify_exception(exc: Exception) -> ExitCode:
    text = f"{exc.__class__.__name__}: {exc}".lower()
    if isinstance(exc, ModuleNotFoundError) or "validation" in text or "checks failed" in text:
        return ExitCode.VALIDATION_FAILED
    if isinstance(exc, (KeyError, ValueError)) or "config" in text or "yaml" in text:
        return ExitCode.CONFIG_ERROR
    if isinstance(exc, (PermissionError, OSError)) and ("permission" in text or "access" in text or "write" in text):
        return ExitCode.WRITE_FAILURE
    if "connect" in text or "timeout" in text or "network" in text or "rate limit" in text:
        return ExitCode.NETWORK_UNAVAILABLE
    if "pdf" in text:
        return ExitCode.PDF_UNAVAILABLE
    if "llm" in text or "openrouter" in text or "doubao" in text or "api" in text:
        return ExitCode.LLM_FAILURE
    return ExitCode.UNEXPECTED_ERROR


def _suggestion_for_exit_code(exit_code: ExitCode) -> str:
    suggestions = {
        ExitCode.CONFIG_ERROR: "Run `paperbrain doctor` and check script/config/config.yaml plus .env values.",
        ExitCode.NETWORK_UNAVAILABLE: "Retry later; if this repeats, run `paperbrain doctor` and inspect Cache cooldown files.",
        ExitCode.LLM_FAILURE: "Verify provider API keys and model names, then retry with --resume.",
        ExitCode.PDF_UNAVAILABLE: "Retry with --resume later; deep analysis requires a usable local PDF.",
        ExitCode.WRITE_FAILURE: "Check vault, Cache, Run_Records, and PDF directory write permissions.",
        ExitCode.VALIDATION_FAILED: "Run `paperbrain check` locally and inspect the first failing test.",
    }
    return suggestions.get(exit_code, "Inspect stderr and the run-state errors.json file.")


def _emit_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    raise SystemExit(main())
