

try:
    import usocket as socket
except:
    import socket
import  network
from machine import Pin, RTC, I2C
import ssd1306 
import ntptime
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

#sensor = dht.DHT22(Pin(14))
rtc = RTC()

#settime using NTP server
ntptime.settime()
