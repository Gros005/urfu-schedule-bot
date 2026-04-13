from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from .config import logger
from .database.user_data import UserData
from .services.group_service import GroupService
from .services.schedule_service import ScheduleService
from .utils.formatters import (
    format_schedule_message,
    format_group_list_message,
    format_mygroup_message,
    format_error_message,
    format_days_settings_message,
    format_days_changed_message,
    format_group_saved_message
)


class BotHandlers:
    """
    Обработчики команд бота
    """

    def __init__(self):
        """
        Инициализирует обработчики с необходимыми сервисами
        """
        self.user_data = UserData()
        self.group_service = GroupService()
        self.schedule_service = ScheduleService(days_ahead=7)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /start
        """
        user = update.effective_user

        message = f"""
👋 Привет, {user.first_name}!

Я — бот для расписания УрФУ.

 *Доступные команды:*
/schedule -  показать расписание
/setgroup -  выбрать группу (по названию или ID)
/today - показать расписание на сегодня
/tomorrow - показать расписание на завтра
/mygroup - ️ информация о вашей группе
/cleargroup -  очистить группу
/days -  установить количество дней для расписания
/groups -  список предустановленных групп
/help -  справка
/about -  о боте
/export - выгрузить расписание в текстовый файл
        """
        await update.message.reply_text(message, parse_mode="Markdown")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /help
        """
        message = """
 *Помощь по боту*

*Основные команды:*
/schedule - показать расписание на ближайшие дни
/today - показать расписание на сегодня
/tomorrow - показать расписание на завтра
/setgroup <название или ID> - выбрать группу
/mygroup - показать текущую группу
/cleargroup - очистить выбранную группу
/export - выгрузить расписание в текстовый файл

*Настройки:*
/days <число> - установить количество дней для расписания (1-30)

*Информация:*
/groups - список предустановленных групп
/about - о боте
/help - эта справка

        """
        await update.message.reply_text(message, parse_mode="Markdown")

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /about
        """
        message = """
 *Бот расписания УрФУ*

