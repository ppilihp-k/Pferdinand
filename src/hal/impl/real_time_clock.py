# ---------------------------------------------------------------------------------------------------------------------
import machine
from time import time, gmtime, mktime
from hal.types import Timestamp
# ---------------------------------------------------------------------------------------------------------------------

class RealTimeClock:

    def __init__(self):
        self.__rtc = machine.RTC()
        pass

    def now(self) -> Timestamp:
        return Timestamp().from_tuple(
            self.__rtc.datetime()
        )

    def start_of_day(self) -> Timestamp:
        return self.now().set_time(0, 0, 0)

    pass
# ---------------------------------------------------------------------------------------------------------------------
