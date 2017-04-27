#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time
import sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from struct import *
from libraryCH.device.lcd import ILI9341
from libraryCH.device.air import G3
debug=0

#LCD顯示設定
lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=90)
lcd.displayImg("rpiRF.jpg")
time.sleep(1)

#LCD設定
lcd_LineNow = 0
lcd_lineHeight = 30  #行的高度
lcd_totalLine = 8  # LCD的行數 (320/30=8)
screenSaverNow = False

pinRED = 4
pinYELLOW = 22
pinGREEN = 27

GPIO.setup(pinRED ,GPIO.OUT)
GPIO.setup(pinYELLOW ,GPIO.OUT)
GPIO.setup(pinGREEN ,GPIO.OUT)
GPIO.output(pinGREEN, GPIO.LOW)
GPIO.output(pinYELLOW, GPIO.LOW)
GPIO.output(pinRED, GPIO.LOW)

numKeep = 6
a_time = ["", "", "", "", "", ""]
a_pm1 = [0, 0, 0, 0, 0, 0]
a_pm25 = [0, 0, 0, 0, 0, 0]
a_pm10 = [0, 0, 0, 0, 0, 0]

def display_data(pm1, pm25, pm10):
    global a_time, a_pm1, a_pm25, a_pm10
    dt = list(time.localtime())

    lcd.displayClear()
    title = ("%15s %9s %9s %9s" % ("H:M:S", "pm01", "pm2.5", "pm10"))
    lcd.displayText("e1.ttf", fontSize=18, text=title, position=(lcd_Line2Pixel(1), 40), fontColor=(255,255,255) )

    for i in range(0,numKeep):
        if(i==(numKeep-1)):
            a_time[0] = str(dt[3]) + ":" + str(dt[4]) + ":" + str(dt[5])
            a_pm1[0] = pm1
            a_pm25[0] = pm25
            a_pm10[0] = pm10
 
        else:
            a_time[numKeep-1-i] = a_time[numKeep-2-i]
            a_pm1[numKeep-1-i] = a_pm1[numKeep-2-i]
            a_pm25[numKeep-1-i] = a_pm25[numKeep-2-i]
            a_pm10[numKeep-1-i] = a_pm10[numKeep-2-i]

        if(a_time[numKeep-1-i]>0 and a_pm1[numKeep-1-i]>0 and a_pm10[numKeep-1-i]>0):
            displayTXT = ("%13s %11d %11d %11d" % (a_time[numKeep-1-i],a_pm1[numKeep-1-i], a_pm25[numKeep-1-i], a_pm10[numKeep-1-i]))
            lcd.displayText("e1.ttf", fontSize=18, text=displayTXT, position=(lcd_Line2Pixel(numKeep-i+1), 60), fontColor=(253,244,6) )

#將行數轉為pixels
def lcd_Line2Pixel(lineNum):
    return lcd_lineHeight*lineNum


#air=G3()

while True:
    air=G3()
    pmdata = (air.read("/dev/ttyS0"))
    print (pmdata[3], pmdata[4], pmdata[5])
    display_data(pmdata[3], pmdata[4], pmdata[5])

    if(pmdata[4]<20):
        GPIO.output(pinGREEN, GPIO.HIGH)
        GPIO.output(pinRED, GPIO.LOW)
        GPIO.output(pinYELLOW, GPIO.LOW)
    elif (pmdata[4]<50 and pmdata[4]>19):
        GPIO.output(pinGREEN, GPIO.LOW)
        GPIO.output(pinRED, GPIO.LOW)
        GPIO.output(pinYELLOW, GPIO.HIGH)
    elif (pmdata[4]>49):
        GPIO.output(pinGREEN, GPIO.LOW)
        GPIO.output(pinRED, GPIO.HIGH)
        GPIO.output(pinYELLOW, GPIO.LOW)

    pmdata = None
    air = None
    time.sleep(6)
    
