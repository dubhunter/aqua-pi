import re


# Sensor attached to TX/RX pins
class SerialSensor:
    def __init__(self, serial_conn):
        self.connection = serial_conn
        self.reading = 0
        self.count = 0

    def read(self):
        r = self.connection.readline(eol='\r')
        self.reading += int(re.sub('[^0-9]', '', r))
        self.count += 1

    def value(self):
        if self.count > 0:
            v = self.reading / self.count
        else:
            v = 0
        self.reading = 0
        self.count = 0
        return v