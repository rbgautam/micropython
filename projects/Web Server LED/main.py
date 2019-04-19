
#import socket
def web_page():
  html ="""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>ESP Web Server</h1><a href=\"?led=on\"><button>ON</button></a>&nbsp;
  <a href=\"?led=off\"><button>OFF</button></a></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr)) 
  request = conn.recv(1024)
  print( 'Content = %s' % str(request))
  request = str(request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  if led_on == 6:
    print('LED ON')
    led.value(1)
  if led_off == 6:
    print('LED OFF')
    led.value(0)
  response = web_page()
  conn.send(response)
  conn.close()
