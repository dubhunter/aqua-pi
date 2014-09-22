#!/usr/bin/env python
from lib.aquapi import *
import serial

sio = serial.Serial('/dev/ttyAMA0', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
sensor_liquid = SerialSensor(sio)

while 1:
    sensor_liquid.read()
    reading = sensor_liquid.value()
    print reading
    print (URF_EMPTY - reading) / (URF_EMPTY - URF_FULL) * 100.0
    time.sleep(0.5)