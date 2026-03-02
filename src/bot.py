import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user

    message = f"""
👋 Привет, {user.first_name} {user.last_name}!

Я — бот для расписания университета.
Сейчас я учусь, но скоро научусь показывать расписание!

Команды:
/start - это сообщение
/help - справка
/about - о боте
    """

    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "Помощь по боту:\n\n"
        "/start - начать работу с ботом\n"
        "/help - эта справка\n"
        "/about - информация о боте"
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /about"""
    await update.message.reply_text(
        "🤖 Бот расписания университета\n\n"
        "Версия: 0.1.0\n"
        "Описание: Простой бот-приветствие\n"
        "Разработка: только началась!"
    )


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

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))

    # Запускаем бота
    print("✅ Бот запущен!")
    print("ℹ️  Нажмите Ctrl+Z для остановки")

    # Запускаем polling
    app.run_polling()


if __name__ == "__main__":
    main()
