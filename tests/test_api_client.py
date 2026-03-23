from unittest.mock import patch, MagicMock
import pytest

from src.api_client import UrfuAPIClient
from src.types import Group, Lesson, DaySchedule, WeekSchedule


SAMPLE_GROUP_DATA = {
    "id": 63725,
    "divisionId": 62404,
    "course": 3,
    "title": "МЕН-333009"
}

SAMPLE_SCHEDULE_DATA = {
    "group": {
        "id": 63725,
        "divisionId": 62404,
        "course": 3,
        "title": "МЕН-333009"
    },
    "events": [
        {
            "id": "22167684-63725",
            "eventId": 22167684,
            "title": "Физическая культура (подгруппа)",
            "loadType": "онлайн",
            "loadKeys": ["pstcim195e3pg0000nfr7sepndfckmrc"],
            "date": "2026-03-29",
            "timeBegin": "00:00:00",
            "timeEnd": "00:00:00",
            "pairNumber": 0,
            "auditoryTitle": None,
            "auditoryLocation": None,
            "teacherAuditoryTitle": None,
            "teacherAuditoryLocation": None,
            "comment": None,
            "teacherName": None,
            "teacherComment": None,
            "teacherLink": None
        },
        {
            "id": "22169494-63725",
            "eventId": 22169494,
            "title": "Патохимия",
            "loadType": "лекции",
            "loadKeys": ["00000000000000000000000000000000"],
            "date": "2026-03-23",
            "timeBegin": "13:10:00",
            "timeEnd": "14:45:00",
            "pairNumber": 3,
            "auditoryTitle": "472",
            "auditoryLocation": "ул. Куйбышева, дом 48а литер А",
            "teacherAuditoryTitle": None,
            "teacherAuditoryLocation": None,
            "comment": None,
            "teacherName": "Емельянов В.В.",
            "teacherComment": None,
            "teacherLink": None
        },
        {
            "id": "22169502-63725",
            "eventId": 22169502,
            "title": "Фармакология",
            "loadType": "лабораторные занятия",
            "loadKeys": ["00000000000000000000000000000000"],
            "date": "2026-03-27",
            "timeBegin": "10:50:00",
            "timeEnd": "12:25:00",
            "pairNumber": 2,
            "auditoryTitle": "802",
            "auditoryLocation": "ул. Куйбышева, дом 48а / ул. Белинского, д.71а литер Б",
            "teacherAuditoryTitle": None,
            "teacherAuditoryLocation": None,
            "comment": None,
            "teacherName": "Емельянов В.В.",
            "teacherComment": None,
            "teacherLink": None
        },
        {
            "id": "22169536-63725",
            "eventId": 22169536,
            "title": "Медицинская микробиология и вирусология",
            "loadType": "лекции",
            "loadKeys": ["00000000000000000000000000000000"],
            "date": "2026-03-25",
            "timeBegin": "09:00:00",
            "timeEnd": "10:35:00",
            "pairNumber": 1,
            "auditoryTitle": "460",
            "auditoryLocation": "ул. Куйбышева, дом 48а литер А",
            "teacherAuditoryTitle": None,
            "teacherAuditoryLocation": None,
            "comment": None,
            "teacherName": "Козлов А.П.",
            "teacherComment": None,
            "teacherLink": None
        },
        {
            "id": "22201606-63725",
            "eventId": 22201606,
            "title": "Дополнительная квалификация (подгруппа)",
            "loadType": "лекции",
            "loadKeys": ["00000000000000000000000000000000"],
            "date": "2026-03-28",
            "timeBegin": "15:00:00",
            "timeEnd": "16:35:00",
            "pairNumber": 4,
            "auditoryTitle": None,
            "auditoryLocation": None,
            "teacherAuditoryTitle": None,
            "teacherAuditoryLocation": None,
            "comment": "https://bbb.urfu.ru/rooms/sgb-t2y-vkx-ern/join",
            "teacherName": "Улитко В.А.",
            "teacherComment": None,
            "teacherLink": None
        }
    ]
}


class TestClientInitialization:
    def test_default_base_url(self):
        client = UrfuAPIClient()
        assert client.base_url == "https://urfu.ru/api/v2"

    def test_custom_base_url(self):
        client = UrfuAPIClient(base_url="https://custom.api.com")
        assert client.base_url == "https://custom.api.com"


