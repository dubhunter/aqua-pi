import time
import requests
import json
import spidev
from collections import deque
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

Scripts.TRANSFER = Scripts.WHITE_FLASH


class AquaPi:
    DEBUG = False
    HOST = 'http://aqua.willandchi.com'
    ENDPOINT_POLL = '/v1/poll'
    ENDPOINT_EVENT = '/v1/events'
    timeout = 3
    led_fade_speed = 64

    def __init__(self):
        self.log('AquaPi initializing...')

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_POWER, GPIO.OUT)

        self.led = BlinkM()
        self.led.reset()
        self.led.set_fade_speed(self.led_fade_speed)
        # self.led.write_script_line(Scripts.TRANSFER, 0, 10, 'c', 0xff, 0xff, 0xff)
        # self.led.write_script_line(Scripts.TRANSFER, 1, 10, 'c', 0x00, 0x00, 0x00)

        self.spi = spidev.SpiDev()
        self.spi.open(0, SPI_ADC)

        self.sensor_light = Sensor(self.spi, ADC_LIGHT)
        self.sensor_liquid = Sensor(self.spi, ADC_LIQUID)

        self.metro_sensor_sample = Metro(500)
        self.metro_sensor_send = Metro(30000)
        self.metro_poll = Metro(6000)
        self.metro_health = Metro(180000)

        self.events = deque()
        self.running = False
        self.current_color = False

        self.happy()

    def loop(self):
        if self.metro_health.check():
            self.log("Health checks are failing. I'm sad :(")
            self.sad()
            self.event('network', 'error')

        if self.metro_sensor_sample.check():
            self.sensor_light.read()
            self.sensor_liquid.read()

        if self.metro_sensor_send.check():
            self.event('light', self.sensor_light.value())
            # 0in: 512, 10in: 202, 12in: 138
            # sensor degradation, using 242
            self.event('liquid', round((512.0 - self.sensor_liquid.value()) / 270.0 * 100.0, 2))

        if self.metro_poll.check():
            self.poll()

        self.send_events()

        time.sleep(0.1)

    def poll(self):
        self.log('Polling...')

        self.led_script(Scripts.TRANSFER)
        self.current_color = colors.white

        try:
            r = requests.get(self.HOST + self.ENDPOINT_POLL,
                             auth=(credentials.username, credentials.password),
                             timeout=self.timeout)
            self.log(r.text)

            if r.status_code == 200:
                data = r.json()
                if len(data):
                    self.power(data['power'] == 'on')

                self.metro_health.reset()
                self.happy()
            else:
                self.log('Polling non-200 response')
                self.event('network', 'error')

        except requests.RequestException:
            self.log('Polling failed')
            self.event('network', 'error')

    def send_events(self):
        if len(self.events) > 0:
            self.log('Sending event...')

            event = self.events.popleft()
            self.log(json.dumps(event))

            self.led_script(Scripts.TRANSFER)
            self.current_color = colors.white

            try:
                r = requests.post(self.HOST + self.ENDPOINT_EVENT,
                                  data=event,
                                  auth=(credentials.username, credentials.password),
                                  timeout=self.timeout)
                if r.status_code == 200:
                    self.metro_health.reset()
                    self.happy()
                else:
                    self.log('Sending event non-200 response')
                    self.event('network', 'error')

            except requests.RequestException:
                self.log('Sending event failed')
                self.event('network', 'error')

    def power(self, on):
        if on:
            GPIO.output(PIN_POWER, True)
            self.running = True
            self.happy()
            self.event('power', 'on')
        else:
            GPIO.output(PIN_POWER, False)
            self.running = False
            self.happy()
            self.event('power', 'off')

    def event(self, name, data):
        self.events.append({
            'event': name,
            'data': data
        })

    def sad(self):
        if self.current_color != colors.red:
            self.led_script(Scripts.RED_FLASH)
            self.current_color = colors.red

    def happy(self):
        if self.running:
            if self.current_color != colors.blue:
                self.led_script(Scripts.BLUE_FLASH)
                self.current_color = colors.blue
        else:
            if self.current_color != colors.green:
                self.led_color(colors.green)
                self.current_color = colors.green

    def led_script(self, script):
        try:
            self.led.reset()
            self.led.play_script(script)
        except IOError:
            self.log('Playing led script failed')
            self.event('led', 'error')

    def led_color(self, color):
        try:
            self.led.reset()
            self.led.go_to_hex(color)
        except IOError:
            self.log('Changing led color failed')
            self.event('led', 'error')

    def log(self, msg):
        if self.DEBUG:
            print "[{}] {}".format(time.strftime('%Y-%m-%d %H:%M:%S'), msg)
