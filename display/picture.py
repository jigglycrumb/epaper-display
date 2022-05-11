#!/usr/bin/python
# -*- coding:utf-8 -*-

# This script shows pictures from the pictures folder

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pictures')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5bc
import time
from PIL import Image
import traceback

logging.basicConfig(level=logging.DEBUG)

imgs = []
valid_images = [".jpg",".jpeg",".bmp",".png"]
for f in os.listdir(picdir):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs.append(f)

try:
    fp_current_image = open("./.current_display_image", "r")
except FileNotFoundError:
    fp_current_image = open(imgs[0], "r")

current_image = fp_current_image.read().replace('\n', '')
fp_current_image.close()

image_index = imgs.index(current_image)
image_index+=1
if(image_index >= len(imgs)):
    image_index = 0
next_image = imgs[image_index]

fp_current_image = open("./.current_display_image", "w")
fp_current_image.write(next_image)
fp_current_image.close()

try:
    logging.info("Picture frame")

    epd = epd7in5bc.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    blackimage1 = Image.new('L', (epd.width, epd.height), 255)
    redimage1 = Image.new('L', (epd.width, epd.height), 255)
    newimage = Image.open(os.path.join(picdir, current_image))
    blackimage1.paste(newimage.resize((640,384)), (0,0))
    epd.display(epd.getbuffer(blackimage1),epd.getbuffer(redimage1))

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5bc.epdconfig.module_exit()
    exit()
