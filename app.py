#!/usr/bin/env python
import sys
from lib.aquapi import AquaPi

log = open('/var/log/aqua-pi.log', 'a', 0)
sys.stdout = log
sys.stderr = log

# AquaPi.DEBUG = True
aquapi = AquaPi()

while 1:
    aquapi.loop()
