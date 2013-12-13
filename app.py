#!/usr/bin/env python
from lib.aquapi import AquaPi

aquapi = AquaPi()
aquapi.DEBUG = True

while 1:
    aquapi.loop()