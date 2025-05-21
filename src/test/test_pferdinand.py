# ---------------------------------------------------------------------------------------------------------------------
from pferdinand.pferdinand import Pferdinand, Event
from unittest import TestCase
from test.printout import PrintOut
from time import time, mktime, localtime, sleep
from hal.interfaces.types import Timestamp
# ---------------------------------------------------------------------------------------------------------------------

class TestInitial(TestCase):

    def runTest(self):
        """Prueft den Initialen Zustand ab."""
        p: Pferdinand = Pferdinand(
            PrintOut()
        )
        self.assertEqual(
            Pferdinand.WAITING,
            p.state()
        )
        pass
# ---------------------------------------------------------------------------------------------------------------------

class TestState(TestCase):

    def runTest(self):
        """Erstellt eine Instanz der Anwendung und prueft, ob die Anwendung ausloest sobald die eingestellte Zeit anschlaegt."""
        p: Pferdinand = Pferdinand(
            PrintOut()
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
            p.dispatch_event(
                Event.time_tick().set_timestamp(time())
            )
            # Pruefe, ob der aktive Zustand eingehalten wird.
            self.assertEqual(
                Pferdinand.ACTIVE if (t + i) >= t_a and (t + i) < (t_a + 3) else Pferdinand.WAITING,
                p.state()
            )
            sleep(1)
        self.assertEqual(
            Pferdinand.WAITING,
            p.state()
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
