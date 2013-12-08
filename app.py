#!/usr/bin/env python
from time import sleep
import spidev
import requests
import os

DEBUG = 0

spi = spidev.SpiDev()
spi.open(0, 0)


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1

    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    return ((r[1] & 3) << 8) + r[2]

while True:
    # read the analog pin
    light = readadc(0)

    print "Current light reading: {}".format(light)

    sleep(1)