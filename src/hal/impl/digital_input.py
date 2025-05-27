# ---------------------------------------------------------------------------------------------------------------------
from hal.interfaces.idigital_output import IDigitalOutput
from machine import Pin
# ---------------------------------------------------------------------------------------------------------------------

class GpioDigitalInput(IDigitalOutput):

    def __init__(self, pin_number: int):
        self.__pin: Pin = Pin(
            pin_number,
            mode=Pin.IN,
            pull=Pin.PULL_DOWN,
        )
        pass

    def value(self) -> bool:
        return self.__pin.value() == 1

    pass
# ---------------------------------------------------------------------------------------------------------------------

class GpioiBufferedDigitalInput(IDigitalOutput):

    def __init__(self, pin_number: int, buffer_size: int):
        self.__pin: Pin = Pin(
            pin_number,
            mode=Pin.IN,
            pull=Pin.PULL_UP,
        )
        self.__buffer: int = 0
        self.__buffer_size: int = buffer_size
        pass

    def value(self) -> bool:
        value: int= self.__pin.value()
        self.__buffer = self.__buffer + 1 * value - 1 * (1 - value)
        return ((self.__buffer / self.__buffer_size) >= 0.5)

    pass
# ---------------------------------------------------------------------------------------------------------------------
