# ---------------------------------------------------------------------------------------------------------------------
from pferdinand.pferdinand import Pferdinand, Event
from unittest import TestCase
from test.printout import PrintOut
from test.digital_output_mock import DigitalOutputMock
from time import time, mktime, localtime, sleep
from hal.interfaces.types import Timestamp
# ---------------------------------------------------------------------------------------------------------------------

class TestInitial(TestCase):

    def double_dabble1(self, number: int) -> int:
        number = number & 0xFF
        scratch = 0
        for i in range(0, 8):
            number = number << 1
            scratch = (scratch << 1) | ((number >> 8) & 0x1)
            hundrets = (scratch >> 8) & 0xF
            tens = (scratch >> 4) & 0xF
            ones = scratch & 0xF
            if ones >= 5:
                ones = ones + 3
            if tens >= 5:
                tens = tens + 3
            if hundrets >= 5:
                hundrets = hundrets + 3
            scratch = (hundrets << 8) | (tens << 4) | ones
        return scratch

    def double_dabble(self, bin_value) -> int:
        for i in range(0, 8):
            # Multiply by 2
            bin_value = bin_value << 1

            # Final op is always a shift, so break out when done
            if i == 7: break

            # If the BCD units value (bits 8-11)  is 5 or more, add 3
            if (bin_value & 0xF00) > 0x4FF: bin_value += 0x300

            # If the BCD tens value (bits 12-15) is 5 or more, add 3
            if (bin_value & 0xF000) > 0x4FFF: bin_value += 0x3000
        return (bin_value >> 8) & 0xFF

    def runTest(self):
        #self.assertEqual(
        #    579,
        #    self.double_dabble(243)
        #)
        self.assertEqual(
            37,
            self.double_dabble(25)
        )
        self.assertEqual(
            80,
            self.double_dabble(50)
        )
        pass
    pass
# ---------------------------------------------------------------------------------------------------------------------

