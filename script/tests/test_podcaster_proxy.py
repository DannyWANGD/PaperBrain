import asyncio
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.podcaster import Podcaster  # noqa: E402


class PodcasterProxyTest(unittest.TestCase):
    def test_edge_tts_receives_configured_http_proxy(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = {
                "obsidian": {"vault_path": tmp},
                "openrouter": {
                    "api_key": "test-key",
                    "model_podcast": "moonshotai/kimi-k3",
                },
            }
            podcaster = Podcaster(config, provider="openrouter")
            communicator = unittest.mock.MagicMock()
            communicator.save = AsyncMock()

            with patch("src.podcaster.configured_http_proxy", return_value="http://proxy.test:8080"), \
                 patch("src.podcaster.edge_tts.Communicate", return_value=communicator) as communicate:
                asyncio.run(podcaster._synthesize_audio("hello", str(Path(tmp) / "audio.mp3")))

        communicate.assert_called_once_with(
            "hello",
            "en-US-ChristopherNeural",
            proxy="http://proxy.test:8080",
        )
        communicator.save.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
