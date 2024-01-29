try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC
import Sensor
import time

class Interpreter:
    def __init__(self, sensor, sensitivity=10, polarity='dark'):
        self.sensor = sensor
        self.sensitivity = sensitivity
        self.polarity = polarity
        self.left = 0
        self.right = 0
        self.center = 0

    def interpret(self):
        self.left, self.center, self.right = self.sensor.read()
        edge_left = abs(self.left - self.center)
        edge_right = abs(self.right - self.center)

        if self.polarity == 'dark':
            off_center = (edge_left - edge_right) / self.sensitivity
        else:
            off_center = (edge_right - edge_left) / self.sensitivity

        # Clamp the off_center value between -1 and 1
        off_center = max(min(off_center, 1), -1)

        return off_center
    
if __name__ == '__main__':
    sensor = Sensor.Sensor()
    interpreter = Interpreter(sensor)
    while True:
        print(interpreter.interpret())
        time.sleep(1)