try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

import  network
from machine import Pin, RTC, I2C
import machine
import esp
esp.osdebug(None)
import gc
gc.collect()




def wifi_connect(timeout=20):
  ssid =""
  password = ""

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
  settime()
  

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600
CST_OFFSET = 5*60*60
host = "pool.ntp.org"

def time():
  NTP_QUERY = bytearray(48)
  NTP_QUERY[0] = 0x1b
  addr = socket.getaddrinfo(host, 123)[0][-1]
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.settimeout(1)
  res = s.sendto(NTP_QUERY, addr)
  msg = s.recv(48)
  s.close()
  val = struct.unpack("!I", msg[40:44])[0]
  return val - (NTP_DELTA+CST_OFFSET)

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
def settime():
    t = time()
    import machine
    import utime
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    
def displaytime():
  datetime = machine.RTC().datetime()
  hour = datetime[4]
  ampm = "AM"
  if (hour > 12):
    hour = hour - 12
    if (hour == 0):
        hour = 12
    ampm = "PM"
  timdata = ("%d:%02d:%02d "+ampm) % (hour, datetime[5], datetime[6])+"-"+"%d/%d/%d" % (datetime[1], datetime[2], datetime[0])
  print(timdata)
  
wifi_connect(30)
displaytime()