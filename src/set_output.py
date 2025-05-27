# ---------------------------------------------------------------------------------------------------------------------
from time import sleep
from hal.impl.led import OnBoardLed
from hal.impl.stdout import UartOut
from hal.impl.real_time_clock import I2CReadTimeClock, RealTimeClock, Timestamp
from pferdinand.constants import (
    PFERDINAND_ACTIVE_TIME_MS,
    PFERDINAND_ACTIVATE_AT,
    PFERDINAND_I2C_RTC_SDA_PIN,
    PFERDINAND_I2C_RTC_SCL_PIN,
    PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
from machine import Pin
# ---------------------------------------------------------------------------------------------------------------------

led: OnBoardLed = OnBoardLed()

pin_number_0: int = 2
pin_number_1: int = 3
p0: Pin = Pin(pin_number_0, mode=Pin.OUT, value=False)
p1: Pin = Pin(pin_number_1, mode=Pin.OUT, pull=None, value=False)

# spin...
while 1:
    sleep(1)
    led.on()
    p0.on()
    p1.off()
    sleep(1)
    led.off()
    p0.off()
    p1.on()

# ---------------------------------------------------------------------------------------------------------------------
