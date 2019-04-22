
#import socket
def web_page():
  html ="""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>ESP Web Server</h1>
  <div><a href=\"?led=on\"><button>ON</button></a></div>
  <div><a href=\"?led=off\"><button>OFF</button></a></div>
  <b> Current Status : """
  html = html+  getPINStatusInWords()+ """</b></body></html>"""
  
  return html

def getPINStatus():
  return led.value()

def getPINStatusInWords():
  if getPINStatus() == 1:
    return "ON"
  else:
    return "OFF"

def setJSON():
  if result == 1:
    json_data = "[{status:ON}]"
  else:
    json_data = "[{status:OFF}]"
  return json_data
  
def isWebRequest():
  if request.find('mode=web') > -1 :
    return True
  elif request.find('mode=json') > -1:
    return False
  else:
    return True
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


def execute_request():
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  try:
    if led_on > -1 :
      print('LED ON')
      led.value(1)
      return 1
    if led_off > -1:
      print('LED OFF')
      led.value(0)
      return 0
  except:
    return -1
    
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr)) 
  request = conn.recv(1024)
  print( 'Content = %s' % str(request))
  request = str(request)
  if isWebRequest() == True:
    result = execute_request()
    response = web_page()
  else:
    result = execute_request()
    response = setJSON()
  
  if result == -1:
    response = "An error occured please try again"
  
  conn.send(response)
  conn.close()
