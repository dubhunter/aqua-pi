#!/usr/bin/env python
from lib.aquapi import *

spi = spidev.SpiDev()
spi.open(0, SPI_ADC)
sensor_liquid = Sensor(spi, ADC_LIQUID)

while 1:
    sensor_liquid.read()
    reading = sensor_liquid.value()
    print reading
    time.sleep(0.5)