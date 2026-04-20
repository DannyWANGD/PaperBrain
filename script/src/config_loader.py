import yaml
import os
import re
from dotenv import load_dotenv

load_dotenv()

def _resolve_base_dir():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(src_dir)

def _load_yaml_with_env(path):
    env_path = os.path.join(os.path.dirname(path), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(r'\$\{([^}]+)\}')
    def replace_env(match):
        return os.getenv(match.group(1), match.group(0))
    return yaml.safe_load(pattern.sub(replace_env, content))

def load_config(path=None):
    if path is None:
        path = os.path.join(_resolve_base_dir(), "config.yaml")
    return _load_yaml_with_env(path)

def load_prompts(path=None):
    """Load prompts.yaml. Returns empty dict if file not found (backward compatible)."""
    if path is None:
        path = os.path.join(_resolve_base_dir(), "prompts.yaml")
    if not os.path.exists(path):
        return {}
    try:
        return _load_yaml_with_env(path)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Failed to load prompts.yaml: {e}")
        return {}

def load_themes(path=None):
    """Load themes.yaml. Returns empty dict if file not found (backward compatible)."""
    if path is None:
        path = os.path.join(_resolve_base_dir(), "themes.yaml")
    if not os.path.exists(path):
        return {}
    try:
        return _load_yaml_with_env(path)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Failed to load themes.yaml: {e}")
        return {}
