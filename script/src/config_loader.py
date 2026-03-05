import yaml
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config(path=None):
    if path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "config.yaml")
        
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
