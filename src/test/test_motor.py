
# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase
from test.digital_output_mock import DigitalOutputMock, IDigitalOutput
from pferdinand.event import Event
from pferdinand.motor import Motor
# ---------------------------------------------------------------------------------------------------------------------


class Initial(TestCase):

    def runTest(self):
        queue: list = []
        up: IDigitalOutput = DigitalOutputMock()
        down: IDigitalOutput = DigitalOutputMock()
        motor: Motor = Motor(
            input_queue=queue,
            up=up,
            down=down,
        )
        self.assertEqual(
            Motor.IDLE, motor.state()
        )
        self.assertFalse(
            up.is_set()
        )
        self.assertFalse(
            down.is_set()
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class Up(TestCase):

    def runTest(self):
        queue: list = []
        up: IDigitalOutput = DigitalOutputMock()
        down: IDigitalOutput = DigitalOutputMock()
        motor: Motor = Motor(
            input_queue=queue,
            up=up,
            down=down,
        )

        queue.append(
            Event.motor_up_command()
        )
        motor.dispatch_event()

        self.assertEqual(
            Motor.UP, motor.state()
        )
        self.assertTrue(
            up.is_set()
        )
        self.assertFalse(
            down.is_set()
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class Down(TestCase):

    def runTest(self):
        queue: list = []
        up: IDigitalOutput = DigitalOutputMock()
        down: IDigitalOutput = DigitalOutputMock()
        motor: Motor = Motor(
            input_queue=queue,
            up=up,
            down=down,
        )

        queue.append(
            Event.motor_down_command()
        )
        motor.dispatch_event()

        self.assertEqual(
            Motor.DOWN, motor.state()
        )
        self.assertFalse(
            up.is_set()
        )
        self.assertTrue(
            down.is_set()
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class UpDown(TestCase):

    def runTest(self):
        queue: list = []
        up: IDigitalOutput = DigitalOutputMock()
        down: IDigitalOutput = DigitalOutputMock()
        motor: Motor = Motor(
            input_queue=queue,
            up=up,
            down=down,
        )

        queue.append(
            Event.motor_up_command()
        )
        queue.append(
            Event.motor_down_command()
        )
        motor.dispatch_event()
        motor.dispatch_event()

        self.assertEqual(
            Motor.IDLE, motor.state()
        )
        self.assertFalse(
            up.is_set()
        )
        self.assertFalse(
            down.is_set()
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class DownUp(TestCase):

    def runTest(self):
        queue: list = []
        up: IDigitalOutput = DigitalOutputMock()
        down: IDigitalOutput = DigitalOutputMock()
        motor: Motor = Motor(
            input_queue=queue,
            up=up,
            down=down,
        )

        queue.append(
            Event.motor_down_command()
        )
        queue.append(
            Event.motor_up_command()
        )
        motor.dispatch_event()
        motor.dispatch_event()

        self.assertEqual(
            Motor.IDLE, motor.state()
        )
        self.assertFalse(
            up.is_set()
        )
        self.assertFalse(
            down.is_set()
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
