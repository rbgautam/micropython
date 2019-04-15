from time import time,sleep
from machine import Pin
last_time = time()
led = Pin(5,Pin.OUT)
while True:
    current_time = time()
    if current_time - last_time > 2:
        print(current_time)
        led.value(not led.value())    
        sleep(1)
        last_time = current_time()
