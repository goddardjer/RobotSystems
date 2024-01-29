# If the import of "robot_hat" fails, it will import from "sim_robot_hat" instead.
try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC

import picarx_improved as car_module

class Sensor:
    def __init__(self):
        self.channel1, self.channel2, self.channel3 = ADC('A0'), ADC('A1'), ADC('A2')

    def read(self):
        return self.channel1, self.channel2, self.channel3

class Interpreter:
    def __init__(self, sensor, sensitivity=1000, polarity='dark'):
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
    def __init__(self, interpreter, scaling_factor=1.0):
        self.interpreter = interpreter
        self.scaling_factor = scaling_factor

    def control(self, car):
        # Get the offset from the interpreter
        offset = self.interpreter.interpret()

        # Calculate the steering angle based on the offset and scaling factor
        steering_angle = offset * self.scaling_factor

        # Steer the car
        car.steer(steering_angle)

        # Return the commanded steering angle
        return steering_angle

def auto_steering(sensor, interpreter, controller, delay=0.1):
    while True:
        # Read sensor values
        sensor_values = sensor.read()

        # Interpret sensor values
        offset = interpreter.interpret()

        # Control the car based on the interpreted values
        steering_angle = controller.control(car_module)

        # Move the car forward
        car_module.move_forward()

        # Print the steering angle for debugging
        print(f'Steering angle: {steering_angle}')

        # Delay to make the motion smooth
        sleep(delay)

if __name__ == "__main__":
    # Create instances of Sensor, Interpreter, and Controller
    sensor = Sensor()
    interpreter = Interpreter(sensor)
    controller = Controller(interpreter)

    # Start automatic steering
    auto_steering(sensor, interpreter, controller)