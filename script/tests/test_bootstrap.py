import argparse
import tempfile
import unittest
from pathlib import Path

import yaml

from src.cli import _run_bootstrap


class BootstrapTests(unittest.TestCase):
    def test_bootstrap_creates_user_config_and_preserves_env(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vault = root / "vault"
            config_dir = root / "config"
            vault.mkdir()

            first = _run_bootstrap(argparse.Namespace(config_dir=str(config_dir), vault=str(vault)))
            self.assertTrue(first["ok"])
            self.assertEqual(set(first["created"]), {"config.yaml", "prompts.yaml", "tags.yaml", ".env"})
            with (config_dir / "config.yaml").open("r", encoding="utf-8") as stream:
                config = yaml.safe_load(stream)
            self.assertEqual(config["obsidian"]["vault_path"], str(vault.resolve()))

            (config_dir / ".env").write_text("OPENROUTER_API_KEY=keep-me\n", encoding="utf-8")
            second = _run_bootstrap(argparse.Namespace(config_dir=str(config_dir), vault=str(vault)))
            self.assertIn(".env", second["preserved"])
            self.assertEqual((config_dir / ".env").read_text(encoding="utf-8"), "OPENROUTER_API_KEY=keep-me\n")

    def test_bootstrap_rejects_missing_vault(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ValueError, "vault path does not exist"):
                _run_bootstrap(argparse.Namespace(config_dir=str(root / "config"), vault=str(root / "missing")))


if __name__ == "__main__":
    unittest.main()
