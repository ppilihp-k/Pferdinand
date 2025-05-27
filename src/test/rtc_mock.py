from hal.interfaces.ireal_time_clock import IRealTimeClock
from hal.interfaces.types import Timestamp
from time import localtime, time

class Rtc(IRealTimeClock):

    def set_time(self, timestamp: Timestamp) -> 'Self':
        return self

    def now(self) -> Timestamp:
        return Timestamp().from_tuple(
            localtime(
                time()
            )
        )

    pass
