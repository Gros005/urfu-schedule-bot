from typing import Optional, List

import httpx
from datetime import datetime, timedelta

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

        Задание:
            Реализуйте этот метод самостоятельно.
            1. Извлеките список событий из data["events"]
            2. Сгруппируйте события по дате
            3. Для каждого события вызовите _parse_event
            4. Отсортируйте дни и уроки по времени
            5. Верните объект WeekSchedule
        """
        raise NotImplementedError("Реализуйте этот метод самостоятельно")

    def _parse_event(self, event: dict) -> Lesson:
        """
        Парсит одно событие в урок.

        Args:
            event: Сырые данные события от API.

        Returns:
            Объект урока.

        Задание:
            Реализуйте этот метод самостоятельно.
            Создайте объект Lesson со всеми полями из event.
        """
        raise NotImplementedError("Реализуйте этот метод самостоятельно")
            
