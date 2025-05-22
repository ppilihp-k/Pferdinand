# ---------------------------------------------------------------------------------------------------------------------
from machine import UART
from machine import Pin
from hal.interfaces.istdout import IStdOut
# ---------------------------------------------------------------------------------------------------------------------

class UartOut(IStdOut):

    def __init__(self):
        # Initialisierung: UART
        # UART 0, TX=GPIO0 (Pin 1), RX=GPIO1 (Pin 2)
        # UART 1, TX=GPIO4 (Pin 6), RX=GPIO5 (Pin 7)
        self.__uart: UART = UART(
            0,
            baudrate=9600,
            tx=Pin(0),
            rx=Pin(1),
            bits=8,
            parity=None,
            stop=1
        )
        pass

    def write(self, msg: str) -> 'Self':
        self.__uart.write(msg)
        return self

    pass
# ---------------------------------------------------------------------------------------------------------------------
