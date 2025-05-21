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

## test/
Tests fuer den Source Code.
Die Tests koennen auf jedem beliebigen Rechner ausgefuert werden.

### Testumgebung aufsetzen

    python -m venv .venv && source .venv/bin/activate

### Ausfuehren
Testdiscovery und Ausfuehrung.

    python -m unittest

Siehe auch https://docs.python.org/3/library/unittest.html
