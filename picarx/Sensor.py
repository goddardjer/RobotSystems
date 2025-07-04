try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC

import time

class Sensor:
    def __init__(self):
        self.channel1, self.channel2, self.channel3 = ADC('A0'), ADC('A1'), ADC('A2')

    def read(self):
        return [self.channel1.read(), self.channel2.read(), self.channel3.read()]


if __name__ == '__main__':
    sensor = Sensor()
    while True:
        print(sensor.read())
        time.sleep(1)