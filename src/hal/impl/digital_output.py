# ---------------------------------------------------------------------------------------------------------------------
from hal.interfaces.idigital_output import IDigitalOutput
from machine import Pin
# ---------------------------------------------------------------------------------------------------------------------

class GpioDigitalOutput(IDigitalOutput):

    def __init__(self, pin_number: int):
        self.__pin: Pin = Pin(
            pin_number, mode=Pin.OUT, value=0
        )
        pass

    def set(self, value: bool) -> 'Self':
        if value:
            self.__pin.on()
        else:
            self.__pin.off()
        return self

    pass
# ---------------------------------------------------------------------------------------------------------------------
