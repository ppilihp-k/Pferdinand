
from hal.interfaces.idigital_input import IDigitalInput


class EntangledCallback:

    def i0_hi(self):
        pass

    def i0_lo(self):
        pass

    def i1_hi(self):
        pass

    def i1_lo(self):
        pass

    def all_lo(self):
        pass
    pass


class EntangledDigitalInput:

    _00: int = 0
    _01: int = 1
    _10: int = 2

    def __init__(
        self,
        i0: IDigitalInput,
        i1: IDigitalInput,
        callback: EntangledCallback,
    ):
        self.__i0: IDigitalInput = i0
        self.__i1: IDigitalInput = i1
        self.__state: int = self._00
        self.__callback: EntangledCallback = callback
        pass

    def state(self) -> int:
        return self.__state

    def __handle_00(self, v0: bool, v1: bool) -> int:
        if not v0 and not v1:
            return self._00
        elif v0 and not v1:
            self.__callback.i0_hi()
            return self._10
        elif not v0 and v1:
            self.__callback.i1_hi()
            return self._01
        else:
            # v0 and v1 should stop everything!
            return self._00

    def __handle_01(self, v0: bool, v1: bool) -> int:
        if not v0 and not v1:
            self.__callback.i1_lo()
            return self._00
        elif v0 and not v1:
            self.__callback.i1_lo()
            return self._00
        elif not v0 and v1:
            return self._01
        else:
            self.__callback.i1_lo()
            return self._00

    def __handle_10(self, v0: bool, v1: bool) -> int:
        if not v0 and not v1:
            self.__callback.i0_lo()
            return self._00
        elif v0 and not v1:
            return self._10
        elif not v0 and v1:
            self.__callback.i0_lo()
            return self._00
        else:
            self.__callback.i0_lo()
            return self._00

    def dispatch_event(self) -> 'Self':
        v0: bool = self.__i0.value()
        v1: bool = self.__i1.value()
        if self._00 == self.__state:
            self.__state = self.__handle_00(v0, v1)
        elif self._01 == self.__state:
            self.__state = self.__handle_01(v0, v1)
        else:
            self.__state = self.__handle_10(v0, v1)
        return self

    pass
