from machine import Pin
from time import sleep
led = Pin(5, Pin.OUT)
while True:
    led.value(not led.value())
    print(led.value())
    sleep(0.5)
