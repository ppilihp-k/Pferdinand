from hal.interfaces.idigital_input import IDigitalInput


class DigitalInputMock(IDigitalInput):

    def __init__(self):
        self.__value: bool = False
        pass

    def set(self, value: bool) -> 'Self':
        self.__value = value
        return self

    def value(self) -> bool:
        return self.__value

    pass
