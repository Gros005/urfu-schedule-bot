from dataclasses import dataclass

@dataclass
class Group:
    """"Группа студентов"""
    
    id: int
    divisionId : int
    course: int
    title: str

@dataclass
class Lesson:
    title: str
    loadType: str
    date: str
    timeBegin: str
    timeEnd: str
    pairNumber: int
    auditoryTitle: str
    auditoryLocation: str
    teacherName: str

@dataclass
class DaySchedule:
    date: str
    weekday: str
    lessons: list[Lesson]

class WeekSchedule:
    days: list[DaySchedule]