try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC
import picarx_improved as pixi
import Interpreter
import Sensor
import time



class Controller(object):
    def __init__(self, interpreter, scaling_factor=-10.0):
        self.interpreter = interpreter
        self.scaling_factor = scaling_factor

    def control(self):
        # Get the offset from the interpreter
        offset = self.interpreter.interpret()

        # Calculate the steering angle based on the offset and scaling factor
        steering_angle = offset * self.scaling_factor

        # Return the commanded steering angle
        return steering_angle
    
if __name__ == '__main__':
    car = pixi.Picarx()
    sensor = Sensor.Sensor()
    interpreter = Interpreter.Interpreter(sensor)
    controller = Controller(interpreter)
    car.forward(35)
    while True:
        steering_angle = controller.control()
        print(f'Setting steering angle to: {steering_angle}')  # Debug print
        car.set_dir_servo_angle(steering_angle)
        