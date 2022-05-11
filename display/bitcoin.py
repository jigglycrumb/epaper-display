#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5bc
import time
from PIL import Image,ImageDraw,ImageFont, ImageOps, ImageEnhance
import traceback

import requests # request img from web

logging.basicConfig(level=logging.DEBUG)

price_url = "https://api.blockchain.com/v3/exchange/tickers/BTC-USD"
r = requests.get(price_url)
rs = r.json()

price_positive = False
if(rs['last_trade_price'] >= rs['price_24h'] ):
  price_positive = True


price_url = "https://blockchain.info/ticker"

r = requests.get(price_url)
rs = r.json()

btc_price_eur = round(rs['EUR']['last'], 2)
btc_price_usd = rs['USD']['last']
moscow_time = round((1 / btc_price_usd) * 100 * 1000000)


# fetch fear & greed data
fear_and_greed_url = "https://api.alternative.me/fng/"
r = requests.get(fear_and_greed_url)
rs = r.json()

fear_and_greed_value = int(rs['data'][0]['value'])
fear_and_greed_label = rs['data'][0]['value_classification']

# fetch block time
block_time_url = "https://mempool.space/api/blocks/tip/height"
r = requests.get(block_time_url)
block_time = r.json()
# print("block time ", rs)

# fetch fees
fees_url = "https://mempool.space/api/v1/fees/recommended"
r = requests.get(fees_url)
fees = r.json()
# print("fees ", rs)

# exit()

# import shutil # save img locally
from cairosvg import svg2png

# import cairosvg
from urllib.request import urlopen


days = 7 # possible values: 1, 7, 30

url = f'https://s3.coinmarketcap.com/generated/sparklines/web/{days}d/2781/1.svg'

bytes = urlopen(url).read().decode("utf-8").replace("fill-opacity:0", "fill-opacity:1")

# print(bytes)

outfile = "btc.png"

svg2png(bytestring=bytes, write_to=outfile, scale=3.9)

font = 'Futura.ttc'

try:
    logging.info("Bitcoin")

    epd = epd7in5bc.EPD()

    logging.info("Init and Clear")
    epd.init()
    epd.Clear()

    newimage = Image.open(outfile).convert("L")

    enhancer = ImageEnhance.Contrast(newimage)
    newimage = enhancer.enhance(5)

    font_big = ImageFont.truetype(os.path.join(fontdir, font), 32)
    font_small = ImageFont.truetype(os.path.join(fontdir, font), 16)

    blackimage1 = Image.new('L', (epd.width, epd.height), 255)
    redimage1 = Image.new('L', (epd.width, epd.height), 255)

    drawblack = ImageDraw.Draw(blackimage1)
    drawred = ImageDraw.Draw(redimage1)

    # draw btc price
    drawblack.text((20, 20), f'1 BTC = {btc_price_eur}€', font=font_big, fill=0)

    fear_and_greed_left = 484

    # draw fear and greed value
    drawblack.text((fear_and_greed_left, 22), f'Fear & Greed: {fear_and_greed_value}', font=font_small, fill=0)

    # draw fear and greed label - red if below 50
    if(fear_and_greed_value >= 50):
        drawblack.text((fear_and_greed_left, 38), fear_and_greed_label, font=font_small, fill=0)
    else:
        drawred.text((fear_and_greed_left, 38), fear_and_greed_label, font=font_small, fill=0)

    # draw price graph - red if current price is below 24h price
    if(price_positive):
        blackimage1.paste(newimage, (0,108))
    else:
        redimage1.paste(newimage, (0,108))

    # draw block time
    drawblack.text((22, 326), f'Block time: {block_time}', font=font_small, fill=0)

    # draw moscow time
    drawblack.text((20, 346), f'Moscow Time: {moscow_time}', font=font_small, fill=0)

    # draw fees
    drawblack.text((384, 326), f"Fast: {fees['fastestFee']}sat/vB\n60m: {fees['hourFee']}sat/vB", font=font_small, fill=0)
    drawblack.text((514, 326), f"30m: {fees['halfHourFee']}sat/vB\nmin: {fees['minimumFee']}sat/vB", font=font_small, fill=0)



    epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5bc.epdconfig.module_exit()
    exit()
