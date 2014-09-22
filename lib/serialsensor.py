import re
import io


# Sensor attached to TX/RX pins
class SerialSensor:
    def __init__(self, serial_conn):
        self.connection = io.TextIOWrapper(io.BufferedRWPair(serial_conn, serial_conn),
                                           errors='ignore',
                                           newline='\r',
                                           line_buffering=True)
        self.reading = 0
        self.count = 0

    def read(self):
        print 'readline'
        print self.connection.read()
        r = self.connection.readline()
        print r
        self.reading += int(re.sub('[^0-9]', '', r))
        print self.reading
        self.count += 1

    def value(self):
        if self.count > 0:
            v = self.reading / self.count
        else:
            v = 0
        self.reading = 0
        self.count = 0
        return v