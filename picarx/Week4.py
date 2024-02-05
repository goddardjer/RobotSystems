import concurrent.futures
import time
try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC
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
    
    def producer(self, bus, delay):
        while True:
            bus.write(self.read())
            time.sleep(delay)



class Interpreter:
    def __init__(self, sensitivity=50, polarity='dark'):
        self.sensitivity = sensitivity
        self.polarity = polarity
        self.left = 0
        self.right = 0
        self.center = 0

    def interpret(self):
        edge_left = abs(self.left - self.center)
        edge_right = abs(self.right - self.center)

        if self.polarity == 'dark':
            off_center = (edge_left - edge_right) / self.sensitivity
        else:
            off_center = (edge_right - edge_left) / self.sensitivity

        # Clamp the off_center value between -1 and 1
        off_center = max(min(off_center, 1), -1)

        return off_center
    
    def consumer_producer(self, sensor_bus, interpreter_bus, delay):
        while True:
            sensor_values = sensor_bus.read()
            self.left, self.center, self.right = sensor_values
            interpreted_values = self.interpret()
            interpreter_bus.write(interpreted_values)
            time.sleep(delay)

class Controller(object):
    def __init__(self):
        pass

    def control(self, offset):
        # Get the offset from the interpreter

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
    
    def consumer(self, interpreter_bus, delay, car):
        while True:
            interpreted_values = interpreter_bus.read()
            steering_angle = self.control(interpreted_values)
            car.set_dir_servo_angle(steering_angle)
            time.sleep(delay)


if __name__ == '__main__':
    car = pixi.Picarx()
    sensor_bus = Bus()
    interpreter_bus = Bus()
    sensor = Sensor()
    interpreter = Interpreter()
    controller = Controller()
    car.forward(35)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(sensor.producer, sensor_bus, .001)
        eInterpreter = executor.submit(interpreter.consumer_producer, sensor_bus, interpreter_bus,.01)
        eController = executor.submit(controller.consumer, interpreter_bus, .1, car)
    eSensor.result()
    eInterpreter.result()
    eController.result()