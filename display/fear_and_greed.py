#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5bc
from PIL import Image, ImageEnhance

import http.client
import json
from urllib.request import urlopen

conn = http.client.HTTPSConnection("api.alternative.me")
conn.request("GET", "/fng/")

res = conn.getresponse()
data = res.read()
json_string = data.decode("utf-8")

# print(json_string)

index_value = int(json.loads(json_string)['data'][0]['value'])

logging.basicConfig(level=logging.DEBUG)

# exit()

url = "https://alternative.me/crypto/fear-and-greed-index.png"

try:
    logging.info("Crypto Fear & Greed Index")

    epd = epd7in5bc.EPD()

    logging.info("Init and Clear")
    epd.init()
    epd.Clear()

    newimage = Image.open(urlopen(url)).convert("L")

    enhancer = ImageEnhance.Contrast(newimage)
    newimage = enhancer.enhance(2)

    blackimage1 = Image.new('L', (epd.width, epd.height), 255)
    redimage1 = Image.new('L', (epd.width, epd.height), 255)

    if(index_value >= 50):
      blackimage1.paste(newimage.resize((428, 384)), (128, 0))
    else:
      redimage1.paste(newimage.resize((428, 384)), (128, 0))

    epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5bc.epdconfig.module_exit()
    exit()
