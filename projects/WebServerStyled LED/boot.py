


# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

#import webrepl

#webrepl.start()


try:
    import usocket as socket
except:
    import socket
import  network
from machine import Pin

#import esp
#esp.osdebug(None)

import gc
gc.collect()

ssid =""
password = ""

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,password)

while station.isconnected() == False:
  pass
print('Connection successful')
print(station.ifconfig())

led = Pin(5,Pin.OUT)


