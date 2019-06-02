try:
  import usocket as socket
except:
  import socket
  
import ujson
import machine
import sys
import time
from machine import Pin, RTC, I2C
import ssd1306 
import ntptime
import alarmcontrol
import  network
import ntptolocal
import alarmcontrol


settings ={}
global rtc_wake
rtc_wake = False
switch = Pin(23,Pin.IN)

switch_active = False

def handle_interrupt(v):
  global switch_active
  
  rtc = RTC()
  print('Switch Interrupt')
  
  if switch_active == False:
    switch_active = True
    rtc.memory(b'3')
    start_webserver()
    
  if switch_active == True:
    switch_active = False
    print('Switch Toggle Off')
  



switch.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)


  
  
  
def readSettings():
  global settings
  f = open("settings.py", "r")
  settings = ujson.loads(f.read().rstrip("\n"))
  #for key, value in settings.items():
    #print (key ,'corresponds to', settings[key])
    #print(type(settings))
  f.close()

def saveSettings(key,newValue):
    settings[key] = newValue;
    print(str(settings)) 
    f = open("settings.py", "w")
    data = ujson.dumps(settings)
    print(data)
    f.write(data)
    f.close()
    
def setBoardTime():
  rtc.datetime((2019, 4, 27, 1, 12, 16, 0, 0)) # set a specific date and time
  
def getBoardTime():
  currTime = rtc.datetime() # get date and time
  print(currTime)
  return currTime
  
#USE BOOTCOUNTER LOGIC
def display_oled(data):
  print("21 ->SDA 22->SCL")
  global display
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
  #stData = station.ifconfig()
  #display.text(str(stData[0]),1,54)
  display.poweron()
  display.show()
  
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
  timdata = ("%02d:%02d:%02d "+ampm) % (hour, datetime[5], datetime[6])+"-"+"%d/%d/%d" % (datetime[1], datetime[2], datetime[0])
  display_oled(timdata)  

def hide_clock():
  display.poweroff()

def start_webserver():
  ssid =settings["SSID"]
  password = settings["WIFIPWD"]

  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid,password)
  switch = Pin(23,Pin.IN)
  switch.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())
  station = network.WLAN(network.STA_IF)
  
  print('Start webserver')
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(( '' , 80))
  s.listen(5)
  
  while True:
    
    
    if switch_active == False:
      rtc.memory(b'1')
      machine.deepsleep(1000)
  
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr)) 
    #s.on("/submit", handleSubmit);
    request = conn.recv(1024)
    print( 'Content = %s' % str(request))
   
    request = str(request)
    #time.sleep(0.25) 
    response = web_page()
    conn.send(response)
    conn.close()
    
    
def handleSubmit():
  print('Submit')
  
def web_page(): 
  html ="""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>Garden Keeper</h1>
  <div> <form method="get" action="/submit"  >"""
  
  html = html+ """<div><b>Start time 1 : <input type=time value ="""+settings["STARTTIME1"]+""" name="start1" ></b></div>"""
  html = html+ """<div><b>End time 1 : <input type=time value ="""+settings["ENDTIME1"]+""" name="end1" ></b></div>"""
  html = html+ """<div><b>Start time 2 : <input type=time value ="""+settings["STARTTIME2"]+""" name="start2" ></b></div>"""
  html = html+ """<div><b>End time 2 : <input type=time value ="""+settings["ENDTIME2"]+""" name="end2" ></b></div>"""
  html = html+ """<div><input type="submit" value="Save"></div></form>"""
  html = html+ """</body></html>"""
  #saveSettings("STARTTIME1","22:35:00")
  #currDtTime = "UTC: " + stryyyy + "-Time: " + strhhmm
  #print('Page genrated')
  return html
#(year, month, day, weekday, hours, minutes, seconds, subseconds)
def convertTupleDate(tup): 
    year =  str(tup[0])
    mth = str(tup[1])
    dy = str(tup[2])
    strDate = year + '/'+mth+ '/' + dy
    return strDate

def wifi_connect(rtc,timeout=20):
  print(rtc.memory() )
  #led.value(0)
  if rtc.memory() == b'':
    
    ssid =settings["SSID"]
    password = settings["WIFIPWD"]

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
    UTC_OFFSET = int(settings["TIMEOFFSET"])
    ntptolocal.settime(UTC_OFFSET)
    
  else:
    alarmpolling(rtc,rtc_wake)
    print("Woke up ------------------------------------------")
    

def main():
  #setBoardTime()
  readSettings()
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)
    
  while True:
    #Show clock
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
    
    
    #render web page
    conn, addr = s.accept()
    request = conn.recv(1024)
    response = web_page()
    conn.send(response)
    conn.close()
    
def alarmpolling(rtc,rtc_wake):
  print('Alarm polling')
  
  if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    if switch.value() == 1:
      print('Switch ON')
    else:
      print('Switch OFF')
      
    readSettings()
    #print('woke from a deep sleep')
    show_clock(rtc)
    
    check_alarm_values(rtc)
    
    time.sleep(5) 
    hide_clock()
  else:
    print('power on or hard reset')

  if rtc.memory() == b'1':
    machine.deepsleep(5000)
  if rtc.memory() == b'2':
    wake_while_active(rtc)
  
  

def check_alarm_values(rtc):
  for key, value in settings.items():
    
    if key.find('START') > -1 :
      #print (key ,'corresponds to', settings[key])
      alarmcontrol.check_alarm_time(settings[key],rtc,True)
    if key.find('END') > -1:
      #print (key ,'corresponds to', settings[key])
      alarmcontrol.check_alarm_time(settings[key],rtc,False)

def wake_while_active(rtc):
  while True:
    readSettings()
    print('wake while active')
    show_clock(rtc)
    
    check_alarm_values(rtc)
    
    time.sleep(5) 
    hide_clock()


