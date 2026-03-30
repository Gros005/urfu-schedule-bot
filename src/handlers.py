from telegram import Update
from telegram.ext import ContextTypes
from .config import logger


class BotHandlers:
    """Обработчики команд бота."""

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        /schedule - расписание на неделю
            """

        await update.message.reply_text(message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /help"""
        await update.message.reply_text(
            "📋 *Помощь по боту*\n\n"
            "/start - начать работу с ботом\n"
            "/help - эта справка\n"
            "/about - информация о боте\n"
            "/schedule - 📅 расписание на текущую неделю\n\n"
            "*Группа:* МЕН-333009\n"
            "*Данные:* актуальное расписание с сайта УрФУ",
            parse_mode="Markdown"
        )

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /about"""
        await update.message.reply_text(
            "🤖 Бот расписания университета\n\n"
            "Версия: 0.1.0\n"
            "Описание: Бот для расписания УрФУ\n"
            "Разработка: активно ведется!"
        )

    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /schedule - показывает полное расписание"""
        from .api_client import UrfuAPIClient
        from datetime import datetime, timedelta

        logger.info("Команда /schedule получена")

        # ID группы МЕН-333009
        group_id = 63725

        await update.message.reply_text("⏳ Загружаю расписание...")

        try:
            with UrfuAPIClient() as client:
                # Получаем расписание на ближайшую неделю
                date_from = datetime.now()
                date_to = date_from + timedelta(days=7)
                schedule = client.get_group_schedule(group_id, date_from, date_to)

                if not schedule.days:
                    await update.message.reply_text("📭 На ближайшую неделю занятий нет")
                    return

                # Формируем красивое сообщение
                message = "📚 *РАСПИСАНИЕ НА НЕДЕЛЮ*\n"
                message += f"📅 С {date_from.strftime('%d.%m')} по {date_to.strftime('%d.%m')}\n"
                message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

                day_count = 0

                for day in schedule.days:
                    if not day.lessons:
                        continue

                    day_count += 1
                    # Заголовок дня
                    message += f"*📌 {day.weekday.capitalize()} ({day.date[5:].replace('-', '.')})*\n"
                    message += "────────────────────────────────────\n"

                    for lesson in day.lessons:
                        # Время занятия
                        time_start = lesson.timeBegin[:5] if lesson.timeBegin else "??:??"
                        time_end = lesson.timeEnd[:5] if lesson.timeEnd else "??:??"

                        # Номер пары
                        pair_info = f"[{lesson.pairNumber} пара]" if lesson.pairNumber > 0 else ""

                        # Формируем строку занятия
                        message += f"🕐 *{time_start}*–{time_end} {pair_info}\n"
                        message += f"📖 {lesson.title}\n"
                        message += f"📚 *Тип:* {lesson.loadType}\n"

                        if lesson.teacherName:
                            message += f"👨‍🏫 *Преподаватель:* {lesson.teacherName}\n"

                        if lesson.auditoryTitle:
                            message += f"🏛 *Аудитория:* {lesson.auditoryTitle}\n"
                            if lesson.auditoryLocation:
                                message += f"📍 {lesson.auditoryLocation}\n"

                        if lesson.comment and lesson.comment.startswith('http'):
                            message += f"🔗 [Ссылка на занятие]({lesson.comment})\n"
                        elif lesson.comment:
                            message += f"💬 {lesson.comment}\n"

                        message += "\n"

                    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

                if day_count == 0:
                    await update.message.reply_text("📭 На этой неделе занятий нет")
                elif len(message) > 4096:
                    # Если сообщение слишком длинное, отправляем по частям
                    parts = []
                    current_part = ""
                    for line in message.split('\n'):
                        if len(current_part) + len(line) + 1 > 4000:
                            parts.append(current_part)
                            current_part = line
                        else:
                            current_part += line + '\n'
                    if current_part:
                        parts.append(current_part)

                    for i, part in enumerate(parts, 1):
                        await update.message.reply_text(
                            f"📚 *Расписание (часть {i}/{len(parts)})*\n\n{part}",
                            parse_mode="Markdown",
                            disable_web_page_preview=True
                        )
                else:
                    await update.message.reply_text(
                        message,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )

        except Exception as e:
            error_msg = f"❌ Ошибка при загрузке расписания: {str(e)}"
            logger.error(f"Ошибка в schedule_command: {e}", exc_info=True)
            await update.message.reply_text(error_msg)