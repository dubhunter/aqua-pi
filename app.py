#!/usr/bin/env python
from lib.hyduino import Hyduino


hyduino = Hyduino()
hyduino.DEBUG = True

while 1:
    hyduino.loop()