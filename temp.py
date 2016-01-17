#!/usr/bin/env python
from lib.aquapi import *

spi = spidev.SpiDev()
spi.open(0, SPI_ADC)
sensor_temp = TempSensor(spi, ADC_TEMP)

while 1:
    sensor_temp.read()
    reading = sensor_temp.value()
    reading_c = sensor_temp.centigrade()
    reading_f = sensor_temp.fahrenheit()
    print "{}".format(reading)
    print "{} C".format(reading_c)
    print "{} F".format(reading_f)
    time.sleep(0.5)
