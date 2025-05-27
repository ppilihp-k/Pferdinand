# ---------------------------------------------------------------------------------------------------------------------
from hal.interfaces.types import Timestamp
from hal.interfaces.istdout import IStdOut
from hal.interfaces.idigital_output import IDigitalOutput
from hal.interfaces.ireal_time_clock import IRealTimeClock
from time import localtime
from pferdinand.event import Event

# ---------------------------------------------------------------------------------------------------------------------

class Pferdinand:

    WAITING: int = 0
    ACTIVE: int = 1

    def __init__(self, event_input_queue: list, event_output_queue: list, rtc: IRealTimeClock, stdout: IStdOut):
        self.__stdout: IStdOut = stdout
        self.__rtc: IRealTimeClock = rtc
        self.__event_input_queue: list = event_input_queue
        self.__event_output_queue: list = event_output_queue

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

    def __motor_up(self) -> 'Self':
        self.__event_output_queue.append(
            Event.motor_up_command().set_timestamp(
                self.__rtc.now(),
            )
        )
        return self

    def __motor_down(self) -> 'Self':
        self.__event_output_queue.append(
            Event.motor_down_command().set_timestamp(
                self.__rtc.now(),
            )
        )
        return self

    def __motor_stop(self) -> 'Self':
        self.__event_output_queue.append(
            Event.motor_stop_command().set_timestamp(
                self.__rtc.now(),
            )
        )
        return self

    def __handle_waiting_state(self, event: Event) -> int:
        if Event.TIME_TICK == event.event_id():
            #self.__stdout.write(f'Tick {event.timestamp()}.\n')
            timestamp: Timestamp = event.timestamp()
            if timestamp.hours() == self.__active_at.hours() and timestamp.minutes() == self.__active_at.minutes() and timestamp.seconds() == self.__active_at.seconds():
                self.__stdout.write('Switch to Active Mode.\n')
                self.__activated_at = timestamp.mktime()
                self.__motor_up()
                return Pferdinand.ACTIVE
            return Pferdinand.WAITING
        elif Event.MOTOR_UP_COMMAND == event.event_id():
            self.__motor_up()
            return Pferdinand.WAITING
        elif Event.MOTOR_DOWN_COMMAND == event.event_id():
            self.__motor_down()
            return Pferdinand.WAITING
        elif Event.MOTOR_STOP_COMMAND == event.event_id():
            self.__motor_stop()
            return Pferdinand.WAITING
        else:
            return Pferdinand.WAITING

    def __handle_active_state(self, event: Event) -> int:
        if Event.TIME_TICK == event.event_id():
            #self.__stdout.write(f'Tick {event.timestamp()}.\n')
            if event.timestamp().mktime() > (self.__activated_at + (self.__active_time_ms / 1000)):
                self.__stdout.write('Switch to Waiting Mode.\n')
                self.__motor_stop()
                return Pferdinand.WAITING
            return Pferdinand.ACTIVE
        elif Event.MOTOR_UP_COMMAND == event.event_id():
            self.__motor_stop()
            return Pferdinand.WAITING
        elif Event.MOTOR_DOWN_COMMAND == event.event_id():
            self.__motor_stop()
            return Pferdinand.WAITING
        elif Event.MOTOR_STOP_COMMAND == event.event_id():
            self.__motor_stop()
            return Pferdinand.WAITING
        else:
            return Pferdinand.ACTIVE

    def dispatch_event(self) -> 'Self':
        if len(self.__event_input_queue) > 0:
            event: Event = self.__event_input_queue.pop()
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
