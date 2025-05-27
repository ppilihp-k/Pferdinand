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

## Hauptskripte
### set_time.py
Das Skript "set_time.py" setzt eine Uhrzeit auf der externen RTC.

## run_app.py
Das Skript "run_app.py" fuehrt die Std-Anwendung aus.
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
