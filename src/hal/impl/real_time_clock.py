# ---------------------------------------------------------------------------------------------------------------------
import machine
from time import time, gmtime, mktime
from hal.types import Timestamp
from hal.interfaces.ireal_time_clock import IRealTimeClock
# ---------------------------------------------------------------------------------------------------------------------

class I2CReadTimeClock(IRealTimeClock):

    def __init__(self):
        pass

    def set_time(self, timestamp: Timestamp) -> 'Self':
        return self

    def now(self) -> Timestamp:
        return Timestamp()

    pass

# ---------------------------------------------------------------------------------------------------------------------

class RealTimeClock(IRealTimeClock):

    def __init__(self):
        self.__rtc = machine.RTC()
        pass

    def set_time(self, timestamp: Timestamp) -> 'Self':
        return self

    def now(self) -> Timestamp:
        return Timestamp().from_tuple(
            self.__rtc.datetime()
        )

    def start_of_day(self) -> Timestamp:
        return self.now().set_time(0, 0, 0)

    pass
# ---------------------------------------------------------------------------------------------------------------------
