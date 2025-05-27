"""Ein Motor.

Diese Klasse kapselt den Zugriff auf einen externen Motor der ueber GPIO Output gesteuert wird.
"""
# ---------------------------------------------------------------------------------------------------------------------
from pferdinand.event import Event
from hal.interfaces.idigital_output import IDigitalOutput
# ---------------------------------------------------------------------------------------------------------------------

class Motor:

    IDLE: int = 0
    UP: int = 1
    DOWN: int = 2

    def __init__(
        self,
        input_queue: list,
        up: IDigitalOutput,
        down: IDigitalOutput,
    ):
        self.__input_queue: list = input_queue
        self.__up: IDigitalOutput = up
        self.__down: IDigitalOutput = down
        self.__state: int = self.IDLE
        pass

    def state(self) -> int:
        return self.__state

    def __motor_up(self) -> 'Self':
        self.__down.set(False)
        self.__up.set(True)
        return self

    def __motor_down(self) -> 'Self':
        self.__up.set(False)
        self.__down.set(True)
        return self

    def __motor_stop(self) -> 'Self':
        self.__up.set(False)
        self.__down.set(False)
        return self

    def __handle_motor_up(self, event: Event) -> int:
        if Event.MOTOR_STOP_COMMAND == event.event_id():
            self.__motor_stop()
            return self.IDLE
        elif Event.MOTOR_UP_COMMAND == event.event_id():
            return self.UP
        elif Event.MOTOR_DOWN_COMMAND == event.event_id():
            self.__motor_stop()
            self.__input_queue.append(
                Event.motor_down_command()
            )
            return self.IDLE
        return self.UP

    def __handle_motor_down(self, event: Event) -> int:
        if Event.MOTOR_STOP_COMMAND == event.event_id():
            self.__motor_stop()
            return self.IDLE
        elif Event.MOTOR_UP_COMMAND == event.event_id():
            self.__motor_stop()
            self.__input_queue.append(
                Event.motor_up_command()
            )
            return self.IDLE
        elif Event.MOTOR_DOWN_COMMAND == event.event_id():
            return self.DOWN
        return self.DOWN

    def __handle_motor_idle(self, event: Event) -> int:
        if Event.MOTOR_STOP_COMMAND == event.event_id():
            self.__motor_stop()
            return self.IDLE
        elif Event.MOTOR_UP_COMMAND == event.event_id():
            self.__motor_up()
            return self.UP
        elif Event.MOTOR_DOWN_COMMAND == event.event_id():
            self.__motor_down()
            return self.DOWN
        return self.IDLE

    def dispatch_event(self) -> 'Self':
        if len(self.__input_queue) > 0:
            event: Event = self.__input_queue.pop()
            if self.IDLE == self.__state:
                self.__state = self.__handle_motor_idle(event)
            elif self.UP == self.__state:
                self.__state = self.__handle_motor_up(event)
            elif self.DOWN == self.__state:
                self.__state = self.__handle_motor_down(event)
            else:
                pass
        return self

    pass
# ---------------------------------------------------------------------------------------------------------------------
