

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

import gc
gc.collect()

bootcount = 0
rtc = RTC()

#USE BOOTCOUNTER LOGIC
def display_oled(data):
  print("21 ->SDA 22->SCL")
  i2c = I2C(-1, Pin(22), Pin(21)) #21 ->SDA #22->SCL

  display = ssd1306.SSD1306_I2C(128, 64, i2c)
  display.fill(0)
  display.text("Garden Keeper", 5, 0)
  datasplit = data.split('-')
  display.text(datasplit[0],1,17)
  display.text(datasplit[1],1,25)
  display.invert(1)
  display.text('CPU: ' + str(machine.freq()/1000000) + 'MHz', 1, 35)
  display.text(sys.platform + " " + sys.version, 1, 45)
  
  display.text(str(stData[0]),1,54)
  display.show()
  machine.deepsleep(5000)
  #scrioll text
  #display.scroll(0,40)
  
def show_clock(rtc):
  datetime = rtc.datetime()
  hour = datetime[4]
  ampm = "AM"
  if (hour > 12):
    hour = hour - 12
    if (hour == 0):
        hour = 12
    ampm = "PM"
  timdata = ("%d:%02d:%02d "+ampm) % (hour, datetime[5], datetime[6])+"-"+"%d/%d/%d" % (datetime[1], datetime[2], datetime[0])
  display_oled(timdata)  

def wifi_connect(bootcount,timeout=20):
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
    
  bootcount = bootcount +1
  
wifi_connect(bootcount,30)
show_clock(rtc)



