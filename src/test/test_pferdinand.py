# ---------------------------------------------------------------------------------------------------------------------
from pferdinand.pferdinand import Pferdinand, Event
from unittest import TestCase
from test.printout import PrintOut
from test.digital_output_mock import DigitalOutputMock
from time import time, mktime, localtime, sleep
from hal.interfaces.types import Timestamp
from test.rtc_mock import Rtc
# ---------------------------------------------------------------------------------------------------------------------

class TestInitial(TestCase):

    def runTest(self):
        """Prueft den Initialen Zustand ab."""
        event_input_queue: list = []
        event_output_queue: list = []
        p: Pferdinand = Pferdinand(
            event_input_queue,
            event_output_queue,
            Rtc(),
            PrintOut(),
        )
        self.assertEqual(
            Pferdinand.WAITING,
            p.state()
        )
        self.assertEqual(
            0,
            len(event_output_queue)
        )
        pass
# ---------------------------------------------------------------------------------------------------------------------

class TestState(TestCase):

    def runTest(self):
        """Erstellt eine Instanz der Anwendung und prueft, ob die Anwendung ausloest sobald die eingestellte Zeit anschlaegt."""
        event_input_queue: list = []
        event_output_queue: list = []
        p: Pferdinand = Pferdinand(
            event_input_queue,
            event_output_queue,
            Rtc(),
            PrintOut(),
        )
        p.set_active_time(
            3000
        )
        t: float = time()
        t_a: float = t + 2
        p.set_active_at(
            Timestamp().from_tuple(
                localtime(t_a)
            )
        )
        for i in range(0, 10):
            event_input_queue.append(
                Event.time_tick().set_timestamp(
                    Timestamp().from_tuple(localtime(time()))
                )
            )
            p.dispatch_event()
            # Pruefe, ob der aktive Zustand eingehalten wird.
            if len(event_output_queue) > 0:
                event: Event = event_output_queue.pop()
                print(event)
                ts = Timestamp().from_tuple(
                    localtime(t_a)
                )
                ts_end = Timestamp().from_tuple(
                    localtime(t_a+3)
                )
                if event.timestamp().hours() >= ts.hours() and event.timestamp().minutes() >= ts.minutes() and event.timestamp().seconds() >= ts.seconds() and event.timestamp().hours() <= ts_end.hours() and event.timestamp().minutes() <= ts_end.minutes() and event.timestamp().seconds() <= ts_end.seconds():
                    self.assertEqual(
                        Pferdinand.ACTIVE,
                        p.state(),
                        f'{localtime(t_a)} <= {event.timestamp().to_tuple()} <= {localtime(t_a + 3)}',
                    )
                    self.assertEqual(
                        Event.MOTOR_UP_COMMAND,
                        event.event_id(),
                        f'{localtime(t_a)} <= {event.timestamp().to_tuple()} <= {localtime(t_a + 3)}',
                    )
                else:
                    self.assertEqual(
                        Pferdinand.WAITING,
                        p.state(),
                        f'{localtime(t_a)} <= {event.timestamp().to_tuple()} <= {localtime(t_a + 3)}',
                    )
                    self.assertEqual(
                        Event.MOTOR_STOP_COMMAND,
                        event.event_id()
                    )
            sleep(1)
        self.assertEqual(
            Pferdinand.WAITING,
            p.state()
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
