"""Runtime control primitives for CLI/plugin orchestration."""

from __future__ import annotations

import json
import os
import time
import ctypes
from datetime import datetime
from pathlib import Path

from src.paths import PaperBrainPaths


LOCK_FILENAME = "paperbrain_pipeline.lock.json"
CANCEL_FILENAME = "paperbrain_cancel.json"


class RunAlreadyActive(RuntimeError):
    """Raised when another PaperBrain pipeline already owns the vault lock."""


class RunCancelled(RuntimeError):
    """Raised when a soft-cancel request is observed."""


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _paths(config):
    paths = PaperBrainPaths.from_config_dict(config)
    paths.cache_dir.mkdir(parents=True, exist_ok=True)
    return paths


def lock_path(config) -> Path:
    return _paths(config).cache_dir / LOCK_FILENAME


def cancel_path(config) -> Path:
    return _paths(config).cache_dir / CANCEL_FILENAME


def _read_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _pid_running(pid):
    try:
        pid = int(pid)
    except Exception:
        return False
    if pid <= 0:
        return False
    if os.name == "nt":
        process_query_limited_information = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(process_query_limited_information, False, pid)
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except OSError:
        return False


class PipelineLock:
    def __init__(self, config, command, target_date=None, provider="", stale_after_seconds=24 * 60 * 60):
        self.config = config
        self.command = command
        self.target_date = target_date
        self.provider = provider
        self.stale_after_seconds = stale_after_seconds
        self.path = lock_path(config)
        self.token = f"{os.getpid()}-{time.time_ns()}"
        self.acquired = False

    def acquire(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        existing = _read_json(self.path) if self.path.exists() else {}
        if self.path.exists() and not existing:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass
        if existing:
            pid = existing.get("pid")
            created_ts = float(existing.get("created_ts", 0) or 0)
            stale = created_ts and (time.time() - created_ts > self.stale_after_seconds)
            if _pid_running(pid) and not stale:
                raise RunAlreadyActive(
                    f"PaperBrain is already running: pid={pid}, command={existing.get('command')}, "
                    f"started_at={existing.get('created_at')}"
                )
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass

        payload = {
            "token": self.token,
            "pid": os.getpid(),
            "command": self.command,
            "provider": self.provider,
            "target_date": str(self.target_date) if self.target_date is not None else "",
            "created_at": _now(),
            "created_ts": time.time(),
        }
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(str(self.path), flags)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception:
            os.close(fd)
            raise
        self.acquired = True
        return self

    def release(self):
        if not self.acquired:
            return
        current = _read_json(self.path)
        if current.get("token") == self.token:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass
        self.acquired = False

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc, tb):
        self.release()


def clear_cancel_request(config):
    path = cancel_path(config)
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def request_cancel(config, reason="user_requested"):
    path = cancel_path(config)
    payload = {
        "requested": True,
        "reason": reason or "user_requested",
        "pid": os.getpid(),
        "created_at": _now(),
        "created_ts": time.time(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path, payload


def cancel_request(config):
    path = cancel_path(config)
    return _read_json(path) if path.exists() else {}


def raise_if_cancelled(config):
    request = cancel_request(config)
    if request.get("requested"):
        raise RunCancelled(f"Run cancelled: {request.get('reason') or 'user_requested'}")
