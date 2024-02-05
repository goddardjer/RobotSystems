try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC

import concurrent.futures
import time
import picarx_improved as pixi


class Bus:
    def __init__(self):
        self.message = None

    def write(self, message):
        self.message = message

    def read(self):
        return self.message



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




class Interpreter:
    def __init__(self, sensor, sensitivity=50, polarity='dark'):
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


    

class Controller(object):
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def control(self):
        # Get the offset from the interpreter
        offset = self.interpreter.interpret()

        # Define the steering angles for left, kinda left, center, kinda right, right
        steering_angles = [30, 15, 0, -15, -30]

        # Calculate the steering angle based on the offset
        if offset < -0.5:
            steering_angle = steering_angles[0]  # Left
        elif -0.5 <= offset < -0.1:
            steering_angle = steering_angles[1]  # Kinda left
        elif -0.1 <= offset <= 0.1:
            steering_angle = steering_angles[2]  # Center
        elif 0.1 < offset <= 0.5:
            steering_angle = steering_angles[3]  # Kinda right
        else:
            steering_angle = steering_angles[4]  # Right

        # Return the commanded steering angle
        return steering_angle
    
    

if __name__ == '__main__':
    bus = Bus.Bus()
    sensor = Sensor(bus)
    interpreter = Interpreter(sensor, bus)
    controller = Controller(bus)
    delay = 0.1
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(sensor.prouducer, bus, delay)
        eInterpreter = executor.submit(interpreter.consumer_prouducer, bus, bus, delay)
        eController = executor.submit(controller.consumer, bus, delay)