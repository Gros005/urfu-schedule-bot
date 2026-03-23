import pytest
from unittest.mock import patch, MagicMock, AsyncMock


@pytest.fixture
def mock_config():
    config = MagicMock()
    config.BOT_TOKEN = "test_token_123"
    return config


@pytest.fixture
def mock_app():
    app = MagicMock()
    app.add_handler = MagicMock()
    app.run_polling = MagicMock()
    return app


class TestBotMain:
    @patch("src.bot.Application")
    @patch("src.bot.BotHandlers")
    @patch("src.bot.Config")
    @patch("src.bot.logger")
    def test_main_initializes_config(self, mock_logger, mock_config_cls, mock_handlers_cls, mock_app_cls, mock_config, mock_app):
        mock_config_cls.return_value = mock_config
        mock_app_cls.builder.return_value.token.return_value.build.return_value = mock_app
        mock_handlers_cls.return_value = MagicMock()

        from src.bot import main
        main()

        mock_config_cls.assert_called_once()

    @patch("src.bot.Application")
    @patch("src.bot.BotHandlers")
    @patch("src.bot.Config")
    @patch("src.bot.logger")
    def test_main_creates_application(self, mock_logger, mock_config_cls, mock_handlers_cls, mock_app_cls, mock_config, mock_app):
        mock_config_cls.return_value = mock_config
        mock_app_cls.builder.return_value.token.return_value.build.return_value = mock_app
        mock_handlers_cls.return_value = MagicMock()

        from src.bot import main
        main()

        mock_app_cls.builder.assert_called_once()
        mock_app_cls.builder.return_value.token.assert_called_once_with("test_token_123")
        mock_app_cls.builder.return_value.token.return_value.build.assert_called_once()

    @patch("src.bot.Application")
    @patch("src.bot.BotHandlers")
    @patch("src.bot.Config")
    @patch("src.bot.logger")
    def test_main_adds_handlers(self, mock_logger, mock_config_cls, mock_handlers_cls, mock_app_cls, mock_config, mock_app):
        mock_config_cls.return_value = mock_config
        mock_app_cls.builder.return_value.token.return_value.build.return_value = mock_app
        handlers_instance = MagicMock()
        mock_handlers_cls.return_value = handlers_instance

        from src.bot import main
        main()

        assert mock_app.add_handler.call_count == 3

    @patch("src.bot.Application")
    @patch("src.bot.BotHandlers")
    @patch("src.bot.Config")
    @patch("src.bot.logger")
    def test_main_logs_startup(self, mock_logger, mock_config_cls, mock_handlers_cls, mock_app_cls, mock_config, mock_app):
        mock_config_cls.return_value = mock_config
        mock_app_cls.builder.return_value.token.return_value.build.return_value = mock_app
        mock_handlers_cls.return_value = MagicMock()

        from src.bot import main
        main()

        assert mock_logger.info.call_count >= 3

    @patch("src.bot.Application")
    @patch("src.bot.BotHandlers")
    @patch("src.bot.Config")
    @patch("src.bot.logger")
    def test_main_runs_polling(self, mock_logger, mock_config_cls, mock_handlers_cls, mock_app_cls, mock_config, mock_app):
        mock_config_cls.return_value = mock_config
        mock_app_cls.builder.return_value.token.return_value.build.return_value = mock_app
        mock_handlers_cls.return_value = MagicMock()

        from src.bot import main
        main()

        mock_app.run_polling.assert_called_once()


class TestBotImports:
    def test_bot_module_imports(self):
        from src.bot import main
        assert callable(main)
