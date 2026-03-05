import yaml
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config(path=None):
    if path is None:
        # Get the directory where this script (config_loader.py) is located (src/)
        src_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to get the script/ directory
        base_dir = os.path.dirname(src_dir)
        path = os.path.join(base_dir, "config.yaml")
        
    # Also try to load .env from the same directory as config.yaml if not already loaded
    env_path = os.path.join(os.path.dirname(path), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace environment variables in the config content
    # Matches ${VAR_NAME}
    pattern = re.compile(r'\$\{([^}]+)\}')
    
    def replace_env(match):
        env_var = match.group(1)
        return os.getenv(env_var, match.group(0)) # Return original if not found
        
    updated_content = pattern.sub(replace_env, content)
    
    return yaml.safe_load(updated_content)
