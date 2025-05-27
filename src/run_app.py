# ---------------------------------------------------------------------------------------------------------------------
from time import sleep
from hal.impl.led import OnBoardLed
from hal.impl.stdout import UartOut
from hal.impl.entangled_digital_input import EntangledDigitalInput, EntangledCallback
from hal.interfaces.istdout import IStdOut
from hal.interfaces.ireal_time_clock import IRealTimeClock
from hal.interfaces.idigital_output import IDigitalOutput
from hal.interfaces.idigital_input import IDigitalInput
from hal.impl.digital_output import GpioDigitalOutput
from hal.impl.digital_input import GpioiBufferedDigitalInput
from hal.impl.real_time_clock import I2CReadTimeClock, RealTimeClock, Timestamp
from time import time, mktime
from pferdinand.pferdinand import Pferdinand, Event
from hal.constants.constants import TIMER_TICK
from machine import Timer
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
# ---------------------------------------------------------------------------------------------------------------------

event_queue: list = []
motor_event_queue: list = []

# ---------------------------------------------------------------------------------------------------------------------

class SwitchCallback(EntangledCallback):

    def __init__(self, event_output_queue: list, rtc: IRealTimeClock):
        self.__rtc: IRealTimeClock = rtc
        self.__event_output_queue: list = event_output_queue
        pass

    def i0_hi(self):
        self.__event_output_queue.append(
            Event.motor_up_command().set_timestamp(rtc.now())
        )
        pass

    def i0_lo(self):
        self.__event_output_queue.append(
            Event.motor_stop_command().set_timestamp(rtc.now())
        )
        pass

    def i1_hi(self):
        self.__event_output_queue.append(
            Event.motor_down_command().set_timestamp(rtc.now())
        )
        pass

    def i1_lo(self):
        self.__event_output_queue.append(
            Event.motor_stop_command().set_timestamp(rtc.now())
        )
        pass

    def all_lo(self):
        self.__event_output_queue.append(
            Event.motor_stop_command().set_timestamp(rtc.now())
        )
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------

# Hardware Initialisieren...
stdout: IStdOut = UartOut()
led: OnBoardLed = OnBoardLed()
rtc: IRealTimeClock = I2CReadTimeClock(
    sda_pin_number=PFERDINAND_I2C_RTC_SDA_PIN,
    scl_pin_number=PFERDINAND_I2C_RTC_SCL_PIN,
    i2c_address=PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
digital_output_pin_0: IDigitalOutput = GpioDigitalOutput(
    PFERDINAND_DIGITAL_OUTPUT_0_PIN_NUMBER,
)
digital_output_pin_1: IDigitalOutput = GpioDigitalOutput(
    PFERDINAND_DIGITAL_OUTPUT_1_PIN_NUMBER,
)

#
# Pull-Up on Inputpin.
#	Default: 1
#	Switch on -> 0
#
switch_input: EntangledDigitalInput = EntangledDigitalInput(
    i0=GpioiBufferedDigitalInput(
        pin_number=PFERDINAND_SWITCH_INPUT_0,
        buffer_size=32,
    ),
    i1=GpioiBufferedDigitalInput(
        pin_number=PFERDINAND_SWITCH_INPUT_1,
        buffer_size=32,
    ),
    callback=SwitchCallback(
        event_output_queue=event_queue,
        rtc=rtc,
    ),
)

def callback(t):
    event_queue.append(
        Event.time_tick().set_timestamp(
            rtc.now()
        )
    )
    pass

# Anwendung bauen...
app: Pferdinand = Pferdinand(
    event_input_queue=event_queue,
    event_output_queue=motor_event_queue,
    stdout=stdout,
).set_active_at(
    Timestamp().from_tuple(
        PFERDINAND_ACTIVATE_AT
    )
).set_active_time(
    PFERDINAND_ACTIVE_TIME_MS
)

# Weitere Hardware initialisieren...
# (Timer darf nicht los laufen bevor nicht die Anwendung initialisiert wurde)
timer: Timer = Timer()
timer.init(
    mode=Timer.PERIODIC,
    freq=1000/TIMER_TICK,
    callback=callback
)

# Anwendung ausfuehren...
stdout.write('Hello World!\n')
while True:
    led.on()
    switch_input.dispatch_event()
    #if len(event_queue) > 0:
    #    print(event_queue.pop())
    app.dispatch_event()
    led.off()
# ---------------------------------------------------------------------------------------------------------------------

