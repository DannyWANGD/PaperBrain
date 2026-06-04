"""Unified command line interface for PaperBrain."""

from __future__ import annotations

import argparse
import compileall
import importlib
import json
import os
import sys
import time
import traceback
import unittest
from datetime import datetime, timedelta
from enum import IntEnum
from pathlib import Path

from src.config_loader import load_config, load_prompts
from src.paths import PaperBrainPaths


REQUIRED_DEPENDENCIES = {
    "feedparser": "feedparser",
    "requests": "requests",
    "yaml": "pyyaml",
    "tqdm": "tqdm",
    "bs4": "beautifulsoup4",
    "fitz": "pymupdf",
    "openai": "openai",
    "edge_tts": "edge-tts",
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

    subparsers.add_parser("doctor", help="Run local configuration and path diagnostics.")

    check_parser = subparsers.add_parser("check", help="Run local validation checks.")
    check_parser.add_argument("--skip-tests", action="store_true", help="Compile and import only; skip unit tests.")

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
    checks = [
        _path_check("config", paths.config_path, must_exist=True),
        _path_check("prompts", paths.prompts_path, must_exist=False),
        _path_check("vault", paths.vault_path, must_exist=True),
        _path_check("cache", paths.cache_dir, must_exist=False),
        _path_check("run_records", paths.run_records_dir, must_exist=False),
        _path_check("research_notes", paths.notes_dir, must_exist=False),
        _path_check("research_index", paths.research_index_dir, must_exist=False),
        _provider_check("doubao", config),
        _provider_check("openrouter", config),
    ]
    checks.extend(_dependency_checks(severity="warning"))
    ok = all(check["ok"] for check in checks if check["severity"] == "error")
    payload = {
        "ok": ok,
        "command": "doctor",
        "paths": paths.as_dict(),
        "prompts_loaded": bool(prompts),
        "checks": checks,
    }
    paths.diagnostics_dir.mkdir(parents=True, exist_ok=True)
    latest = paths.diagnostics_dir / "latest.json"
    latest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    payload["artifacts"] = {"diagnostics": str(latest)}
    if not ok:
        raise RuntimeError("Doctor found one or more blocking local configuration errors.")
    return payload


def _run_check(args) -> dict:
    paths = PaperBrainPaths.default()
    script_dir = str(paths.script_dir)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    missing_dependencies = [check for check in _dependency_checks(severity="error") if not check["ok"]]
    compile_ok = compileall.compile_dir(script_dir, quiet=1)
    import_ok = False if missing_dependencies else _import_core_modules()
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

    ok = bool(compile_ok and import_ok and tests_ok and not missing_dependencies)
    payload = {
        "ok": ok,
        "command": "check",
        "compile_ok": bool(compile_ok),
        "import_ok": bool(import_ok),
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


def _path_check(name: str, path: Path, must_exist: bool) -> dict:
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
        "path": str(path),
        "message": message,
    }


def _provider_check(provider: str, config: dict) -> dict:
    cfg = config.get(provider, {})
    key = str(cfg.get("api_key") or "")
    ok = bool(key and not key.startswith("${"))
    return {
        "name": f"{provider}_api_key",
        "ok": ok,
        "severity": "warning",
        "message": "API key is configured" if ok else f"{provider} API key is missing or still unresolved",
    }


def _dependency_checks(severity: str) -> list[dict]:
    import importlib.util

    checks = []
    for module, package in REQUIRED_DEPENDENCIES.items():
        ok = importlib.util.find_spec(module) is not None
        checks.append(
            {
                "name": f"dependency_{package}",
                "package": package,
                "module": module,
                "ok": ok,
                "severity": severity,
                "message": f"{package} is importable" if ok else f"{package} is not installed in this Python environment",
            }
        )
    return checks


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
