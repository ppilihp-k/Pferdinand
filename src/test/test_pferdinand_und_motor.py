# ---------------------------------------------------------------------------------------------------------------------
from time import time, mktime, localtime, sleep
from pferdinand.pferdinand import Pferdinand, Event
from pferdinand.motor import Motor
from unittest import TestCase
from test.printout import PrintOut
from test.digital_output_mock import DigitalOutputMock, IDigitalOutput
from time import time, mktime, localtime, sleep
from hal.interfaces.types import Timestamp
from test.rtc_mock import Rtc
# ---------------------------------------------------------------------------------------------------------------------

class TestInitial(TestCase):

    def runTest(self):
        """Prueft den Initialen Zustand ab."""
        event_input_queue: list = []
        event_output_queue: list = []
        p: Pferdinand = Pferdinand(
            event_input_queue,
            event_output_queue,
            Rtc(),
            PrintOut(),
        )
        up: IDigitalOutput = DigitalOutputMock()
        down: IDigitalOutput = DigitalOutputMock()
        motor: Motor = Motor(
            event_output_queue,
            up,
            down,
        )

        event_input_queue.append(
            Event.motor_down_command().set_timestamp(
                Timestamp().from_tuple(
                    localtime(time())
                )
            )
        )
        event_input_queue.append(
            Event.time_tick().set_timestamp(
                Timestamp().from_tuple(
                    localtime(time())
                )
            )
        )

        while len(event_input_queue) > 0 or len(event_output_queue) > 0:
            p.dispatch_event()
            motor.dispatch_event()

        self.assertEqual(
            Motor.DOWN,
            motor.state()
        )
        pass
# ---------------------------------------------------------------------------------------------------------------------