class TestSearchGroups:
    def test_search_groups_returns_list(self):
        with patch("src.api_client.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = [SAMPLE_GROUP_DATA]
            mock_client.return_value.get.return_value = mock_response

            client = UrfuAPIClient()
            groups = client.search_groups("МЕН-333009")

            assert isinstance(groups, list)
            assert len(groups) == 1
            assert groups[0].id == 63725
            assert groups[0].divisionId == 62404
            assert groups[0].course == 3
            assert groups[0].title == "МЕН-333009"

    def test_search_groups_returns_multiple(self):
        with patch("src.api_client.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = [
                SAMPLE_GROUP_DATA,
                {**SAMPLE_GROUP_DATA, "id": 63726, "title": "МЕН-333010"},
            ]
            mock_client.return_value.get.return_value = mock_response

            client = UrfuAPIClient()
            groups = client.search_groups("МЕН-33300")

            assert isinstance(groups, list)
            assert len(groups) == 2
            assert groups[0].title == "МЕН-333009"
            assert groups[1].title == "МЕН-333010"

    def test_search_groups_correct_url(self):
        with patch("src.api_client.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = [SAMPLE_GROUP_DATA]
            mock_client.return_value.get.return_value = mock_response

            client = UrfuAPIClient()
            client.search_groups("test")

            call_args = mock_client.return_value.get.call_args
            assert "schedule/groups" in call_args[0][0]
            assert call_args[1]["params"]["search"] == "test"

    def test_search_groups_empty_result(self):
        with patch("src.api_client.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = []
            mock_client.return_value.get.return_value = mock_response

            client = UrfuAPIClient()
            groups = client.search_groups("НеСуществующаяГруппа")

            assert isinstance(groups, list)
            assert len(groups) == 0

    def test_search_groups_raises_on_error(self):
        with patch("src.api_client.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("HTTP 404")
            mock_client.return_value.get.return_value = mock_response

            client = UrfuAPIClient()
            with pytest.raises(Exception, match="HTTP 404"):
                client.search_groups("invalid")


class TestGetGroupSchedule:
    def test_get_schedule_returns_week_schedule(self):
        with patch("src.api_client.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = SAMPLE_SCHEDULE_DATA
            mock_client.return_value.get.return_value = mock_response

            client = UrfuAPIClient()
            schedule = client.get_group_schedule(63725)

            assert isinstance(schedule, WeekSchedule)
            assert isinstance(schedule.days, list)

    def test_get_schedule_with_date_range(self):
        with patch("src.api_client.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = SAMPLE_SCHEDULE_DATA
            mock_client.return_value.get.return_value = mock_response

            client = UrfuAPIClient()
            from datetime import datetime, timedelta
            date_from = datetime(2026, 3, 23)
            date_to = datetime(2026, 3, 29)

            schedule = client.get_group_schedule(63725, date_from, date_to)

            call_args = mock_client.return_value.get.call_args
            assert call_args[1]["params"]["date_gte"] == "2026-03-23"
            assert call_args[1]["params"]["date_lte"] == "2026-03-29"


class TestParseSchedule:
    def test_parse_single_event_to_lesson(self):
        client = UrfuAPIClient()
        event = SAMPLE_SCHEDULE_DATA["events"][1]
        
        lesson = client._parse_event(event)

        assert isinstance(lesson, Lesson)
        assert lesson.title == "Патохимия"
        assert lesson.loadType == "лекции"
        assert lesson.date == "2026-03-23"
        assert lesson.timeBegin == "13:10:00"
        assert lesson.timeEnd == "14:45:00"
        assert lesson.pairNumber == 3
        assert lesson.auditoryTitle == "472"
        assert lesson.auditoryLocation == "ул. Куйбышева, дом 48а литер А"
        assert lesson.teacherName == "Емельянов В.В."

    def test_parse_event_with_online_lesson(self):
        client = UrfuAPIClient()
        event = SAMPLE_SCHEDULE_DATA["events"][0]
        
        lesson = client._parse_event(event)

        assert lesson.title == "Физическая культура (подгруппа)"
        assert lesson.loadType == "онлайн"
        assert lesson.auditoryTitle is None
        assert lesson.auditoryLocation is None

    def test_parse_event_with_link_in_comment(self):
        client = UrfuAPIClient()
        event = SAMPLE_SCHEDULE_DATA["events"][4]
        
        lesson = client._parse_event(event)

        assert lesson.title == "Дополнительная квалификация (подгруппа)"
        assert lesson.comment == "https://bbb.urfu.ru/rooms/sgb-t2y-vkx-ern/join"

    def test_parse_schedule_groups_by_date(self):
        client = UrfuAPIClient()
        schedule = client._parse_schedule(SAMPLE_SCHEDULE_DATA)

        dates = [day.date for day in schedule.days]
        assert "2026-03-23" in dates
        assert "2026-03-25" in dates
        assert "2026-03-27" in dates
        assert "2026-03-28" in dates

    def test_parse_schedule_sorts_days(self):
        client = UrfuAPIClient()
        schedule = client._parse_schedule(SAMPLE_SCHEDULE_DATA)

        dates = [day.date for day in schedule.days]
        assert dates == sorted(dates)

    def test_parse_schedule_groups_lessons_by_time(self):
        client = UrfuAPIClient()
        schedule = client._parse_schedule(SAMPLE_SCHEDULE_DATA)
        
        day_23 = next((d for d in schedule.days if d.date == "2026-03-23"), None)
        assert day_23 is not None
        assert len(day_23.lessons) == 1
        assert day_23.lessons[0].pairNumber == 3

    def test_parse_schedule_calculates_weekday(self):
        client = UrfuAPIClient()
        schedule = client._parse_schedule(SAMPLE_SCHEDULE_DATA)
        
        day_23 = next((d for d in schedule.days if d.date == "2026-03-23"), None)
        assert day_23 is not None
        assert day_23.weekday in ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

    def test_parse_schedule_empty_events(self):
        client = UrfuAPIClient()
        empty_data = {"group": SAMPLE_SCHEDULE_DATA["group"], "events": []}
        
        schedule = client._parse_schedule(empty_data)
        
        assert len(schedule.days) == 0

    def test_lesson_with_all_fields(self):
        event = {
            "id": "12345-63725",
            "eventId": 12345,
            "title": "Тестовый предмет",
            "loadType": "практические занятия",
            "date": "2026-04-01",
            "timeBegin": "10:00:00",
            "timeEnd": "11:35:00",
            "pairNumber": 2,
            "auditoryTitle": "101",
            "auditoryLocation": "Главный корпус",
            "comment": "С собой калькулятор",
            "teacherName": "Иванов И.И."
        }
        
        client = UrfuAPIClient()
        lesson = client._parse_event(event)
        
        assert lesson.title == "Тестовый предмет"
        assert lesson.loadType == "практические занятия"
        assert lesson.pairNumber == 2
        assert lesson.auditoryTitle == "101"
        assert lesson.auditoryLocation == "Главный корпус"
        assert lesson.comment == "С собой калькулятор"
        assert lesson.teacherName == "Иванов И.И."

    def test_lesson_with_minimal_fields(self):
        event = {
            "id": "12345-63725",
            "eventId": 12345,
            "title": "Минимальный предмет",
            "loadType": "лекции",
            "date": "2026-04-01",
            "timeBegin": "10:00:00",
            "timeEnd": "11:35:00",
            "pairNumber": 2,
            "auditoryTitle": None,
            "auditoryLocation": None,
            "comment": None,
            "teacherName": None
        }
        
        client = UrfuAPIClient()
        lesson = client._parse_event(event)
        
        assert lesson.title == "Минимальный предмет"
        assert lesson.auditoryTitle is None
        assert lesson.teacherName is None


class TestDaySchedule:
    def test_day_schedule_contains_lessons(self):
        client = UrfuAPIClient()
        schedule = client._parse_schedule(SAMPLE_SCHEDULE_DATA)
        
        day_27 = next((d for d in schedule.days if d.date == "2026-03-27"), None)
        assert day_27 is not None
        assert len(day_27.lessons) == 1
        assert day_27.lessons[0].title == "Фармакология"


class TestWeekSchedule:
    def test_week_schedule_structure(self):
        client = UrfuAPIClient()
        schedule = client._parse_schedule(SAMPLE_SCHEDULE_DATA)
        
        assert isinstance(schedule, WeekSchedule)
        assert hasattr(schedule, "days")
        assert isinstance(schedule.days, list)

    def test_week_schedule_unique_dates(self):
        client = UrfuAPIClient()
        schedule = client._parse_schedule(SAMPLE_SCHEDULE_DATA)
        
        dates = [day.date for day in schedule.days]
        assert len(dates) == len(set(dates))
