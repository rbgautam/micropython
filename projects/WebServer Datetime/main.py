

def setBoardTime():
  rtc.datetime((2019, 4, 27, 1, 12, 16, 0, 0)) # set a specific date and time
  
def getBoardTime():
  currTime = rtc.datetime() # get date and time
  print(currTime)
  return currTime
  


def web_page():
  html ="""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>NTP Web Server Time</h1>
  <div>
  <b> Current Time : """
  dtTup = getBoardTime()
  stryyyy = convertTupleDate(dtTup)
  strhhmm = convertTupleTime(dtTup)
  html = html+  stryyyy + """</b><div>"""
  html = html+ """<div><b>"""+strhhmm+"""</b></div></body></html>"""
  
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
