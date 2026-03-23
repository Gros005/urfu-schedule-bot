import pytest
from src.types import Group, Lesson, DaySchedule, WeekSchedule


class TestGroup:
    def test_create_group(self):
        group = Group(
            id=63725,
            divisionId=62404,
            course=3,
            title="МЕН-333009"
        )

        assert group.id == 63725
        assert group.divisionId == 62404
        assert group.course == 3
        assert group.title == "МЕН-333009"

    def test_group_equality(self):
        group1 = Group(id=1, divisionId=2, course=3, title="Test")
        group2 = Group(id=1, divisionId=2, course=3, title="Test")
        group3 = Group(id=2, divisionId=2, course=3, title="Test")

        assert group1 == group2
        assert group1 != group3


class TestLesson:
    def test_create_lesson_with_all_fields(self):
        lesson = Lesson(
            title="Патохимия",
            loadType="лекции",
            date="2026-03-23",
            timeBegin="13:10:00",
            timeEnd="14:45:00",
            pairNumber=3,
            auditoryTitle="472",
            auditoryLocation="ул. Куйбышева, дом 48а",
            teacherName="Емельянов В.В.",
            comment=None
        )

        assert lesson.title == "Патохимия"
        assert lesson.loadType == "лекции"
        assert lesson.pairNumber == 3
        assert lesson.auditoryTitle == "472"
        assert lesson.teacherName == "Емельянов В.В."
        assert lesson.comment is None

    def test_create_lesson_with_optional_fields(self):
        lesson = Lesson(
            title="Физическая культура",
            loadType="онлайн",
            date="2026-03-29",
            timeBegin="00:00:00",
            timeEnd="00:00:00",
            pairNumber=0,
            auditoryTitle=None,
            auditoryLocation=None,
            teacherName=None,
            comment="https://example.com/link"
        )

        assert lesson.auditoryTitle is None
        assert lesson.auditoryLocation is None
        assert lesson.teacherName is None
        assert lesson.comment == "https://example.com/link"

    def test_lesson_equality(self):
        lesson1 = Lesson(
            title="Test", loadType="lec", date="2026-03-23",
            timeBegin="09:00", timeEnd="10:00", pairNumber=1,
            auditoryTitle=None, auditoryLocation=None,
            teacherName=None, comment=None
        )
        lesson2 = Lesson(
            title="Test", loadType="lec", date="2026-03-23",
            timeBegin="09:00", timeEnd="10:00", pairNumber=1,
            auditoryTitle=None, auditoryLocation=None,
            teacherName=None, comment=None
        )

        assert lesson1 == lesson2


class TestDaySchedule:
    def test_create_day_schedule(self):
        lessons = [
            Lesson(
                title="Математика", loadType="лекции", date="2026-03-23",
                timeBegin="09:00", timeEnd="10:35", pairNumber=1,
                auditoryTitle="101", auditoryLocation="Корпус 1",
                teacherName="Иванов", comment=None
            )
        ]
        day = DaySchedule(
            date="2026-03-23",
            weekday="понедельник",
            lessons=lessons
        )

        assert day.date == "2026-03-23"
        assert day.weekday == "понедельник"
        assert len(day.lessons) == 1
        assert day.lessons[0].title == "Математика"

    def test_day_schedule_empty_lessons(self):
        day = DaySchedule(
            date="2026-03-25",
            weekday="среда",
            lessons=[]
        )

        assert len(day.lessons) == 0


class TestWeekSchedule:
    def test_create_week_schedule(self):
        day1 = DaySchedule(
            date="2026-03-23",
            weekday="понедельник",
            lessons=[]
        )
        day2 = DaySchedule(
            date="2026-03-24",
            weekday="вторник",
            lessons=[]
        )
        week = WeekSchedule(days=[day1, day2])

        assert len(week.days) == 2
        assert week.days[0].date == "2026-03-23"
        assert week.days[1].date == "2026-03-24"

    def test_week_schedule_empty_days(self):
        week = WeekSchedule(days=[])

        assert len(week.days) == 0
