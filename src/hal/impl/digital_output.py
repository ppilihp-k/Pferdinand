# ---------------------------------------------------------------------------------------------------------------------
from hal.interfaces.idigital_output import IDigitalOutput
from machine import Pin
# ---------------------------------------------------------------------------------------------------------------------

class GpioDigitalOutput(IDigitalOutput):

    def __init__(self, pin_number: int, pin_value: int=0):
        self.__pin: Pin = Pin(
            pin_number, mode=Pin.OUT, value=pin_value,
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

class InvertedGpioDigitalOutput(IDigitalOutput):

    def __init__(self, pin_number: int):
        self.__digital_output: IDigitalOutput = GpioDigitalOutput(
            pin_number=pin_number, pin_value=1,
        )
        pass

    def set(self, value: bool) -> 'Self':
        return self.__digital_output.set(not value)

    pass
# ---------------------------------------------------------------------------------------------------------------------
