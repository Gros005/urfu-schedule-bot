from dataclasses import dataclass
from typing import Optional


@dataclass
class Group:
    """Группа студентов."""

    id: int
    divisionId: int
    course: int
    title: str


@dataclass
class Lesson:
    """Урок в расписании."""

    title: str
    loadType: str
    date: str
    timeBegin: str
    timeEnd: str
    pairNumber: int
    auditoryTitle: Optional[str]
    auditoryLocation: Optional[str]
    teacherName: Optional[str]
    comment: Optional[str]


@dataclass
class DaySchedule:
    """Расписание на один день."""

    date: str
    weekday: str
    lessons: list[Lesson]


class WeekSchedule:
    """Расписание на неделю."""

    def __init__(self, days: list[DaySchedule]) -> None:
        self.days = days
