from typing import Optional, List
from collections import defaultdict
from datetime import datetime, timedelta

import httpx

from .config import logger
from .types import Group, Lesson, DaySchedule, WeekSchedule


class UrfuAPIClient:
    """Клиент для API расписания УрФУ."""

    def __init__(self, base_url: str = "https://urfu.ru/api/v2") -> None:
        """
        Инициализирует клиент.

        Args:
            base_url: Базовый URL API.
        """
        self.base_url = base_url
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        """Получает или создаёт HTTP-клиент."""
        if self._client is None:
            self._client = httpx.Client(timeout=30.0)
        return self._client

    def close(self) -> None:
        """Закрывает HTTP-клиент."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "UrfuAPIClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def _get(self, endpoint: str, params: dict) -> dict:
        """
        Выполняет GET-запрос к API.

        Args:
            endpoint: Эндпоинт API.
            params: Параметры запроса.

        Returns:
            JSON-ответ от API.
        """
        url = f"{self.base_url}/{endpoint}/"
        logger.debug("GET %s params=%s", url, params)
        response = self._get_client().get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search_groups(self, name: str) -> List[Group]:
        """
        Ищет группы по названию.

        Args:
            name: Название группы.

        Returns:
            Список найденных групп.
        """
        data = self._get("schedule/groups", {"search": name})

        groups = [
            Group(
                id=item["id"],
                divisionId=item["divisionId"],
                course=item["course"],
                title=item["title"],
            )
            for item in data
        ]

        logger.debug("Найдено %d групп по запросу '%s'", len(groups), name)
        return groups

    def get_group_schedule(
            self,
            group_id: int,
            date_from: Optional[datetime] = None,
            date_to: Optional[datetime] = None,
    ) -> WeekSchedule:
        """
        Получает расписание группы.

        Args:
            group_id: ID группы.
            date_from: Начальная дата (по умолчанию — сегодня).
            date_to: Конечная дата (по умолчанию — через неделю).

        Returns:
            Расписание на неделю.
        """
        if date_from is None:
            date_from = datetime.now()
        if date_to is None:
            date_to = date_from + timedelta(days=7)

        params = {
            "date_gte": date_from.strftime("%Y-%m-%d"),
            "date_lte": date_to.strftime("%Y-%m-%d"),
        }

        data = self._get(f"schedule/groups/{group_id}/schedule", params)
        return self._parse_schedule(data)

    def _parse_schedule(self, data: dict) -> WeekSchedule:
        """
        Парсит данные расписания.

        Args:
            data: Сырые данные от API.

        Returns:
            Расписание на неделю.
        """
        # Группируем события по дате
        events_by_date = defaultdict(list)
        for event in data["events"]:
            lesson = self._parse_event(event)
            events_by_date[event["date"]].append(lesson)

        # Создаем дни
        days = []
        for date, lessons in sorted(events_by_date.items()):
            # Сортируем уроки по времени
            lessons.sort(key=lambda x: x.timeBegin)

            days.append(DaySchedule(
                date=date,
                weekday=self._get_weekday(date),
                lessons=lessons
            ))

        return WeekSchedule(days=days)

    def _parse_event(self, event: dict) -> Lesson:
        """
        Парсит одно событие в урок.

        Args:
            event: Сырые данные события от API.

        Returns:
            Объект урока.
        """
        return Lesson(
            title=event.get("title", ""),
            loadType=event.get("loadType", ""),
            date=event.get("date", ""),
            timeBegin=event.get("timeBegin", ""),
            timeEnd=event.get("timeEnd", ""),
            pairNumber=event.get("pairNumber", 0),
            auditoryTitle=event.get("auditoryTitle"),
            auditoryLocation=event.get("auditoryLocation"),
            teacherName=event.get("teacherName"),
            comment=event.get("comment"),
        )

    def _get_weekday(self, date_str: str) -> str:
        """
        Возвращает название дня недели по дате.

        Args:
            date_str: Дата в формате YYYY-MM-DD

        Returns:
            Название дня недели.
        """
        weekdays = ["понедельник", "вторник", "среда", "четверг",
                    "пятница", "суббота", "воскресенье"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return weekdays[dt.weekday()]