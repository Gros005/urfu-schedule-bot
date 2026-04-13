import sys
from telegram.ext import Application, CommandHandler
from .config import Config, logger
from .handlers import BotHandlers
from .console_handler import ConsoleHandler


def main():

    """
    Основная функция запуска бота
    """

    logger.info("Запускаю бота...")

    config = Config()
    app = Application.builder().token(config.BOT_TOKEN).build()
    handlers = BotHandlers()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", handlers.start_command))
    app.add_handler(CommandHandler("help", handlers.help_command))
    app.add_handler(CommandHandler("about", handlers.about_command))
    app.add_handler(CommandHandler("schedule", handlers.schedule_command))
    app.add_handler(CommandHandler("setgroup", handlers.setgroup_command))
    app.add_handler(CommandHandler("mygroup", handlers.mygroup_command))
    app.add_handler(CommandHandler("cleargroup", handlers.cleargroup_command))
    app.add_handler(CommandHandler("days", handlers.days_command))
    app.add_handler(CommandHandler("groups", handlers.groups_command))
    app.add_handler(CommandHandler("today", handlers.today_command))
    app.add_handler(CommandHandler("tomorrow", handlers.tomorrow_command))
    app.add_handler(CommandHandler("export", handlers.export_command))

    # Запускаем консольный обработчик (для управления из консоли)
    console = ConsoleHandler(app)
    console.start()

    # Запускаем бота
    logger.info(" Бот запущен!")
    logger.info(" Для остановки введите 'stop' в консоли или нажмите Ctrl+C")
    logger.info(" Доступные команды в Telegram: /start, /help, /about, /schedule, /setgroup, /mygroup, /cleargroup, /days")

    try:
        # Запускаем polling (бесконечный цикл получения обновлений)
        app.run_polling()
    except KeyboardInterrupt:
        logger.info(" Получен сигнал остановки (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print(sys.executable)
    main()