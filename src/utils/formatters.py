from typing import List
from ..types import WeekSchedule, Lesson, Group
from .grammar import plural_form, format_days_message


def format_schedule_message(schedule: WeekSchedule,
                            group_title: str = None,
                            days_ahead: int = 7) -> str:
    """
    Форматирует расписание в красивое сообщение для Telegram
    """
    if not schedule.days:
        return " На ближайшие дни занятий нет"

    message = " *РАСПИСАНИЕ*\n"
    if group_title:
        message += f" *Группа:* {group_title}\n"

    days_word = format_days_message(days_ahead)
    message += f" *Период:* {days_ahead} {days_word}\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    day_count = 0

    for day in schedule.days:
        if not day.lessons: continue

        day_count += 1
        weekday_ru = _translate_weekday(day.weekday)
        date_short = day.date[5:].replace('-', '.')
        message += f"* {weekday_ru} ({date_short})*\n"
        message += "────────────────────────────────────\n"

        for lesson in day.lessons: message += _format_lesson(lesson)
        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if day_count == 0: return " На ближайшие дни занятий нет"

    return message


def _format_lesson(lesson: Lesson) -> str:
    """
    Форматирует одно занятие
    """
    # Время
    time_start = lesson.timeBegin[:5] if lesson.timeBegin else "??:??"
    time_end = lesson.timeEnd[:5] if lesson.timeEnd else "??:??"
    pair_info = f"[{lesson.pairNumber} пара]" if lesson.pairNumber > 0 else ""

    message = f" *{time_start}*–{time_end} {pair_info}\n"
    message += f" {lesson.title}\n"
    message += f" *Тип:* {lesson.loadType}\n"

    # Преподаватель
    if lesson.teacherName:
        message += f" *Преподаватель:* {lesson.teacherName}\n"

    # Аудитория
    if lesson.auditoryTitle:
        message += f" *Аудитория:* {lesson.auditoryTitle}\n"
        if lesson.auditoryLocation:
            # Сокращаем длинное название локации
            location = lesson.auditoryLocation[:60] + "..." if len(
                lesson.auditoryLocation) > 60 else lesson.auditoryLocation
            message += f" {location}\n"

    # Комментарий или ссылка
    if lesson.comment:
        if lesson.comment.startswith('http'):
            message += f" [Ссылка на занятие]({lesson.comment})\n"
        else:
            comment = lesson.comment[:80] + "..." if len(lesson.comment) > 80 else lesson.comment
            message += f" {comment}\n"

    return message + "\n"


def format_group_list_message(groups: List[Group], query: str) -> str:
    """
    Форматирует список найденных групп
    """
    if not groups: return f" По запросу '{query}' группы не найдены"

    group_word = plural_form(len(groups), ("группа", "группы", "групп"))

    message = f" *Результаты поиска групп:*\n"
    message += f" *Запрос:* '{query}'\n"
    message += f" *Найдено:* {len(groups)} {group_word}\n\n"

    for i, group in enumerate(groups[:10], 1):
        course_word = plural_form(group.course, ("курс", "курса", "курсов"))
        message += f"{i}. *{group.title}*\n"
        message += f"    ID: `{group.id}`\n"
        message += f"    {group.course} {course_word}\n\n"

    if len(groups) > 10:
        message += f"*...и еще {len(groups) - 10} {plural_form(len(groups) - 10, ('группа', 'группы', 'групп'))}*\n\n"

    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    message += " *Как выбрать группу:*\n"
    message += "• По названию: `/setgroup МЕН-333009`\n"
    message += "• По ID: `/setgroup 63725`\n\n"

    return message


def format_mygroup_message(group_title: str, group_id: int, course: int, days_ahead: int) -> str:
    """
    Форматирует сообщение с информацией о текущей группе
    """
    course_word = plural_form(course, ("курс", "курса", "курсов"))
    days_word = format_days_message(days_ahead)

    message = f"""
 *Ваша текущая группа*

 *Название:* {group_title}
 *ID:* `{group_id}`
 *Курс:* {course} *курс *

 *Настройки:*
 *Дней для расписания:* {days_ahead} {days_word}

💡 *Команды:*
/schedule - показать расписание
/cleargroup - удалить группу
/days <число> - изменить количество дней
"""
    return message


def format_days_settings_message(current_days: int) -> str:
    """
    Форматирует сообщение о настройке количества дней
    """
    days_word = format_days_message(current_days)
    return f"""
 *Текущее количество дней:* {current_days} {days_word}

Используйте /days <число> для изменения
Пример: /days 14
Доступный диапазон: 1-30 дней
"""


def format_days_changed_message(days: int) -> str:
    """
    Форматирует сообщение об успешном изменении количества дней
    """
    days_word = format_days_message(days)
    return f"""
 *Количество дней изменено!*

 Теперь расписание показывается на {days} {days_word}

Используйте /schedule для просмотра
"""


def _translate_weekday(weekday: str) -> str:
    """
    Переводит название дня недели на русский с заглавной буквы
    """
    return weekday.capitalize()


def format_error_message(error: str) -> str:
    """
    Форматирует сообщение об ошибке
    """
    return f" *Ошибка:* {error}\n\nПопробуйте позже или обратитесь к администратору."


def format_group_saved_message(group_title: str, group_id: int, course: int) -> str:
    """
    Форматирует сообщение об успешном сохранении группы
    """
    course_word = plural_form(course, ("курс", "курса", "курсов"))
    return f"""
 *Группа сохранена!*

 {group_title}
 {course} {course_word}
 ID: `{group_id}`

Теперь используйте /schedule для просмотра расписания
"""