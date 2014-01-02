#!/usr/bin/env python
from lib.aquapi import *

spi = spidev.SpiDev()
spi.open(0, SPI_ADC)
sensor_liquid = Sensor(spi, ADC_LIQUID)

while 1:
    sensor_liquid.read()
    print 512 - sensor_liquid.value()
    time.sleep(0.5)