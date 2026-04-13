"""
Модуль для правильного склонения слов
"""

def plural_form(number: int, forms: tuple) -> str:
    """
    Возвращает правильную форму слова в зависимости от числа
    """
    n = abs(number) % 100
    n1 = n % 10

    # Исключение для 11-19
    if 10 < n < 20:
        return forms[2]
    # Для 2-4
    if 1 < n1 < 5:
        return forms[1]
    # Для 1
    if n1 == 1:
        return forms[0]
    # Для 0, 5-9, 11-19
    return forms[2]


def format_found_message(count: int, query: str) -> str:
    """
    Форматирует сообщение о найденных группах
    """
    group_word = plural_form(count, ("группа", "группы", "групп"))
    return f" Найдено {count} {group_word} по запросу '{query}'"


def format_days_message(days: int) -> str:
    """
    Форматирует сообщение о количестве дней
    """
    return plural_form(days, ("день", "дня", "дней"))


def format_course_message(course: int) -> str:
    """
    Форматирует сообщение о курсе
    """
    return plural_form(course, ("курс", "курса", "курсов"))