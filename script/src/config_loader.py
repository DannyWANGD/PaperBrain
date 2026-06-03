import yaml
import os
import re
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()

def _resolve_base_dir():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(src_dir)

def _first_existing(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return paths[0]

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
    """Normalize relative paths in config.yaml against the config file directory."""
    if not isinstance(config, dict):
        return config
    obsidian_cfg = config.get("obsidian")
    if not isinstance(obsidian_cfg, dict):
        return config
    vault_path = obsidian_cfg.get("vault_path")
    if not isinstance(vault_path, str) or not vault_path.strip():
        return config

    if not os.path.isabs(vault_path):
        config_dir = os.path.dirname(os.path.abspath(config_path))
        obsidian_cfg["vault_path"] = os.path.normpath(
            os.path.abspath(os.path.join(config_dir, vault_path))
        )
    else:
        obsidian_cfg["vault_path"] = os.path.normpath(vault_path)
    return config

def load_config(path=None):
    if path is None:
        base_dir = _resolve_base_dir()
        path = _first_existing([
            os.path.join(base_dir, "config", "config.yaml"),
            os.path.join(base_dir, "config.yaml"),
        ])
    config = _load_yaml_with_env(path)
    return _normalize_paths(config, path)

def load_prompts(path=None):
    """Load prompts.yaml. Returns empty dict if file not found (backward compatible)."""
    if path is None:
        base_dir = _resolve_base_dir()
        path = _first_existing([
            os.path.join(base_dir, "config", "prompts.yaml"),
            os.path.join(base_dir, "prompts.yaml"),
        ])
    if not os.path.exists(path):
        return {}
    try:
        return _load_yaml_with_env(path)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Failed to load prompts.yaml: {e}")
        return {}
