# ---------------------------------------------------------------------------------------------------------------------
from time import sleep
from hal.impl.entangled_digital_input import EntangledDigitalInput, EntangledCallback
from hal.interfaces.istdout import IStdOut
from hal.interfaces.ireal_time_clock import IRealTimeClock
from hal.interfaces.idigital_output import IDigitalOutput
from hal.interfaces.idigital_input import IDigitalInput
from pferdinand.pferdinand import Pferdinand, Event
from pferdinand.constants import (
    PFERDINAND_DIGITAL_OUTPUT_0_PIN_NUMBER,
    PFERDINAND_DIGITAL_OUTPUT_1_PIN_NUMBER,
    PFERDINAND_ACTIVE_TIME_MS,
    PFERDINAND_ACTIVATE_AT,
    PFERDINAND_I2C_RTC_SDA_PIN,
    PFERDINAND_I2C_RTC_SCL_PIN,
    PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
    PFERDINAND_SWITCH_INPUT_0,
    PFERDINAND_SWITCH_INPUT_1,
)
from pferdinand.motor import Motor
from hal.interfaces.types import Timestamp
# ---------------------------------------------------------------------------------------------------------------------

class SwitchCallback(EntangledCallback):

    def __init__(self, event_output_queue: list, rtc: IRealTimeClock):
        self.__rtc: IRealTimeClock = rtc
        self.__event_output_queue: list = event_output_queue
        pass

    def i0_hi(self):
        self.__event_output_queue.append(
            Event.motor_up_command().set_timestamp(self.__rtc.now())
        )
        pass

    def i0_lo(self):
        self.__event_output_queue.append(
            Event.motor_stop_command().set_timestamp(self.__rtc.now())
        )
        pass

    def i1_hi(self):
        self.__event_output_queue.append(
            Event.motor_down_command().set_timestamp(self.__rtc.now())
        )
        pass

    def i1_lo(self):
        self.__event_output_queue.append(
            Event.motor_stop_command().set_timestamp(self.__rtc.now())
        )
        pass

    def all_lo(self):
        self.__event_output_queue.append(
            Event.motor_stop_command().set_timestamp(self.__rtc.now())
        )
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------

class App:
    """Application.

    Simple encapsulation of other Components.
    """
    def __init__(
        self,
        stdout: IStdOut,
        rtc: IRealTimeClock,
        up_input: IDigitalInput,
        down_input: IDigitalInput,
        up_output: IDigitalOutput,
        down_output: IDigitalOutput,
    ):
        self.__event_input_queue: list = []
        self.__event_output_queue: list = []
        self.__pferdinant: Pferdinand = Pferdinand(
            event_input_queue=self.__event_input_queue,
            event_output_queue=self.__event_output_queue,
            rtc=rtc,
            stdout=stdout,
        ).set_active_at(
            Timestamp().from_tuple(
                PFERDINAND_ACTIVATE_AT
            )
        ).set_active_time(
            PFERDINAND_ACTIVE_TIME_MS
        )
        self.__switch: EntangledDigitalInput = EntangledDigitalInput(
            i0=up_input,
            i1=down_input,
            callback=SwitchCallback(
                event_output_queue=self.__event_output_queue,
                rtc=rtc,
            )
        )
        self.__motor: Motor = Motor(
            input_queue=self.__event_output_queue,
            up=up_output,
            down=down_output,
        )
        pass

    def set_active_at(self, active_at: Timestamp) -> 'Self':
        self.__pferdinant.set_active_at(timestamp=active_at)
        return self

    def dispatch_event(self) -> 'Self':
        self.__switch.dispatch_event()
        self.__pferdinant.dispatch_event()
        self.__motor.dispatch_event()
        return self

    def motor(self) -> Motor:
        return self.__motor

    def switch(self) -> EntangledDigitalInput:
        return self.__switch

    def event_input_queue(self) -> list:
        return self.__event_input_queue

    pass

# ---------------------------------------------------------------------------------------------------------------------

