from hal.interfaces.idigital_output import IDigitalOutput


class DigitalOutputMock(IDigitalOutput):

    def __init__(self):
        self.__value: bool = False
        pass

    def set(self, value: bool) -> 'Self':
        self.__value = value
        return self

    def is_set(self) -> bool:
        return self.__value

    pass
