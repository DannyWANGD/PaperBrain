import logging
import requests
import urllib.parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Notifier:
    def __init__(self, config):
        self.config = config
        self.bark_url = config.get('notification', {}).get('bark_url', '')
        self.enabled = config.get('notification', {}).get('enabled', False)
        
    def send_daily_summary(self, high_value_papers):
        """
        Sends a summary of high-value papers to Bark.
        """
        if not self.enabled or not self.bark_url or "YOUR_BARK_KEY" in self.bark_url:
            logger.info("Notification skipped: Bark not configured or disabled.")
            return

        if not high_value_papers:
            logger.info("Notification skipped: No high-value papers to report.")
            return

        # Construct Notification Content
        # Title: 📅 PaperBrain: X New Papers
        count = len(high_value_papers)
        title = f"PaperBrain: {count} Top Papers"
        
        # Body: 
        # 1. Title (Score: 9) - Innovation...
        # 2. Title (Score: 8) ...
        body_lines = []
        for p in high_value_papers:
            score = p.get('score', 0)
            short_title = p.get('short_title', p['title'][:20])
            innovation = p.get('innovation', 'No summary')[:100] # Truncate
            
            line = f"🔥[{score}] {short_title}\n💡{innovation}"
            body_lines.append(line)
            
        body = "\n\n".join(body_lines)
        
        # Send Request
        self._send_bark(title, body)

    def _send_bark(self, title, body):
        try:
            base_url = self.bark_url.rstrip('/')

            sound = self.config.get('notification', {}).get('bark_sound', 'minuet')
            group = self.config.get('notification', {}).get('bark_group', 'PaperBrain')
            icon = self.config.get('notification', {}).get(
                'bark_icon',
                'https://cdn-icons-png.flaticon.com/512/2053/2053072.png',
            )

            safe_title = urllib.parse.quote(str(title), safe='')
            safe_body = urllib.parse.quote(str(body), safe='')

            params = urllib.parse.urlencode(
                {
                    'sound': sound,
                    'group': group,
                    'icon': icon,
                },
                safe=':/',
            )

            final_url = f"{base_url}/{safe_title}/{safe_body}?{params}"
            response = requests.get(final_url, timeout=10)

            if response.status_code == 200:
                logger.info("✅ Notification sent to Bark.")
                return

            hint = ""
            try:
                payload = response.json()
                message = str(payload.get("message", ""))
                if "device token" in message.lower():
                    hint = " (Bark 端尚未注册该 Key 对应设备，请在 iPhone 打开 Bark App 等待其完成注册/刷新)"
            except Exception:
                pass

            logger.warning(
                f"Failed to send notification. Status: {response.status_code}, Response: {response.text}{hint}"
            )
                
        except Exception as e:
            logger.error(f"Notification error: {e}")
