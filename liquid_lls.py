#!/usr/bin/env python
from lib.aquapi import *

spi = spidev.SpiDev()
spi.open(0, SPI_ADC)
sensor_liquid = AnalogSensor(spi, ADC_LIQUID)

while 1:
    sensor_liquid.read()
    reading = sensor_liquid.value()
    print reading
    print (LLS_EMPTY - reading) / (LLS_EMPTY - LLS_FULL) * 100.0
    time.sleep(0.5)
