# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase
from application.app import App

from test.digital_output_mock import DigitalOutputMock
from test.digital_input_mock import DigitalInputMock
from test.printout import PrintOut
from test.rtc_mock import Rtc

from hal.interfaces.types import Timestamp
from hal.impl.entangled_digital_input import EntangledDigitalInput
from pferdinand.event import Event
from pferdinand.motor import Motor
from time import localtime, time, sleep
# ---------------------------------------------------------------------------------------------------------------------

class Initial(TestCase):

    def runTest(self):
        """Test if the App can be constructed."""
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=DigitalInputMock().set(True),
            down_input=DigitalInputMock(),
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        )

        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
        )
        self.assertEqual(
            EntangledDigitalInput._00,
            app.switch().state(),
        )

        for _ in range(0, 2):
            app.event_input_queue().append(
                Event.time_tick().set_timestamp(
                    Timestamp().from_tuple(
                        localtime(
                            time()
                        )
                    )
                )
            )
            app.dispatch_event()
            sleep(1)

        self.assertEqual(
            Motor.UP,
            app.motor().state(),
        )
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------


class TwoActive(TestCase):

    def runTest(self):
        """Stellt sicher, dass der Motor bei 2 aktiven Inputs nicht anlaeuft."""
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=DigitalInputMock().set(True),
            down_input=DigitalInputMock().set(True),
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        )

        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
        )
        self.assertEqual(
            EntangledDigitalInput._00,
            app.switch().state(),
        )

        for _ in range(0, 2):
            app.event_input_queue().append(
                Event.time_tick().set_timestamp(
                    Timestamp().from_tuple(
                        localtime(
                            time()
                        )
                    )
                )
            )
            app.dispatch_event()
            sleep(1)

        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
        )
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------

class TwoActiveThenUp(TestCase):

    def runTest(self):
        """Pruefe, was passiert, wenn die Anwendung mit 2 aktiven Inputs gestartet wird.

        Dabei soll der Motor nicht angehen.
        """
        up_input = DigitalInputMock().set(True)
        down_input = DigitalInputMock().set(True)
        up_output = DigitalOutputMock()
        down_output = DigitalOutputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=down_input,
            up_output=up_output,
            down_output=down_output,
        )

        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
        )
        self.assertEqual(
            EntangledDigitalInput._00,
            app.switch().state(),
        )
        self.assertFalse(
            up_output.is_set(),
        )
        self.assertFalse(
            down_output.is_set(),
        )

        for i in range(0, 5):
            app.event_input_queue().append(
                Event.time_tick().set_timestamp(
                    Timestamp().from_tuple(
                        localtime(
                            time()
                        )
                    )
                )
            )
            app.dispatch_event()
            if i == 2:
                down_input.set(False)
            if i == 3:
                self.assertEqual(
                    Motor.UP,
                    app.motor().state(),
                )
            sleep(1)
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------

class TwoActiveTheDown(TestCase):

    def runTest(self):
        """Pruefe, was passiert, wenn die Anwendung mit 2 aktiven Inputs gestartet wird.

        Dabei soll der Motor nicht angehen.
        """
        up_input = DigitalInputMock().set(True)
        down_input = DigitalInputMock().set(True)
        up_output = DigitalOutputMock()
        down_output = DigitalOutputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=down_input,
            up_output=up_output,
            down_output=down_output,
        )

        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
        )
        self.assertEqual(
            EntangledDigitalInput._00,
            app.switch().state(),
        )
        self.assertFalse(
            up_output.is_set(),
        )
        self.assertFalse(
            down_output.is_set(),
        )

        for i in range(0, 5):
            app.event_input_queue().append(
                Event.time_tick().set_timestamp(
                    Timestamp().from_tuple(
                        localtime(
                            time()
                        )
                    )
                )
            )
            app.dispatch_event()
            if i == 2:
                up_input.set(False)
            if i == 3:
                self.assertEqual(
                    Motor.DOWN,
                    app.motor().state(),
                )
            sleep(1)
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------
