
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
            up_input=DigitalInputMock(),
            down_input=DigitalInputMock(),
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
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
            sleep(1)
            app.dispatch_event()

        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
        )
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------

class Up(TestCase):

    def runTest(self):
        """If up Button is pressed start the Motor in up Direction."""
        up_input: DigitalInputMock = DigitalInputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=DigitalInputMock(),
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        )

        for i in range(0, 10):
            if i == 4:
                up_input.set(True)
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
            EntangledDigitalInput._10,
            app.switch().state(),
            f'Switch State was: {app.switch().state()}'
        )
        self.assertEqual(
            Motor.UP,
            app.motor().state(),
            f'Motor State was: {app.motor().state()}'
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------


class Down(TestCase):

    def runTest(self):
        """If down Button is pressed start the Motor in down Direction."""
        up_input: DigitalInputMock = DigitalInputMock()
        down_input: DigitalInputMock = DigitalInputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=down_input,
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        )

        for i in range(0, 10):
            if i == 4:
                down_input.set(True)
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
            EntangledDigitalInput._01,
            app.switch().state(),
            f'Switch State was: {app.switch().state()}'
        )
        self.assertEqual(
            Motor.DOWN,
            app.motor().state(),
            f'Motor State was: {app.motor().state()}'
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------


class UpDown(TestCase):

    def runTest(self):
        """Up Button is pressed, if down Button is pressed later, stop the Motor."""
        up_input: DigitalInputMock = DigitalInputMock()
        down_input: DigitalInputMock = DigitalInputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=down_input,
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        )

        for i in range(0, 10):
            if i == 3:
                up_input.set(True)
            if i == 4:
                down_input.set(True)
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
            EntangledDigitalInput._00,
            app.switch().state(),
            f'Switch State was: {app.switch().state()}'
        )
        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
            f'Motor State was: {app.motor().state()}'
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------


class DownUp(TestCase):

    def runTest(self):
        """Down Button is pressed, if up Button is pressed later, stop the Motor."""
        up_input: DigitalInputMock = DigitalInputMock()
        down_input: DigitalInputMock = DigitalInputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=down_input,
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        )

        for i in range(0, 10):
            if i == 3:
                down_input.set(True)
            if i == 4:
                up_input.set(True)
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
            EntangledDigitalInput._00,
            app.switch().state(),
            f'Switch State was: {app.switch().state()}'
        )
        self.assertEqual(
            Motor.IDLE,
            app.motor().state(),
            f'Motor State was: {app.motor().state()}'
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class UpInputWhileActive(TestCase):

    def runTest(self):
        """If automatic Mode is active an up Button is pressed, stop the motor."""
        up_input: DigitalInputMock = DigitalInputMock()
        down_input: DigitalInputMock = DigitalInputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=down_input,
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        ).set_active_at(
            active_at=Timestamp().from_tuple(
                localtime(time() + 3)
            )
        )

        for i in range(0, 10):
            if i == 4:
                up_input.set(True)
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
            f'Motor State was: {app.motor().state()}'
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class DownInputWhileActive(TestCase):

    def runTest(self):
        """If automatic Mode is active an down Button is pressed, stop the motor."""
        up_input: DigitalInputMock = DigitalInputMock()
        down_input: DigitalInputMock = DigitalInputMock()
        app: App = App(
            stdout=PrintOut(),
            rtc=Rtc(),
            up_input=up_input,
            down_input=down_input,
            up_output=DigitalOutputMock(),
            down_output=DigitalOutputMock(),
        ).set_active_at(
            active_at=Timestamp().from_tuple(
                localtime(time() + 3)
            )
        )

        for i in range(0, 10):
            if i == 4:
                down_input.set(True)
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
            Motor.DOWN,
            app.motor().state(),
            f'Motor State was: {app.motor().state()}'
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
