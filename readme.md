# Pferdinand

## Hardware 
Diese Anwendung ist fuer einen Raspberry Pi Pico gebaut.

## src/
Hier liegt der Source Code der auf der Zielhardware ausgefuehrt werden kann.
Die Anwendung ist mit Thonny fuer MicroPython entwickelt.
MicroPython ist ein Subset von Python, der hier abliegende Code muss jederzeit
konform zu der MicroPython Spezifikation sein.

MicroPython: https://docs.micropython.org/en/latest/library/
Thonny: https://thonny.org 

## Umgang
Das System besteht aus einer Hauptplatine mit Raspberry Pi Pico der 2 Relais schaltet. Und einer Nebenplatine die eine Beschaltung zum Anschliessen 
von 2 Schaltern (UP und DOWN) bereit stellt.
Auf der Hauptplatine befindet sich eine Batteriegepufferte Real Time Clock (RTC) aus der die Uhrzeit ausgelesen wird.
Je ein Schalter schaltet einen Ausgang, UP schaltet den UP Ausgang / DOWN schaltet den DOWN Ausgang.
Die Software verschraenkt die beiden Schalter gegeneinander, so dass nicht beide Ausgaenge gleichzeitig geschaltet werden koennen.
Wird eine voreingestellte Uhrzeit erreich schaltet die Software den UP Ausgang fuer eine voreingestellte Dauer.

Die Urhzeit wird durch das Ausfuehren eines seperaten Skripts eingestellt.
Das Skript muss so angepasst werden, dass eine spezifische Uhrzeit per I2C uebertragen wird. Das Skript muss auf dem Raspberry Pi ausgefuehrt werden.

## Hauptskripte
### set_time.py
Das Skript "set_time.py" setzt eine Uhrzeit auf der externen RTC.

## main.py
Das Skript "main.py" fuehrt die Std-Anwendung aus.
Die Std-Anwendung schaltet einen Ausgang zu einem vordefinierten Zeitpunkt (Stunde, Minute, Sekunde, -ohne Datum-).
Zusaetzlich koennen zwei Ausgaenge ueber einen Schalter gesetzt werden. Die Ausgaenge sind gegeneinander verschraenkt und koennen nicht gleichzeitig aktiviert werden.
Die Anwendung logged ueber einen UART.

## test/
Tests fuer den Source Code.
Die Tests koennen auf jedem beliebigen Rechner ausgefuert werden.

### Testumgebung aufsetzen

    python -m venv .venv && source .venv/bin/activate

### Ausfuehren
Testdiscovery und Ausfuehrung.

    python -m unittest

Siehe auch https://docs.python.org/3/library/unittest.html

## doc/
Hier liegt die Dokumentation ab.
