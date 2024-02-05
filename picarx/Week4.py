import concurrent.futures
import time
try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC

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

def sensor_function(bus, delay):
    sensor = Sensor()
    while True:
        bus.write(sensor.read())
        time.sleep(delay)

def interpreter_function(sensor_bus, interpreter_bus, delay):
    while True:
        sensor_data = sensor_bus.read()
        if sensor_data is not None:
            interpreter = Interpreter(sensor_data)
            interpreter_bus.write(interpreter.interpret())
        time.sleep(delay)

def controller_function(interpreter_bus, delay):
    while True:
        interpreter_data = interpreter_bus.read()
        if interpreter_data is not None:
            controller = Controller(interpreter_data)
            print(controller.control())
        time.sleep(delay)

if __name__ == '__main__':
    sensor_bus = Bus()
    interpreter_bus = Bus()
    delay = 0.1
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(sensor_function, sensor_bus, delay)
        eInterpreter = executor.submit(interpreter_function, sensor_bus, interpreter_bus, delay)
        eController = executor.submit(controller_function, interpreter_bus, delay)