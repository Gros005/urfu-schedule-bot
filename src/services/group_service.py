from typing import List, Optional
from ..api_client import UrfuAPIClient
from ..types import Group


class GroupService:
    """Сервис для работы с группами"""

    @staticmethod
    def search_groups(query: str) -> List[Group]:
        """
        Поиск групп по названию
        """
        with UrfuAPIClient() as client:
            return client.search_groups(query)

    @staticmethod
    def get_group_by_id(group_id: int) -> Optional[Group]:
        """
        Получает информацию о группе по ID
        """
        # Сначала пробуем найти среди предустановленных групп
        try:
            from ..data.preset_groups import get_preset_group_by_id
            preset = get_preset_group_by_id(group_id)
            if preset:
                return Group(
                    id=preset["id"],
                    divisionId=0,  # временное значение
                    course=preset["course"],
                    title=preset["title"]
                )
        except ImportError:
            pass

        # Ищем через API
        try:
            # API ищет по строке, поэтому передаем ID как строку
            groups = GroupService.search_groups(str(group_id))
            for group in groups:
                if group.id == group_id:
                    return group
        except Exception:
            pass

        return None

    @staticmethod
    def get_group_by_title(title: str) -> Optional[Group]:
        """
        Получает информацию о группе по точному названию
        """
        groups = GroupService.search_groups(title)

        for group in groups:
            if group.title.lower() == title.lower():
                return group
        return groups[0] if groups else None

    @staticmethod
    def is_valid_group_id(group_id: int) -> bool:
        """
        Проверяет, существует ли группа с таким ID
        """
        return GroupService.get_group_by_id(group_id) is not None