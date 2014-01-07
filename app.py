#!/usr/bin/env python
from lib.aquapi import AquaPi

AquaPi.DEBUG = True
aquapi = AquaPi()

while 1:
    aquapi.loop()