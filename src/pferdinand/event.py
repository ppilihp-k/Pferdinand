"""Ein Event.

Diese Klasse kapselt Informationen zu einem aufgetretenden Event, wie Zeitstempel und Id.
"""
# ---------------------------------------------------------------------------------------------------------------------
from hal.interfaces.types import Timestamp
# ---------------------------------------------------------------------------------------------------------------------

class Event:

    TIME_TICK: int = 0
    MOTOR_UP_COMMAND: int = 1
    MOTOR_DOWN_COMMAND: int = 2
    MOTOR_STOP_COMMAND: int = 3

    def __init__(self, event_id: int):
        self.__event_id: int = event_id
        self.__timestamp: Timestamp = Timestamp()
        pass

    def event_id(self) -> int:
        return self.__event_id

    def set_timestamp(self, timestamp: Timestamp) -> 'Self':
        self.__timestamp = timestamp
        return self

    def timestamp(self) -> Timestamp:
        return self.__timestamp

    @staticmethod
    def event_name(event_id: int) -> str:
        if Event.TIME_TICK == event_id:
            return 'TIME_TICK'
        elif Event.MOTOR_UP_COMMAND == event_id:
            return 'MOTOR_UP_COMMAND'
        elif Event.MOTOR_DOWN_COMMAND == event_id:
            return 'MOTOR_DOWN_COMMAND'
        elif Event.MOTOR_STOP_COMMAND == event_id:
            return 'MOTOR_STOP_COMMAND'
        else:
            return 'None'

    def __str__(self) -> str:
        return '{' + f'"event_id":{self.event_name(self.__event_id)},"timestamp":{self.__timestamp}' + '}'

    @staticmethod
    def motor_up_command() -> 'Event':
        return Event(
            event_id=Event.MOTOR_UP_COMMAND
        )

    @staticmethod
    def motor_down_command() -> 'Event':
        return Event(
            event_id=Event.MOTOR_DOWN_COMMAND
        )

    @staticmethod
    def motor_stop_command() -> 'Event':
        return Event(
            event_id=Event.MOTOR_STOP_COMMAND
        )

    @staticmethod
    def time_tick() -> 'Event':
        return Event(
            event_id=Event.TIME_TICK
        )
    pass
# ---------------------------------------------------------------------------------------------------------------------