*Версия:* 2.0.0
*Функционал:*
• Просмотр расписания групп
• Сохранение выбранной группы
• Настройка периода расписания
• Поиск по названию или ID
*Данные:* API УрФУ

        """
        await update.message.reply_text(message, parse_mode="Markdown")

    async def setgroup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /setgroup - выбор группы (по названию или ID)
        """
        user_id = update.effective_user.id
        args = context.args

        if not args:
            await update.message.reply_text(
                " *Укажите группу*\n\n"
                "Примеры:\n"
                "/setgroup МЕН-333009\n"
                "/setgroup 63725\n\n"
                "Используйте /groups для просмотра доступных групп",
                parse_mode="Markdown"
            )
            return

        query = " ".join(args)
        await update.message.reply_text(f" Ищу группу '{query}'...")

        try:
            groups = []

            # Вариант 1: Пользователь ввел число (ID группы)
            if query.isdigit():
                group_id = int(query)
                group = self.group_service.get_group_by_id(group_id)
                if group:
                    groups = [group]

            # Вариант 2: Пользователь ввел название (содержит МЕН)
            elif "МЕН" in query.upper():
                groups = self.group_service.search_groups(query)

            # Вариант 3: Непонятный запрос
            else:
                await update.message.reply_text(
                    " *Неверный формат запроса*\n\n"
                    "Используйте:\n"
                    "• По названию: `/setgroup МЕН-333009`\n"
                    "• По ID: `/setgroup 63725`\n\n"
                    " Подсказка: название группы обычно начинается с МЕН ",
                    parse_mode="Markdown"
                )
                return

            if not groups:
                await update.message.reply_text(f" Группа '{query}' не найдена")
                return

            if len(groups) == 1:
                # Одна группа - сохраняем сразу
                group = groups[0]
                self.user_data.set_user_group(
                    user_id=user_id,
                    group_id=group.id,
                    group_title=group.title,
                    course=group.course,
                    division_id=group.divisionId
                )
                message = format_group_saved_message(group.title, group.id, group.course)
                await update.message.reply_text(message, parse_mode="Markdown")
            else:
                # Несколько групп - показываем список
                message = format_group_list_message(groups, query)
                await update.message.reply_text(message, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Ошибка в setgroup: {e}")
            await update.message.reply_text(format_error_message(str(e)), parse_mode="Markdown")

    async def mygroup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /mygroup - информация о текущей группе
        """
        user_id = update.effective_user.id
        user_info = self.user_data.get_full_user_info(user_id)

        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(
                " *Группа не выбрана*\n\n"
                "Используйте /setgroup для выбора группы",
                parse_mode="Markdown"
            )
            return

        message = format_mygroup_message(
            group_title=user_info.get('group_title', 'Неизвестно'),
            group_id=user_info['group_id'],
            course=user_info.get('course', 0),
            days_ahead=self.schedule_service.days_ahead
        )
        await update.message.reply_text(message, parse_mode="Markdown")

    async def cleargroup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /cleargroup - удаление группы
        """
        user_id = update.effective_user.id

        user_info = self.user_data.get_full_user_info(user_id)
        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(" У вас не выбрана группа")
            return

        self.user_data.delete_user(user_id)
        await update.message.reply_text(
            " *Группа удалена!*\n\n"
            "Используйте /setgroup для выбора новой группы",
            parse_mode="Markdown"
        )

    async def days_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /days - установка количества дней
        """
        args = context.args

        if not args:
            message = format_days_settings_message(self.schedule_service.days_ahead)
            await update.message.reply_text(message, parse_mode="Markdown")
            return

        try:
            days = int(args[0])
            if days < 1 or days > 30:
                await update.message.reply_text(" Количество дней должно быть от 1 до 30")
                return

            self.schedule_service.set_days_ahead(days)
            message = format_days_changed_message(days)
            await update.message.reply_text(message, parse_mode="Markdown")

        except ValueError:
            await update.message.reply_text(" Укажите число. Пример: /days 14")

    async def groups_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /groups - показать список доступных групп
        """
        from .data.preset_groups import get_preset_groups

        groups = get_preset_groups()

        if not groups:
            await update.message.reply_text(" Список групп не загружен")
            return

        message = " *Доступные группы УрФУ*\n\n"

        men_333 = [g for g in groups if "МЕН-333" in g["title"]]
        men_330 = [g for g in groups if "МЕН-330" in g["title"]]

        if men_333:
            message += "*МЕН-333:*\n"
            for group in men_333:
                message += f"  • `{group['title']}` (ID: {group['id']})\n"

        if men_330:
            message += "\n*МЕН-330:*\n"
            for group in men_330:
                message += f"  • `{group['title']}` (ID: {group['id']})\n"

        message += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        message += " *Как выбрать группу:*\n"
        message += "• По названию: `/setgroup МЕН-333009`\n"
        message += "• По ID: `/setgroup 63725`\n\n"
        message += " *Совет:* Используйте `/setgroup` для поиска других групп"

        await update.message.reply_text(message, parse_mode="Markdown")

    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /schedule - показать расписание
        """
        user_id = update.effective_user.id

        user_info = self.user_data.get_full_user_info(user_id)

        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(
                " *Группа не выбрана!*\n\n"
                "Сначала выберите группу командой /setgroup\n"
                "Пример: /setgroup МЕН-333009 или /setgroup 63725",
                parse_mode="Markdown"
            )
            return

        group_id = user_info['group_id']
        group_title = user_info.get('group_title', 'Ваша группа')

        await update.message.reply_text(f" Загружаю расписание для группы *{group_title}*...",
                                        parse_mode="Markdown")

        try:
            schedule = self.schedule_service.get_schedule(group_id)

            message = format_schedule_message(
                schedule,
                group_title,
                self.schedule_service.days_ahead
            )

            if len(message) > 4096:
                # Если сообщение слишком длинное, отправляем по частям
                for i in range(0, len(message), 4000):
                    await update.message.reply_text(
                        message[i:i + 4000],
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
            logger.error(f"Ошибка в schedule: {e}")
            await update.message.reply_text(format_error_message(str(e)), parse_mode="Markdown")

    async def today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /today - расписание на сегодня
        """
        user_id = update.effective_user.id

        user_info = self.user_data.get_full_user_info(user_id)

        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(
                " *Группа не выбрана!*\n\n"
                "Сначала выберите группу командой /setgroup",
                parse_mode="Markdown"
            )
            return

        group_id = user_info['group_id']
        group_title = user_info.get('group_title', 'Ваша группа')

        await update.message.reply_text(f" Загружаю расписание на сегодня для *{group_title}*...",
                                        parse_mode="Markdown")

        try:
            schedule = self.schedule_service.get_today_schedule(group_id)

            if not schedule.days or not schedule.days[0].lessons:
                await update.message.reply_text(" На сегодня занятий нет")
                return

            today = schedule.days[0]

            message = f" *Расписание на сегодня*\n"
            message += f" *Группа:* {group_title}\n"
            message += f" *{today.weekday.capitalize()} ({today.date})*\n"
            message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            for lesson in today.lessons:
                time_start = lesson.timeBegin[:5] if lesson.timeBegin else "??:??"
                time_end = lesson.timeEnd[:5] if lesson.timeEnd else "??:??"
                pair_info = f"[{lesson.pairNumber} пара]" if lesson.pairNumber > 0 else ""

                message += f" *{time_start}*–{time_end} {pair_info}\n"
                message += f" {lesson.title}\n"
                message += f" *Тип:* {lesson.loadType}\n"

                if lesson.teacherName:
                    message += f" *Преподаватель:* {lesson.teacherName}\n"

                if lesson.auditoryTitle:
                    message += f" *Аудитория:* {lesson.auditoryTitle}\n"

                message += "\n"

            await update.message.reply_text(message, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Ошибка в today: {e}")
            await update.message.reply_text(format_error_message(str(e)), parse_mode="Markdown")

    async def tomorrow_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /tomorrow - расписание на завтра
        """
        user_id = update.effective_user.id

        user_info = self.user_data.get_full_user_info(user_id)

        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(
                " *Группа не выбрана!*\n\n"
                "Сначала выберите группу командой /setgroup",
                parse_mode="Markdown"
            )
            return

        group_id = user_info['group_id']
        group_title = user_info.get('group_title', 'Ваша группа')

        await update.message.reply_text(f" Загружаю расписание на завтра для *{group_title}*...",
                                        parse_mode="Markdown")

        try:
            schedule = self.schedule_service.get_tomorrow_schedule(group_id)

            if not schedule.days or not schedule.days[0].lessons:
                await update.message.reply_text(" На завтра занятий нет")
                return

            tomorrow = schedule.days[0]

            message = f" *Расписание на завтра*\n"
            message += f" *Группа:* {group_title}\n"
            message += f" *{tomorrow.weekday.capitalize()} ({tomorrow.date})*\n"
            message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            for lesson in tomorrow.lessons:
                time_start = lesson.timeBegin[:5] if lesson.timeBegin else "??:??"
                time_end = lesson.timeEnd[:5] if lesson.timeEnd else "??:??"
                pair_info = f"[{lesson.pairNumber} пара]" if lesson.pairNumber > 0 else ""

                message += f" *{time_start}*–{time_end} {pair_info}\n"
                message += f" {lesson.title}\n"
                message += f" *Тип:* {lesson.loadType}\n"

                if lesson.teacherName:
                    message += f" *Преподаватель:* {lesson.teacherName}\n"

                if lesson.auditoryTitle:
                    message += f" *Аудитория:* {lesson.auditoryTitle}\n"

                message += "\n"

            await update.message.reply_text(message, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Ошибка в tomorrow: {e}")
            await update.message.reply_text(format_error_message(str(e)), parse_mode="Markdown")

    async def export_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Обработчик команды /export - выгрузить расписание на текущую неделю (пн-вс)
        """
        user_id = update.effective_user.id

        user_info = self.user_data.get_full_user_info(user_id)

        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(
                " *Группа не выбрана!*\n\n"
                "Сначала выберите группу командой /setgroup",
                parse_mode="Markdown"
            )
            return

        group_id = user_info['group_id']
        group_title = user_info.get('group_title', 'Ваша группа')

        await update.message.reply_text(
            f" Экспортирую расписание на неделю для *{group_title}*...\n"
            f" Период: понедельник - воскресенье",
            parse_mode="Markdown"
        )

        try:
            # Экспортируем ровно 7 дней (неделя с понедельника)
            file_path = self.schedule_service.export_schedule_to_text(
                group_id,
                group_title,
                days=7
            )

            with open(file_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename=f"schedule_{group_title}_{datetime.now().strftime('%Y%m%d')}.txt",
                    caption=f" Расписание группы {group_title}\n Неделя: {datetime.now().strftime('%d.%m')} - {(datetime.now() + timedelta(days=6)).strftime('%d.%m')}"
                )

            # Удаляем временный файл
            import os
            os.unlink(file_path)

        except Exception as e:
            logger.error(f"Ошибка в export: {e}")
            await update.message.reply_text(
                f" *Ошибка при экспорте*\n\n"
                f"Попробуйте позже или используйте /schedule",
                parse_mode="Markdown"
            )