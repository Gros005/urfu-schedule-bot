import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.handlers import BotHandlers


@pytest.fixture
def mock_update():
    update = MagicMock()
    update.effective_user.first_name = "Иван"
    update.effective_user.last_name = "Иванов"
    update.message.reply_text = AsyncMock()
    return update


@pytest.fixture
def mock_context():
    return MagicMock()


@pytest.fixture
def handlers():
    return BotHandlers()


class TestStartCommand:
    @pytest.mark.asyncio
    async def test_start_command_sends_welcome(self, handlers, mock_update, mock_context):
        await handlers.start_command(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Привет" in call_args
        assert "Иван" in call_args
        assert "/start" in call_args
        assert "/help" in call_args
        assert "/about" in call_args

    @pytest.mark.asyncio
    async def test_start_command_includes_bot_description(self, handlers, mock_update, mock_context):
        await handlers.start_command(mock_update, mock_context)

        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "расписания" in call_args.lower()


class TestHelpCommand:
    @pytest.mark.asyncio
    async def test_help_command_sends_help_text(self, handlers, mock_update, mock_context):
        await handlers.help_command(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "/start" in call_args
        assert "/help" in call_args
        assert "/about" in call_args

    @pytest.mark.asyncio
    async def test_help_command_format(self, handlers, mock_update, mock_context):
        await handlers.help_command(mock_update, mock_context)

        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Помощь" in call_args


class TestAboutCommand:
    @pytest.mark.asyncio
    async def test_about_command_sends_about_text(self, handlers, mock_update, mock_context):
        await handlers.about_command(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Версия: 0.1.0" in call_args
        assert "Бот расписания" in call_args

    @pytest.mark.asyncio
    async def test_about_command_mentions_development(self, handlers, mock_update, mock_context):
        await handlers.about_command(mock_update, mock_context)

        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "разработк" in call_args.lower()


class TestBotHandlersInit:
    def test_handlers_init(self):
        handlers = BotHandlers()
        assert handlers is not None
