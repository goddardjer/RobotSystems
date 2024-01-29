try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC
import Interpreter
import time



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