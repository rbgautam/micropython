
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

ssid ="Stargate"
password = "T9NKET77ASDFG"

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,password)

while station.isconnected() == False:
  pass
print('Connection successful')
print(station.ifconfig())

led = Pin(5,Pin.OUT)

