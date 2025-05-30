# ---------------------------------------------------------------------------------------------------------------------
from time import mktime, localtime, time
# ---------------------------------------------------------------------------------------------------------------------

class Timestamp:
    def __init__(self):
        # (Jahr, Monat, Tag, Stunde, Minute, Sekunde, Wochentag)
        self.__value = (2000, 0, 0, 0, 0, 0, 0, 0, 0)
        pass

    def to_tuple(self) -> tuple:
        return self.__value

    def hours(self) -> int:
        return self.__value[3]

    def minutes(self) -> int:
        return self.__value[4]

    def seconds(self) -> int:
        return self.__value[5]

    def from_tuple(self, value: tuple) -> 'Self':
        if len(value) < 8:
            raise ValueError
        self.__value = value
        return self

    def set_time(self, hours: int, minutes: int, seconds: int) -> 'Self':
        self.__value = (
            self.__value[0],
            self.__value[1],
            self.__value[2],
            hours,
            minutes,
            seconds,
            self.__value[6],
            self.__value[7],
            0,
        )
        return self

    def mktime(self) -> int:
        return mktime(self.__value)

    def __str__(self) -> str:
        return str(self.__value)
# ---------------------------------------------------------------------------------------------------------------------
