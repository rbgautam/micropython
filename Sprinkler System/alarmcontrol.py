import machine
from machine import RTC
from machine import Timer
import main
import urtc
from time import time,sleep
from machine import Pin
my_time = machine.RTC().datetime()

def initalarm(rtc,rtc_wake):
  tim = machine.Timer(1)   # init with default time and date
  # create a RTC alarm that expires after 10 seconds
  #rtc.alarm(time=10000, repeat=True)
  #rtc_i = rtc.irq(trigger=RTC.ALARM0, handler=alarm_handler, wake=machine.SLEEP | machine.IDLE)
  tim.init(mode=tim.PERIODIC, period=2000,callback=alarm_handler(rtc,rtc_wake))

def alarm_handler (rtc,rtc_wake):
  
  rtc_wake = True
  main.alarmpolling(rtc,rtc_wake)
  print(rtc_wake)


def check_alarm_time(alarm_time,rtc,isStart):
  print('check alarm time')
  #def datetime_tuple(year=None, month=None, day=None, weekday=None, hour=None, minute=None, second=None, millisecond=None)
  currtime =  rtc.datetime()
  #(year, month, day, weekday, hours, minutes, seconds, subseconds)
  timarray = alarm_time.split(":")
  my_time= urtc.datetime_tuple(int(currtime[0]),int(currtime[1]),int(currtime[2]),int(currtime[3]),int(timarray[0]),int(timarray[1]),int(timarray[2]),0)
  alarm_end_time = urtc.datetime_tuple(int(currtime[0]),int(currtime[1]),int(currtime[2]),int(currtime[3]),int(timarray[0]),int(timarray[1]),int(timarray[2])+30,0)
  hour = my_time[4]
  ampm = "AM"
  if (hour > 12):
    hour = hour - 12
    if (hour == 0):
        hour = 12
    ampm = "PM"
  timdata = ("%d:%02d:%02d "+ampm) % (hour, my_time[5], my_time[6])+"-"+"%d/%d/%d" % (my_time[1], my_time[2], my_time[0])
  #print(my_time)
  if currtime > my_time and currtime <alarm_end_time:
    print('before execute alrm')
    excecute_alarm(isStart)
    #time.sleep(10)
    
def create_alarmtime(alarm_time,currtime):
  timarray = alarm_time.split(":")
  my_time= urtc.datetime_tuple(int(currtime[0]),int(currtime[1]),int(currtime[2]),int(currtime[3]),int(timarray[0]),int(timarray[1]),int(timarray[2]),0)
  
def excecute_alarm(isStart):
  print('inside execute alarm')
  led = Pin(15,Pin.OUT)
  rtc = machine.RTC()
  if isStart == True and led.value() == 0:
    led.value(1)
    rtc.memory(b'2')
  if isStart == False and led.value() == 1:
    led.value(0)
    rtc.memory(b'1')
    
