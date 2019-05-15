
import ujson
import machine
import sys
import time
from machine import Pin, RTC, I2C
import ssd1306 
import ntptime
import alarmcontrol

settings ={}
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
  
  
def web_page():
  html ="""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>NTP Web Server Time</h1>
  <div>
  <b> Current Time : """
  dtTup = getBoardTime()
  stryyyy = convertTupleDate(dtTup)
  strhhmm = convertTupleTime(dtTup)
  html = html+  stryyyy + """</b><div>"""
  html = html+ """<div><b>"""+strhhmm+"""</b></div>"""
  html = html+ """<div><b>Start time 1 : """+settings["STARTTIME1"]+"""</b></div>"""
  html = html+ """</body></html>"""
  saveSettings("STARTTIME1","22:35:00")
  currDtTime = "UTC: " + stryyyy + "-Time: " + strhhmm
 
  return html
#(year, month, day, weekday, hours, minutes, seconds, subseconds)
def convertTupleDate(tup): 
    year =  str(tup[0])
    mth = str(tup[1])
    dy = str(tup[2])
    strDate = year + '/'+mth+ '/' + dy
    return strDate



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
