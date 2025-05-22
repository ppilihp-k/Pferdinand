# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from hal.interfaces.types import Timestamp
# ---------------------------------------------------------------------------------------------------------------------

class IRealTimeClock:

    @abstractmethod
    def set_time(self, timestamp: Timestamp) -> 'Self':
        pass

    @abstractmethod
    def now(self) -> Timestamp:
        pass
# ---------------------------------------------------------------------------------------------------------------------
