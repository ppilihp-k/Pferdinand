# ---------------------------------------------------------------------------------------------------------------------
from hal.interfaces.types import Timestamp
from hal.interfaces.istdout import StdOut
from time import localtime

# ---------------------------------------------------------------------------------------------------------------------

class Event:

    TIME_TICK: int = 0

    def __init__(self, event_id: int):
        self.__event_id: int = event_id
        self.__timestamp: int = 0
        pass

    def event_id(self) -> int:
        return self.__event_id

    def set_timestamp(self, timestamp: int) -> 'Self':
        self.__timestamp = timestamp
        return self

    def timestamp(self) -> Timestamp:
        return Timestamp().from_tuple(
            localtime(self.__timestamp)
        )

    @staticmethod
    def time_tick() -> 'Event':
        return Event(
            event_id=Event.TIME_TICK
        )

    pass
# ---------------------------------------------------------------------------------------------------------------------



class Pferdinand:

    WAITING: int = 0
    ACTIVE: int = 1

    def __init__(self, stdout: StdOut):
        self.__stdout: StdOut = stdout

        self.__active_at: Timestamp = Timestamp()
        self.__active_time_ms: int = 3000

        self.__activated_at: int = 0

        self.__state: int = Pferdinand.WAITING
        pass

    def state(self) -> int:
        return self.__state

    def __set_state(self, state: int) -> 'Self':
        self.__state = state
        return self

    def __handle_waiting_state(self, event: Event) -> int:
        if Event.TIME_TICK == event.event_id():
            timestamp: Timestamp = event.timestamp()
            if timestamp.hours() == self.__active_at.hours() and timestamp.minutes() == self.__active_at.minutes() and timestamp.seconds() == self.__active_at.seconds():
                self.__stdout.write('Switch to Active Mode.')
                self.__activated_at = timestamp.mktime()
                return Pferdinand.ACTIVE
            return Pferdinand.WAITING
        else:
            return Pferdinand.WAITING

    def __handle_active_state(self, event: Event) -> int:
        if Event.TIME_TICK == event.event_id():
            if (event.timestamp().mktime() - self.__activated_at) >= (self.__active_time_ms / 1000):
                self.__stdout.write('Switch to Waiting Mode.')
                return Pferdinand.WAITING
            return Pferdinand.ACTIVE
        else:
            return Pferdinand.ACTIVE

    def dispatch_event(self, event: Event) -> 'Self':
        if Pferdinand.WAITING == self.state():
            self.__set_state(
                self.__handle_waiting_state(event)
            )
        elif Pferdinand.ACTIVE  == self.state():
            self.__set_state(
                self.__handle_active_state(event)
            )
        else:
            self.__set_state(
                Pferdinand.WAITING
            )
        return self

    def set_active_at(self, timestamp: Timestamp) -> 'Self':
        self.__active_at = timestamp
        return self

    def set_active_time(self, time_in_ms: int) -> 'Self':
        self.__active_time_ms = time_in_ms
        return self

    pass
# ---------------------------------------------------------------------------------------------------------------------
