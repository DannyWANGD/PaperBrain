import yaml
import os
import re
from src.paths import PaperBrainPaths
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()

def _load_yaml_with_env(path):
    config_dir = os.path.dirname(path)
    for env_path in (
        os.path.join(config_dir, ".env"),
        os.path.join(os.path.dirname(config_dir), ".env"),
    ):
        if os.path.exists(env_path):
            load_dotenv(env_path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(r'\$\{([^}]+)\}')
    def replace_env(match):
        return os.getenv(match.group(1), match.group(0))
    return yaml.safe_load(pattern.sub(replace_env, content))

def _normalize_paths(config, config_path):
    """Normalize project paths from the repository root and vault paths from vault root."""
    if not isinstance(config, dict):
        return config
    obsidian_cfg = config.get("obsidian")
    if not isinstance(obsidian_cfg, dict):
        return config

    paths = PaperBrainPaths.from_config(config, config_path=config_path)
    obsidian_cfg["vault_path"] = os.path.normpath(str(paths.vault_path))
    config["_paperbrain_paths"] = paths.as_dict()
    return config

def load_config(path=None):
    path = str(PaperBrainPaths.resolve_config_path(path))
    config = _load_yaml_with_env(path)
    return _normalize_paths(config, path)

def load_prompts(path=None):
    """Load prompts.yaml. Returns empty dict if file not found (backward compatible)."""
    path = str(PaperBrainPaths.resolve_prompts_path(path))
    if not os.path.exists(path):
        return {}
    try:
        return _load_yaml_with_env(path)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Failed to load prompts.yaml: {e}")
        return {}
