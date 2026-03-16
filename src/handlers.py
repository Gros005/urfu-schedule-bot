from telegram import Update
from telegram.ext import ContextTypes

class BotHandlers:

    def __init__(self):
        pass

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user

        message = f"""
        👋 Привет, {user.first_name} {user.last_name}! Рад тебя видеть снова!

        Я — бот для расписания университета.
        Сейчас я учусь, но скоро научусь показывать расписание!

        Команды:
        /start - это сообщение
        /help - справка
        /about - о боте
            """

        await update.message.reply_text(message)


    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        await update.message.reply_text(
            "Помощь по боту:\n\n"
            "/start - начать работу с ботом\n"
            "/help - эта справка\n"
            "/about - информация о боте"
        )


    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /about"""
        await update.message.reply_text(
            "🤖 Бот расписания университета\n\n"
            "Версия: 0.1.0\n"
            "Описание: Простой бот-приветствие\n"
            "Разработка: только началась!"
        )