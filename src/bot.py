
from telegram import Update
from telegram.ext import Application, CommandHandler

from .config import Config 
from .handlers import BotHandlers


def main():
    """Основная функция запуска бота"""
    print("🚀 Запускаю бота-приветствие...")

    # Конфигурация бота
    config = Config()

    # Создаем приложение бота
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Инициализация обработчиков
    handlers = BotHandlers()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", handlers.start_command))
    app.add_handler(CommandHandler("help", handlers.help_command))
    app.add_handler(CommandHandler("about", handlers.about_command))

    # Запускаем бота
    print("✅ Бот запущен!")
    print("ℹ️  Нажмите Ctrl+Z для остановки")

    # Запускаем polling
    app.run_polling()


if __name__ == "__main__":
    print(sys.executable)
    main()
