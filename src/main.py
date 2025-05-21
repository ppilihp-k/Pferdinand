
from time import sleep
from hal.led import OnBoardLed
from hal.stdout import StdOut
from hal.real_time_clock import RealTimeClock, Timestamp
from time import time, mktime
from pferdinand.pferdinand import Pferdinand, Event
from hal.constants import TIMER_TICK

from machine import Timer


# Hardware Initialisieren...
stdout: StdOut = StdOut()
led: OnBoardLed = OnBoardLed()
rtc: RealTimeClock = RealTimeClock()
event_queue: list = []

def callback(t):
    event_queue.append(
        Event.time_tick().set_timestamp(
            time()
        )
    )
    pass

# Anwendung bauen...
app: Pferdinand = Pferdinand(
    stdout=stdout
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

