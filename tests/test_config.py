import os
import pytest
from unittest.mock import patch, MagicMock


class TestConfig:
    def test_bot_token_from_env(self):
        with patch.dict(os.environ, {"BOT_TOKEN": "test_token_123"}, clear=True):
            with patch("src.config.load_dotenv"):
                with patch("src.config.logger"):
                    with patch("builtins.exit"):
                        import importlib
                        import src.config
                        importlib.reload(src.config)
                        from src.config import Config
                        assert Config.BOT_TOKEN == "test_token_123"

    def test_config_class_has_bot_token(self):
        with patch.dict(os.environ, {"BOT_TOKEN": "test_token"}):
            with patch("src.config.load_dotenv"):
                with patch("src.config.logger"):
                    with patch("builtins.exit"):
                        import importlib
                        import src.config
                        importlib.reload(src.config)
                        from src.config import Config
                        assert hasattr(Config, "BOT_TOKEN")


class TestLogger:
    def test_logger_imported(self):
        with patch.dict(os.environ, {"BOT_TOKEN": "test"}):
            with patch("src.config.load_dotenv"):
                with patch("src.config.logger"):
                    with patch("builtins.exit"):
                        import importlib
                        import src.config
                        importlib.reload(src.config)
                        assert hasattr(src.config, "logger")
