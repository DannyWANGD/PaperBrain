import yaml
import os
import logging
from src.notifier import Notifier

# Configure minimal logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_notification():
    # 1. Load config
    print("Loading config.yaml...")
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    # 2. Check configuration
    bark_url = config.get('notification', {}).get('bark_url')
    enabled = config.get('notification', {}).get('enabled')
    
    print(f"Notification Enabled: {enabled}")
    print(f"Bark URL: {bark_url}")
    
    if not enabled:
        print("⚠️  Notification is disabled in config.yaml. Please set 'enabled: true'.")
        return
        
    if not bark_url or "YOUR_BARK_KEY" in bark_url:
        print("⚠️  Bark URL is not configured correctly. Please update 'bark_url' in config.yaml.")
        return

    # 3. Initialize Notifier
    notifier = Notifier(config)
    
    # 4. Create Dummy Data
    test_papers = [
        {
            "title": "Test Paper: World Models for Robots",
            "score": 9,
            "short_title": "World_Models",
            "innovation": "This is a test notification from PaperBrain to verify Bark setup."
        }
    ]
    
    # 5. Send Notification
    print("\nSending test notification...")
    notifier.send_daily_summary(test_papers)
    print("\nCheck your phone! If you received it, everything is working.")

if __name__ == "__main__":
    test_notification()
