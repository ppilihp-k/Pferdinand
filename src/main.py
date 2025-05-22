# ---------------------------------------------------------------------------------------------------------------------
from time import sleep
from hal.led import OnBoardLed
from hal.impl.stdout import UartOut
from hal.interfaces.istdout import IStdOut
from hal.interfaces.ireal_time_clock import IRealTimeClock
from hal.interfaces.idigital_output import IDigitalOutput
from hal.impl.digital_output import GpioDigitalOutput
from hal.impl.real_time_clock import I2CReadTimeClock, RealTimeClock, Timestamp
from time import time, mktime
from pferdinand.pferdinand import Pferdinand, Event
from hal.constants import TIMER_TICK
from hal.interfaces.istdout import StdOut
from machine import Timer
from pferdinand.constants import PFERDINAND_DIGITAL_OUTPUT_PIN_NUMBER
# ---------------------------------------------------------------------------------------------------------------------


# Hardware Initialisieren...
stdout: IStdOut = UartOut()
led: OnBoardLed = OnBoardLed()
rtc: IRealTimeClock = RealTimeClock().set_time(
    I2CReadTimeClock().now()
)
digital_output_pin_0: IDigitalOutput = GpioDigitalOutput(
    PFERDINAND_DIGITAL_OUTPUT_PIN_NUMBER
)

event_queue: list = []

def callback(t):
    event_queue.append(
        Event.time_tick().set_timestamp(
            rtc.now().mktime()
    )
    pass

# Anwendung bauen...
app: Pferdinand = Pferdinand(
    digital_output=digital_output_pin_0,
    stdout=stdout,
).set_active_at(
    Timestamp().from_tuple(
        # (Jahr, Monat, Tag, Stunde, Minute, Sekunde, Wochentag)
        (0, 0, 0, 17, 17, 0, 0)
    )
).set_active_time(
    5000
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

