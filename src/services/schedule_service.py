from datetime import datetime, timedelta
from typing import Optional
from ..api_client import UrfuAPIClient
from ..types import WeekSchedule


class ScheduleService:
    """
    Сервис для работы с расписанием
    """

    def __init__(self, days_ahead: int = 7):
        """
        Инициализирует сервис расписания
        """
        self.days_ahead = days_ahead

    def set_days_ahead(self, days: int) -> None:
        """
        Устанавливает количество дней для отображения расписания
        """
        if 1 <= days <= 30:
            self.days_ahead = days

    def get_schedule(self, group_id: int,
                     date_from: Optional[datetime] = None,
                     days: Optional[int] = None) -> WeekSchedule:
        """
        Получает расписание группы
        """
        if date_from is None:
            date_from = datetime.now()

        days_to_use = days or self.days_ahead
        date_to = date_from + timedelta(days=days_to_use - 1)

        with UrfuAPIClient() as client:
            return client.get_group_schedule(group_id, date_from, date_to)

    def get_today_schedule(self, group_id: int) -> WeekSchedule:
        """
        Получает расписание на сегодня
        """
        today = datetime.now()
        return self.get_schedule(group_id, today, days=1)

    def get_tomorrow_schedule(self, group_id: int) -> WeekSchedule:
        """
        Получает расписание на завтра
        """
        tomorrow = datetime.now() + timedelta(days=1)
        return self.get_schedule(group_id, tomorrow, days=1)

    def export_schedule_to_text(self, group_id: int, group_title: str, days: int = 7) -> str:
        """
        Экспортирует расписание в текстовый файл
        """
        import tempfile
        import os
        from datetime import datetime, timedelta

        today = datetime.now()
        days_until_monday = -today.weekday()
        monday = today + timedelta(days=days_until_monday)
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

        schedule = self.get_schedule(group_id, date_from=monday, days=days)

        fd, path = tempfile.mkstemp(suffix='.txt', prefix='schedule_', text=True)

        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            # Заголовок
            f.write(f" РАСПИСАНИЕ ГРУППЫ {group_title}\n")
            f.write("=" * 60 + "\n")
            f.write(f" Дата выгрузки: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")

            sunday = monday + timedelta(days=6)
            f.write(f" Период: {monday.strftime('%d.%m')} - {sunday.strftime('%d.%m')} (пн-вс)\n")
            f.write("=" * 60 + "\n\n")

            lesson_count = 0
            day_count = 0

            for day in schedule.days:
                if not day.lessons:
                    continue

                day_count += 1
                f.write(f"\n {day.weekday.capitalize()} ({day.date})\n")
                f.write("-" * 40 + "\n")

                for lesson in day.lessons:
                    lesson_count += 1
                    time_start = lesson.timeBegin[:5] if lesson.timeBegin else "??:??"
                    time_end = lesson.timeEnd[:5] if lesson.timeEnd else "??:??"

                    f.write(f"\n   {time_start} - {time_end}\n")
                    f.write(f"   {lesson.title}\n")
                    f.write(f"   Тип: {lesson.loadType}\n")

                    if lesson.pairNumber > 0:
                        f.write(f"   {lesson.pairNumber} пара\n")

                    if lesson.teacherName:
                        f.write(f"   Преподаватель: {lesson.teacherName}\n")

                    if lesson.auditoryTitle:
                        f.write(f"   Аудитория: {lesson.auditoryTitle}\n")
                        if lesson.auditoryLocation:
                            location = lesson.auditoryLocation[:80] if len(
                                lesson.auditoryLocation) > 80 else lesson.auditoryLocation
                            f.write(f"   {location}\n")

                    if lesson.comment:
                        if lesson.comment.startswith('http'):
                            f.write(f"   Ссылка: {lesson.comment}\n")
                        else:
                            f.write(f"   {lesson.comment}\n")

                f.write("\n" + "=" * 40 + "\n")

            f.write(f"\n ИТОГО:\n")
            f.write(f"   • Дней с занятиями: {day_count}\n")
            f.write(f"   • Всего занятий: {lesson_count}\n")

        return path