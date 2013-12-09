import spidev


# Sensor attached to MCP3008 chip (read through SPI)
# 8 possible ADC's (0-7)
class Sensor:
    def __init__(self, spi_conn, adc_pin):
        if adc_pin > 7 or adc_pin < 0:
            raise Exception('adc_num must be between 0 and 7')

        self.connection = spi_conn
        self.pin = adc_pin
        self.reading = 0
        self.count = 0

    def read(self):
        r = self.connection.xfer2([1, (8 + self.pin) << 4, 0])
        self.reading += ((r[1] & 3) << 8) + r[2]

    def value(self):
        v = self.reading / self.count
        self.reading = 0
        self.count = 0
        return v