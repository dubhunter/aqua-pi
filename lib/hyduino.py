import time
import requests
import spidev
from collections import namedtuple, deque
from lib import colors
from lib import credentials
from lib.metro import Metro
from lib.sensor import Sensor
import RPi.GPIO as GPIO
from pyblinkm import BlinkM, Scripts

PIN_POWER = 4
SPI_ADC = 0
ADC_LIGHT = 0
ADC_LIQUID = 1

class Hyduino:
    DEBUG = False
    HOST = 'http://hyduino.willandchi.com'
    ENDPOINT_POLL = '/v1/poll'
    ENDPOINT_EVENT = '/v1/events'
    timeout = 1

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_POWER, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(0, SPI_ADC)

        self.led = BlinkM()

        self.sensor_light = Sensor(self.spi, ADC_LIGHT)
        self.sensor_liquid = Sensor(self.spi, ADC_LIQUID)

        self.metro_sensor_sample = Metro(500)
        self.metro_sensor_send = Metro(30000)
        self.metro_poll = Metro(10000)
        self.metro_health = Metro(180000)

        self.events = deque()

    def init(self):
        self.led.reset()

        self.led.play_script(Scripts.THUNDERSTORM)

        time.sleep(3)

        self.led.reset()
        self.led.fade_to_hex(colors.green)

    def loop(self):
        if self.metro_health.check():
            self.led.fade_to_hex(colors.red)
            self.event('network', 'error')

        if self.metro_sensor_sample.check():
            self.sensor_light.read()
            self.sensor_liquid.read()

        if self.metro_sensor_send.check():
            self.event('light', self.sensor_light.value())
            self.event('liquid', max(0, 500 - self.sensor_liquid.value()))

        if self.metro_poll.check():
            self.poll()

        self.send_events()

        time.sleep(0.1)

    def poll(self):
        try:
            r = requests.get(self.HOST + self.ENDPOINT_POLL,
                             auth=(credentials.username, credentials.password),
                             timeout=self.timeout)
            if r.status_code == 200:
                self.log(r.text)
                data = r.json()
                if len(data):
                    self.power(data.power == 'on')
            else:
                self.event('network', 'error')
        except:
            self.event('network', 'error')

    def send_events(self):
        if len(self.events) > 0:
            event = self.events.popleft()
            r = requests.post(self.HOST + self.ENDPOINT_EVENT,
                              data=event,
                              auth=(credentials.username, credentials.password),
                              timeout=self.timeout)
            if r.status_code != 200:
                self.event('network', 'error')

    def power(self, on):
        if on:
            GPIO.output(PIN_POWER, True)
            self.led.fade_to_hex(colors.blue)
            self.event('power', 'on')
        else:
            GPIO.output(PIN_POWER, False)
            self.led.fade_to_hex(colors.green)
            self.event('power', 'off')

    def event(self, name, data):
        self.events.append({
            'event': name,
            'data': data
        })

    def log(self, msg):
        if self.DEBUG:
            print msg
