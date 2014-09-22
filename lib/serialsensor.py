import re
import io


# Sensor attached to TX/RX pins
class SerialSensor:
    def __init__(self, serial_conn):
        self.connection = serial_conn
        self.reading = 0
        self.count = 0

    def read(self):
        print 'read'
        line = ''
        while True:
            r = self.connection.read()
            print r
            if r == '/r':
                break
            print ''.join([line, r])
            line = ''.join([line, r])

        print 'done'
        print line
        print re.sub('[^0-9]', '', line)
        self.reading += int(re.sub('[^0-9]', '', line))
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