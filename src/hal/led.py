# Bibliotheken laden
from machine import Pin

class OnBoardLed:
    
    def __init__(self):
        self.__led: Pin = Pin("LED", Pin.OUT)
        pass
    
    def on(self) -> 'Self':
        self.__led.on()
        return self
    
    def off(self) -> 'Self':
        self.__led.off()
        return self
    
    pass