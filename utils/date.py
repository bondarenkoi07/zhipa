from datetime import date, timedelta
from enum import Flag, auto, Enum


class TeachState(Flag):
    AUTUMN_SEMESTER = auto()
    WINTER_HOLIDAYS = auto()
    SPRING_SEMESTER = auto()
    SUMMER_HOLIDAYS = auto()

    SEMESTER = AUTUMN_SEMESTER | SPRING_SEMESTER
    HOLIDAYS = WINTER_HOLIDAYS | SUMMER_HOLIDAYS

    AUTUMN = AUTUMN_SEMESTER | WINTER_HOLIDAYS
    SPRING = SPRING_SEMESTER | SUMMER_HOLIDAYS

    def it_is(self, comp: Enum):
        return self.value & comp.value > 0


class TeachTime:
    month_start = 9
    weeks_in_semester = 17

    def __init__(self, now=date.today()):
        if now.month >= self.month_start:
            self.__autumn_start1 = self.__avoid_sunday(date(year=now.year, month=9, day=1))
            self.__spring_start = self.__avoid_sunday(date(year=now.year + 1, month=2, day=9))
            self.__autumn_start2 = self.__avoid_sunday(date(year=now.year + 1, month=9, day=1))
        else:
            self.__autumn_start1 = self.__avoid_sunday(date(year=now.year - 1, month=9, day=1))
            self.__spring_start = self.__avoid_sunday(date(year=now.year, month=2, day=9))
            self.__autumn_start2 = self.__avoid_sunday(date(year=now.year, month=9, day=1))

        self.__autumn_end = self.__autumn_start1 + timedelta(days=7 * self.weeks_in_semester)
        self.__spring_end = self.__spring_start + timedelta(days=7 * self.weeks_in_semester)

        self.teach_state = self.__teach_time(now)

    @property
    def start(self) -> date:
        if self.teach_state.it_is(TeachState.AUTUMN):
            return self.__autumn_start1
        elif self.teach_state.it_is(TeachState.SPRING):
            return self.__spring_start
        raise ValueError(f"Can't get current start with teach_time = {self.teach_state}")

    @property
    def end(self) -> date:
        if self.teach_state.it_is(TeachState.AUTUMN):
            return self.__autumn_end
        elif self.teach_state.it_is(TeachState.SPRING):
            return self.__spring_end
        raise ValueError(f"Can't get current end with teach_time = {self.teach_state}")

    @property
    def next_start(self) -> date:
        if self.teach_state.it_is(TeachState.AUTUMN):
            return self.__spring_start
        elif self.teach_state.it_is(TeachState.SPRING):
            return self.__autumn_start2

    @property
    def week(self) -> int:
        return date.today().isocalendar()[1] - self.start.isocalendar()[1] + 1

    def __teach_time(self, now: date) -> TeachState:
        if self.__autumn_start1 <= now < self.__autumn_end:
            return TeachState.AUTUMN_SEMESTER
        elif self.__autumn_end <= now < self.__spring_start:
            return TeachState.WINTER_HOLIDAYS
        elif self.__spring_start <= now < self.__spring_end:
            return TeachState.SPRING_SEMESTER
        elif self.__spring_end <= now < self.__autumn_start2:
            return TeachState.SUMMER_HOLIDAYS

        raise ValueError('Undefined type of TeachTime')

    @classmethod
    def __avoid_sunday(cls, date: date) -> date:
        if date.weekday() == 6:
            date += timedelta(days=1)
        return date
