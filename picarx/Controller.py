try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC
import picarx_improved as pixi
import Interpreter
import Sensor
import time



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
    car = pixi.Picarx()
    sensor = Sensor.Sensor()
    interpreter = Interpreter.Interpreter(sensor)
    controller = Controller(interpreter)
    car.forward(35)
    try:
        while True:
            steering_angle = controller.control()
            print(f'Setting steering angle to: {steering_angle}')  # Debug print
            car.set_dir_servo_angle(steering_angle)
    except KeyboardInterrupt:
        # Stop the car when Ctrl+C is pressed
        car.stop()
        print("Program exited gracefully")