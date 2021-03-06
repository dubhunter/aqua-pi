import time


class Metro:
    def __init__(self, interval_millis):
        self.interval_millis = 0
        self.previous_millis = 0
        self.interval(interval_millis)
        self.reset()

    def time(self):
        return int(time.time() * 1000)

    def interval(self, interval_millis):
        self.interval_millis = interval_millis

    def check(self):
        now = self.time()

        if self.interval <= 0:
            self.previous_millis = now
            return True

        if now - self.previous_millis >= self.interval_millis:
            self.previous_millis += self.interval_millis
            return True

        return False

    def reset(self):
        self.previous_millis = self.time()
