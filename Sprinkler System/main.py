
import ujson
import machine
import sys
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
  display.show()
  #scrioll text
  #display.scroll(0,40)

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
  display_oled(currDtTime)
  return html
#(year, month, day, weekday, hours, minutes, seconds, subseconds)
def convertTupleDate(tup): 
    year =  str(tup[0])
    mth = str(tup[1])
    dy = str(tup[2])
    strDate = year + '/'+mth+ '/' + dy
    return strDate

def convertTupleTime(tup):
  hour =  str(tup[4])
  min = str(tup[5])
  sec = str(tup[6])
  strTime = hour + ':'+min+ ':'+ sec
  return strTime
  
def getTimeSinceMidnight():
  currBoardTime = rtc.datetime();
  currTimeInSeconds = (currBoardTime[4]*60)+(currBoardTime[5]*60)+(currBoardTime[6])
  currTimeInSeconds = currTimeInSeconds - getTimeOffset()
  return currTimeInSeconds
  
def getTimeOffset():
  return 6*60*60
  
def getCSTTime():
  currTime = rtc.datetime() 
  secsfrom12 = getTimeSinceMidnight()
  hrsFromSecs = int(secsfrom12/3600)
  minsfromSecs = int((secsfrom12 - (hrsFromSecs*3600))/60)
  secsFromMins = int(secsfrom12 - ((hrsFromSecs*3600)+(minsfromSecs*60)))
  rtc.datetime((currTime[0],currTime[1],currTime[2],currTime[3],hrsFromSecs,minsfromSecs,secsFromMins,currTime[7]))
  return rtc.datetime()

def main():
  #setBoardTime()
  readSettings()
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)
    
  while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    response = web_page()
    conn.send(response)
    conn.close()

main()

