

try:
    import usocket as socket
except:
    import socket
import  network
from machine import Pin, RTC, I2C
import ssd1306 
import ntptime
import machine
import sys
import time
import esp
esp.osdebug(None)
import main
import gc
gc.collect()


rtc = RTC()


def wifi_connect(timeout=20):
  print(rtc.memory() )
  if rtc.memory() == b'':
    
    ssid ="Stargate"
    password = "T9NKET77ASDFG"

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid,password)

    while station.isconnected() == False:
      pass
    print('Connection successful')
    print(station.ifconfig())
    station = network.WLAN(network.STA_IF)
    stData = station.ifconfig()
    rtc.memory(b'read')
    
    
  #settime using NTP server
    ntptime.settime()
    
  else:
    print("Woke up ------------------------------------------")
    
  
  
wifi_connect(30)
main.show_clock(rtc)



