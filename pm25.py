#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time
import sys
from struct import *
from libraryCH.device.lcd import ILI9341
debug=0

#LCD顯示設定
lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=90)
lcd.displayImg("green.png")
#LCD設定
lcd_LineNow = 0
lcd_lineHeight = 30  #行的高度
lcd_totalLine = 8  # LCD的行數 (320/30=8)
screenSaverNow = False

numKeep = 6
a_time = ["", "", "", "", "", ""]
a_pm1 = [0, 0, 0, 0, 0, 0]
a_pm25 = [0, 0, 0, 0, 0, 0]
a_pm10 = [0, 0, 0, 0, 0, 0]

def display_data(pm1, pm25, pm10):
    global a_time, a_pm1, a_pm25, a_pm10

    dt = list(time.localtime())
    nowMinute = dt[4]
    nowSeconds = dt[5]

    lcd.displayText("e1.ttf", fontSize=12, text="TIME    [PM]1  [PM]2.5  [pm]10", position=(lcd_Line2Pixel(1), 180), fontColor=(253,244,6) )
    for i in range(0,numKeep):
        if(i==(numKeep-1)):
            a_time[0] = str(nowMinute) + ":" + str(nowSeconds)
            a_pm1[0] = pm1
            a_pm25[0] = pm25
            a_pm10[0] = pm10
 
        else:
            a_time[numKeep-1-i] = a_time[numKeep-2-i]
            a_pm1[numKeep-1-i] = a_pm1[numKeep-2-i]
            a_pm25[numKeep-1-i] = a_pm25[numKeep-2-i]
            a_pm10[numKeep-1-i] = a_pm10[numKeep-2-i]

        displayTXT = a_time[numKeep-1-i] + "  " + str(a_pm1[numKeep-1-i]) + "  " + str(a_pm25[numKeep-1-i]) + "  " + str(a_pm10[numKeep-1-i])
        lcd.displayText("e1.ttf", fontSize=12, text=displayTXT, position=(lcd_Line2Pixel(numKeep-i+1), 180), fontColor=(253,244,6) )

#將行數轉為pixels
def lcd_Line2Pixel(lineNum):
    return lcd_lineHeight*lineNum


class g3sensor():
    def __init__(self):
        if debug: print "init"
	self.endian = sys.byteorder
    
    def conn_serial_port(self, device):
        if debug: print device
        self.serial = serial.Serial(device, baudrate=9600)
        if debug: print "conn ok"

    def check_keyword(self):
        if debug: print "check_keyword"
        while True:
            token = self.serial.read()
    	    token_hex=token.encode('hex')
    	    if debug: print token_hex
    	    if token_hex == '42':
    	        if debug: print "get 42"
    	        token2 = self.serial.read()
    	        token2_hex=token2.encode('hex')
    	        if debug: print token2_hex
    	        if token2_hex == '4d':
    	            if debug: print "get 4d"
                    return True
		elif token2_hex == '00': # fixme
		    if debug: print "get 00"
		    token3 = self.serial.read()
		    token3_hex=token3.encode('hex')
		    if token3_hex == '4d':
			if debug: print "get 4d"
			return True
		    
    def vertify_data(self, data):
	if debug: print data
        n = 2
	sum = int('42',16)+int('4d',16)
        for i in range(0, len(data)-4, n):
            #print data[i:i+n]
	    sum=sum+int(data[i:i+n],16)
	versum = int(data[40]+data[41]+data[42]+data[43],16)
	if debug: print sum
        if debug: print versum
	if sum == versum:
	    print "data correct"
	
    def read_data(self):
        data = self.serial.read(22)
        data_hex=data.encode('hex')
        if debug: self.vertify_data(data_hex)
        pm1_cf=int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16)
        pm25_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
        pm10_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
        pm1=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
        pm25=int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16)
        pm10=int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16)
        if debug: print "pm1_cf: "+str(pm1_cf)
        if debug: print "pm25_cf: "+str(pm25_cf)
        if debug: print "pm10_cf: "+str(pm10_cf)
        if debug: print "pm1: "+str(pm1)
        if debug: print "pm25: "+str(pm25)
        if debug: print "pm10: "+str(pm10)
        data = [pm1_cf, pm10_cf, pm25_cf, pm1, pm10, pm25]
    	self.serial.close()
        return data

    def read(self, argv):
        tty=argv[0:]
        self.conn_serial_port(tty)
        if self.check_keyword() == True:
            self.data = self.read_data()
            if debug: print self.data
            return self.data

air=g3sensor()

while True:
    pmdata = (air.read("/dev/ttyS0"))
    print (pmdata[3], pmdata[4], pmdata[5])
    display_data(pmdata[3], pmdata[4], [5])
    time.sleep(30)


#if __name__ == '__main__': 
#    air=g3sensor()
#    while True:
#        pmdata=0
#        try:
#            pmdata=air.read("/dev/ttyAMA0")
#        except: 
#            next
#        if pmdata != 0:
#            print pmdata
#            break

