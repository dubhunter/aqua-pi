#!/usr/bin/env python
from time import sleep
import spidev
import requests
import os
import RPi.GPIO as GPIO

LED = 4

spi = spidev.SpiDev()
spi.open(0, 0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)


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

    if light < 200:
        GPIO.output(LED, True)
    else:
        GPIO.output(LED, False)

    sleep(1)
