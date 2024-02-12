#!/usr/bin/python3
"""
This file demonstrates the basic operation of a RossROS program.
"""

import rossros as rr
import logging
import time
import math
import picarx_improved as pixi
try:
    from robot_hat import ADC
except ImportError:
    from sim_robot_hat import ADC

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)

""" First Part: Generation and processing functions """

class Sensor:
    def __init__(self):
        self.channel1, self.channel2, self.channel3 = ADC('A0'), ADC('A1'), ADC('A2')

    def read(self):
        #print("Sensor values: ", self.channel1.read(), self.channel2.read(), self.channel3.read())
        return [self.channel1.read(), self.channel2.read(), self.channel3.read()]
    
class UltraSonic:
    def __init__(self, px):
        self.px = px

    def read(self):
        print("distance: ", self.px.get_distance())
        return self.px.get_distance()
    

class Interpreter:
    def __init__(self, sensitivity=50, polarity='dark'):
        self.sensitivity = sensitivity
        self.polarity = polarity
        self.left = 0
        self.right = 0
        self.center = 0

    def interpret(self, sensor_bus):
        #print("Interpreting sensor values")
        self.left, self.center, self.right = sensor_bus 
        #print("After read)")
        edge_left = abs(self.left - self.center)
        edge_right = abs(self.right - self.center)

        #print("After math)")
        if self.polarity == 'dark':
            off_center = (edge_left - edge_right) / self.sensitivity
        else:
            off_center = (edge_right - edge_left) / self.sensitivity

        #print("After math2)")

        # Clamp the off_center value between -1 and 1
        off_center = max(min(off_center, 1), -1)

        #print("Off center: ", off_center)

        return off_center

class Controller(object):
    def __init__(self, car):
        self.car = car

    def control(self, offset, ultraSonicDistance):
        #print(f"offset: {offset}, ultraSonicDistance: {ultraSonicDistance}")

        # Define the steering angles for left, kinda left, center, kinda right, right
        steering_angles = [30, 15, 0, -15, -30]

        #print("Top of control")

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

        #print("Steering angle: ", steering_angle)

        car.set_dir_servo_angle(steering_angle)

        if ultraSonicDistance >= 10:
            car.forward(25)
        else:
            car.backward(5)


        

""" Second Part: Create buses for passing data """

# Initiate data and termination busses
bSensor_Interp = rr.Bus(0, "Sensor to Interpreter Bus")
bInterp_Control = rr.Bus(0, "Interpreter to Control Bus")
bUltraSonic_Interp = rr.Bus(0, "UltraSonic to Interpreter Bus")
bTerminate = rr.Bus(0, "Termination Bus")

""" Third Part: Wrap signal generation and processing functions into RossROS objects """

# Wrap the square wave signal generator into a producer
sensor = Sensor()
readSensor = rr.Producer(sensor.read, bSensor_Interp, 0.01, bTerminate, "Read sensor values")

# Wrap the multiplier function into a consumer-producer
interpreter = Interpreter()
interpSensor = rr.ConsumerProducer(interpreter.interpret, bSensor_Interp, bInterp_Control, 0.05, bTerminate, "Interpret sensor values and write to control bus")

car = pixi.Picarx()

ultraSonic = UltraSonic(car)
readUltraSonic = rr.Producer(ultraSonic.read, bUltraSonic_Interp, 0.01, bTerminate, "Read ultrasonic values")
#ultraSonicAvoidance = rr.Producer(ultraSonic.obsitcal_avoidance, bTerminate, 0.01, bTerminate, "UltraSonic avoidance")

controller = Controller(car)
controlPicarx = rr.Consumer(controller.control, (bInterp_Control, bUltraSonic_Interp), 0.1, bTerminate, "Control Picarx with interpreted values")

""" Fourth Part: Create RossROS Printer and Timer objects """

# Make a printer that returns the most recent wave and product values
printBuses = rr.Printer([bSensor_Interp, bInterp_Control, bUltraSonic_Interp], 0.1, bTerminate, "Print raw and derived data", "Data bus readings are: ")

# Make a timer (a special kind of producer) that turns on the termination bus when it triggers
terminationTimer = rr.Timer(bTerminate, 5.0, 0.1, bTerminate, "Termination timer")

""" Fifth Part: Concurrent execution """

# Create a list of producer-consumers to execute concurrently
producer_consumer_list = [readSensor, interpSensor, controlPicarx, readUltraSonic, printBuses, terminationTimer]

# Execute the list of producer-consumers concurrently
rr.runConcurrently(producer_consumer_list)
