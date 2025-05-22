# ---------------------------------------------------------------------------------------------------------------------
from time import sleep
from hal.impl.led import OnBoardLed
from hal.impl.stdout import UartOut
from hal.interfaces.istdout import IStdOut
from hal.interfaces.ireal_time_clock import IRealTimeClock
from hal.interfaces.idigital_output import IDigitalOutput
from hal.impl.digital_output import GpioDigitalOutput
from hal.impl.real_time_clock import I2CReadTimeClock, RealTimeClock, Timestamp
from time import time, mktime
from pferdinand.pferdinand import Pferdinand, Event
from hal.constants.constants import TIMER_TICK
from machine import Timer
from pferdinand.constants import (
    PFERDINAND_DIGITAL_OUTPUT_PIN_NUMBER,
    PFERDINAND_ACTIVE_TIME_MS,
    PFERDINAND_ACTIVATE_AT,
    PFERDINAND_I2C_RTC_SDA_PIN,
    PFERDINAND_I2C_RTC_SCL_PIN,
    PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
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
    PFERDINAND_DIGITAL_OUTPUT_PIN_NUMBER
)

event_queue: list = []

def callback(t):
    event_queue.append(
        Event.time_tick().set_timestamp(
            rtc.now()
        )
    )
    pass

# Anwendung bauen...
app: Pferdinand = Pferdinand(
    digital_output=digital_output_pin_0,
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
while True:
    if len(event_queue) > 0:
        led.on()
        event: Event = event_queue.pop()
        app.dispatch_event(
            event
        )
        led.off()
# ---------------------------------------------------------------------------------------------------------------------

