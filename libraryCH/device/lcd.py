#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0


class ILI9341:
    def __init__(self, LCD_size_w=240, LCD_size_h=320, LCD_Rotate=180):
        DC = 18
        RST = 23
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.LCD_size_w = LCD_size_w
        self.LCD_size_h = LCD_size_h
        self.LCD_Rotate = LCD_Rotate
        disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
        self.disp = disp

        disp.begin()  # Initialize display.

    def displayImg(self, imagePath):
        image = Image.open(imagePath)
        image = image.rotate(self.LCD_Rotate).resize((self.LCD_size_w, self.LCD_size_h))
        self.disp.display(image)

    def displayClear(self):
        self.disp.clear((0, 0, 0))

    def displayText(self, fontPath, fontSize=18, text="Hello world.", position=(10, 10), fontColor=(255, 255, 255), imagePath=""):
        # Get rendered font width and height.
        if(imagePath!=""):
            image = Image.open(imagePath)
            image = image.rotate(self.LCD_Rotate).resize((self.LCD_size_w, self.LCD_size_h))
            #self.disp.display(image)
        else:
            image = self.disp.buffer

        font = ImageFont.truetype(fontPath, fontSize)
        draw = ImageDraw.Draw(image)
        width, height = draw.textsize(text, font=font)
        # Create a new image with transparent background to store the text.
        textimage = Image.new('RGBA', (width, height), (0,0,0,0))
        # Render the text.
        textdraw = ImageDraw.Draw(textimage)
        textdraw.text((0,0), text, font=font, fill=fontColor)
        # Rotate the text image.
        rotated = textimage.rotate(self.LCD_Rotate, expand=1)
        # Paste the text into the image, using it as a mask for transparency.
        image.paste(rotated, position, rotated)
        self.disp.display()
        #del font, image, textimage, textdraw, rotated
        font = None
        image = None
        textimage = None
        textdraw = None
        rotated = None
