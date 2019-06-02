

from machine import Pin, RTC, I2C
import ssd1306 
import machine
import sys
import time
import esp
esp.osdebug(None)
import main

import gc
global rtc_wake
rtc_wake = False
gc.collect()
led = Pin(5,Pin.OUT)
led.value(0)

rtc = RTC()

main.readSettings()  
main.wifi_connect(rtc,30)
main.alarmpolling(rtc,rtc_wake)
#alarmcontrol.initalarm(rtc,rtc_wake)








