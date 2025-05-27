"""Dies ist ein Startskript.

Das Skript initialisiert die Hardware und die Anwendung.
"""
# ---------------------------------------------------------------------------------------------------------------------
from hal.impl.led import OnBoardLed
from hal.impl.stdout import UartOut
from hal.interfaces.istdout import IStdOut
from hal.interfaces.ireal_time_clock import IRealTimeClock
from hal.interfaces.idigital_output import IDigitalOutput
from hal.impl.digital_output import GpioDigitalOutput
from hal.impl.digital_input import GpioiBufferedDigitalInput
from hal.impl.real_time_clock import I2CReadTimeClock, Timestamp
from time import time, mktime
from pferdinand.pferdinand import Pferdinand, Event
from hal.constants.constants import TIMER_TICK
from machine import Timer
from pferdinand.constants import (
    PFERDINAND_DIGITAL_OUTPUT_0_PIN_NUMBER,
    PFERDINAND_DIGITAL_OUTPUT_1_PIN_NUMBER,
    PFERDINAND_I2C_RTC_SDA_PIN,
    PFERDINAND_I2C_RTC_SCL_PIN,
    PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
    PFERDINAND_SWITCH_INPUT_0,
    PFERDINAND_SWITCH_INPUT_1,
    PFERDINAND_INPUT_BUFFER_SIZE,
)
from gc import collect, mem_alloc, mem_free
from application.app import App
# ---------------------------------------------------------------------------------------------------------------------

# Hardware Initialisieren...

# UART Out.
stdout: IStdOut = UartOut()
# On Board LED die Blinkt.
led: OnBoardLed = OnBoardLed()
# Initialisierung der Echtzeituhr.
rtc: IRealTimeClock = I2CReadTimeClock(
    sda_pin_number=PFERDINAND_I2C_RTC_SDA_PIN,
    scl_pin_number=PFERDINAND_I2C_RTC_SCL_PIN,
    i2c_address=PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
# Digitale Outputs.
digital_output_pin_0: IDigitalOutput = GpioDigitalOutput(
    PFERDINAND_DIGITAL_OUTPUT_0_PIN_NUMBER,
)
digital_output_pin_1: IDigitalOutput = GpioDigitalOutput(
    PFERDINAND_DIGITAL_OUTPUT_1_PIN_NUMBER,
)

# Die Anwendung zur Steuerung und Koordination der Ein- und Ausgaben.
app: App = App(
    stdout=stdout,
    rtc=rtc,
    up_input=GpioiBufferedDigitalInput(
        pin_number=PFERDINAND_SWITCH_INPUT_0,
        buffer_size=PFERDINAND_INPUT_BUFFER_SIZE,
    ),
    down_input=GpioiBufferedDigitalInput(
        pin_number=PFERDINAND_SWITCH_INPUT_1,
        buffer_size=PFERDINAND_INPUT_BUFFER_SIZE,
    ),
    up_output=digital_output_pin_0,
    down_output=digital_output_pin_1,
)

# Weitere Hardware initialisieren...
def callback(t):
    app.event_input_queue().append(
        Event.time_tick().set_timestamp(
            rtc.now()
        )
    )
    pass

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
    app.dispatch_event()
    collect()
    self.__stdout.write(f'Mem {mem_alloc()} / {mem_free()}\n')
    led.off()
# ---------------------------------------------------------------------------------------------------------------------

