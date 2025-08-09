from machine import Pin  # type: ignore

import time

led = Pin(25, Pin.OUT)  # LED integrado

while True:
    led.toggle()
    time.sleep(0.5)
