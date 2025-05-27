
# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase
from hal.impl.entangled_digital_input import EntangledDigitalInput, EntangledCallback
from hal.interfaces.idigital_input import IDigitalInput
# ---------------------------------------------------------------------------------------------------------------------

class TestDigitalInput(IDigitalInput):

    def __init__(self, value: bool):
        self.__value: bool = value
        pass

    def set(self, value: bool) -> 'Self':
        self.__value = value
        return self

    def value(self) -> bool:
        return self.__value

    pass
# ---------------------------------------------------------------------------------------------------------------------

class TestEntagledCallback(EntangledCallback):

    def __init__(self, event_output_queue: list):
        self.__queue: list = event_output_queue
        pass

    def i0_hi(self):
        self.__queue.insert(0, 1)
        pass

    def i0_lo(self):
        self.__queue.insert(0, 0)
        pass

    def i1_hi(self):
        self.__queue.insert(0, 2)
        pass

    def i1_lo(self):
        self.__queue.insert(0, 0)
        pass

    def all_lo(self):
        self.__queue.insert(0, 0)
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------

class Initial(TestCase):

    def runTest(self):

        output_queue: list = []
        entangled_input: EntangledDigitalInput = EntangledDigitalInput(
            i0=TestDigitalInput(False),
            i1=TestDigitalInput(False),
            callback=TestEntagledCallback(output_queue),
        )

        entangled_input.dispatch_event()
        self.assertEqual(
            0,
            len(output_queue),
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class Test10(TestCase):

    def runTest(self):

        output_queue: list = []
        entangled_input: EntangledDigitalInput = EntangledDigitalInput(
            i0=TestDigitalInput(True),
            i1=TestDigitalInput(False),
            callback=TestEntagledCallback(output_queue),
        )

        entangled_input.dispatch_event()
        self.assertEqual(
            1,
            len(output_queue),
        )
        self.assertEqual(
            1,
            output_queue[0]
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class Test01(TestCase):

    def runTest(self):

        output_queue: list = []
        entangled_input: EntangledDigitalInput = EntangledDigitalInput(
            i0=TestDigitalInput(False),
            i1=TestDigitalInput(True),
            callback=TestEntagledCallback(output_queue),
        )

        entangled_input.dispatch_event()
        self.assertEqual(
            1,
            len(output_queue),
        )
        self.assertEqual(
            2,
            output_queue[0]
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class Test11(TestCase):

    def runTest(self):

        output_queue: list = []
        entangled_input: EntangledDigitalInput = EntangledDigitalInput(
            i0=TestDigitalInput(True),
            i1=TestDigitalInput(True),
            callback=TestEntagledCallback(output_queue),
        )

        entangled_input.dispatch_event()
        self.assertEqual(
            0,
            len(output_queue),
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class Test1011(TestCase):

    def runTest(self):

        i0: TestDigitalInput = TestDigitalInput(True)
        i1: TestDigitalInput =TestDigitalInput(False)
        output_queue: list = []
        entangled_input: EntangledDigitalInput = EntangledDigitalInput(
            i0=i0,
            i1=i1,
            callback=TestEntagledCallback(output_queue),
        )

        entangled_input.dispatch_event()
        i1.set(True)
        entangled_input.dispatch_event()

        self.assertEqual(
            2,
            len(output_queue),
        )
        self.assertEqual(
            0,
            output_queue[0],
        )
        self.assertEqual(
            1,
            output_queue[1],
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------

class Test0111(TestCase):

    def runTest(self):

        i0: TestDigitalInput = TestDigitalInput(False)
        i1: TestDigitalInput =TestDigitalInput(True)
        output_queue: list = []
        entangled_input: EntangledDigitalInput = EntangledDigitalInput(
            i0=i0,
            i1=i1,
            callback=TestEntagledCallback(output_queue),
        )

        entangled_input.dispatch_event()
        i0.set(True)
        entangled_input.dispatch_event()

        self.assertEqual(
            2,
            len(output_queue),
        )
        self.assertEqual(
            0,
            output_queue[0],
        )
        self.assertEqual(
            2,
            output_queue[1],
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
