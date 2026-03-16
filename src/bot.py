import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .handlers import BotHandlers

def main():
    """Основная функция запуска бота"""
    print("🚀 Запускаю бота-приветствие...")

    # Загружаем переменные окружения
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        print("❌ Ошибка: BOT_TOKEN не найден в .env файле")
        print("Создайте файл .env с содержимым:")
        print("BOT_TOKEN=ваш_токен_от_botfather")
        exit(1)

    # Создаем приложение бота
    app = Application.builder().token(bot_token).build()

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
