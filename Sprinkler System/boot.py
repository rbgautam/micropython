try:
    import usocket as socket
except:
    import socket
import  network
from machine import Pin, RTC, I2C
import ssd1306 
import machine
import sys
import time
import esp
esp.osdebug(None)
import main

import gc
import ntptolocal
import alarmcontrol
gc.collect()


rtc = RTC()
global rtc_wake
rtc_wake = False
led = Pin(15,Pin.OUT)

def wifi_connect(timeout=20):
  print(rtc.memory() )
  led.value(0)
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
    rtc.memory(b'1')
    
    
  #settime using NTP server
    ntptolocal.settime()
    
  else:
    main.alarmpolling(rtc,rtc_wake)
    print("Woke up ------------------------------------------")
    
  
  
wifi_connect(30)
main.alarmpolling(rtc,rtc_wake)
#alarmcontrol.initalarm(rtc,rtc_wake)






