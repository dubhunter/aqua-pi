from analogsensor import AnalogSensor

# Measured with multi-meter
REFERENCE_VOLTAGE = 4.6


class TempSensor(AnalogSensor):
    """TMP36 Handling Class

    Based on https://learn.adafruit.com/tmp36-temperature-sensor/using-a-temp-sensor

    The resolution is 10 mV / degree centigrade with a 500 mV offset to allow for negative temperatures
    """

    def centigrade(self):
        voltage = self.value() * REFERENCE_VOLTAGE / 1024.0
        # Convert from 10 mv per degree with 500 mV offset to degrees ((voltage - 500mV) times 100)
        return (voltage - 0.5) * 100

    def fahrenheit(self):
        return (self.centigrade() * 9.0 / 5.0) + 32.0
