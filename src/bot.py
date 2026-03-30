import sys
from telegram.ext import Application, CommandHandler

from .config import Config, logger
from .handlers import BotHandlers
from .console_handler import ConsoleHandler

def main():
    """Основная функция запуска бота"""
    logger.info("🚀 Запускаю бота-приветствие...")

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
    app.add_handler(CommandHandler("schedule", handlers.schedule_command))

    # Запускаем консольный обработчик
    console = ConsoleHandler(app)
    console.start()

    # Запускаем бота
    logger.info("✅ Бот запущен!")
    logger.info("ℹ️  Для остановки введите 'stop' в консоли или нажмите Ctrl+C")

    try:
        # Запускаем polling
        app.run_polling()
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print(sys.executable)
    main()