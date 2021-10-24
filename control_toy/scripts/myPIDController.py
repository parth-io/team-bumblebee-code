#!/usr/bin/env python

import time
import rospy
from std_msgs.msg import Float64, Bool

"""
You need to complete the following 3 steps to get this script to work:
2. Implement your PID Controller
3. Tune your PID Controller
"""

#declaration of global variables
global depth
global setpoint
setpoint = 0
depth = 0

#Declaration of callback functions
def SetPointCallback(msg):
    global setpoint
    setpoint = msg.data

def PIDControlCallback(msg):
    global depth
    depth = msg.data
    
class Area_under_curve:
    def __init__(self, iteration_time):
        self.iteration_time = iteration_time
        self.current_area_under_curve = 0
        
    def set_current_area_under_curve(self, current_error): #right riemann sum vs midpoint riemann sum vs trapezoidal
        self.current_area_under_curve = self.current_area_under_curve + current_error * self.iteration_time
        
    def get_current_area_under_curve(self):
        return self.current_area_under_curve


#Main
if __name__ == '__main__':
    rospy.init_node('PID_Controller')
    pub_thrust = rospy.Publisher('/simulator/thruster', Float64, queue_size=10)
    rospy.Subscriber('/simulator/setpoint', Float64, SetPointCallback)
    rospy.Subscriber('/simulator/depth', Float64, PIDControlCallback)
    
    print("Time to rock and roll")

    """
    Our assumption: Distance is measured in metres and our update interval is a constant 50 ms.
    For fun, assume that the max speed of the thruster is 8 m/s (0.4 metres per 50 ms) and that
    our vehicle sinks at a constant 2 m/s (0.1 metres per 50 ms).
    """
    #Step 3: Tune your PID Controller
    KP = 0.0009      #What Proportional value is good?
    KI = 0.000001025     #What integral value is good?
    KD = 0.00045      #What differential value is good?
    bias = 0    #Is a bias necessary?

    #Declare all the variables that you need here!
    iteration_time = 0.05 #Assume constant update intervals.
    previous_error = 0
    current_error = 0
    distance_to_correct = 0
    area_under_curve = Area_under_curve(iteration_time)
        

    while not rospy.is_shutdown():

        """
        ==================================================================================
        TODO: Implement your PID Control code here.
        Hint: You may need to declare a few more variables.
        The result of your PID Controller should be stored in the variable named "thrust".
        Note that a +ve thrust is upwards while -ve thrust is downwards.
        ==================================================================================
        """
        #Step 2: Add your PID Controller code here.
        current_error = depth - setpoint
        area_under_curve.set_current_area_under_curve(current_error)
        distance_to_correct = KP * current_error + KI * area_under_curve.get_current_area_under_curve() + KD * ((current_error - previous_error) / iteration_time)
        print(current_error, area_under_curve.get_current_area_under_curve(), distance_to_correct, distance_to_correct / iteration_time)
        previous_error = current_error
        thrust = distance_to_correct / iteration_time
        if abs(distance_to_correct) < 0.005: #a bias is necessary here though
            thrust = thrust + 0.1
        """
        Just for fun,
        Assume that the equipment is experiencing a constant acceleration due to gravity,
        hence, we do not need to worry about moving downwards.
        To avoid wearing out the hypothetical thruster and save energy,
        we can stop the motor instead of propelling the equipment downwards.
        """
        if thrust > 0.4:
            thrust = 0.4
        elif thrust < 0.0:
            thrust = 0.0

        pub_thrust.publish(Float64(thrust))
        #print("Depth: {0:.4f} thrust: {1:.4f}".format(round(depth, 5), round(thrust, 5)))
        time.sleep(iteration_time)

    print("Shutting Down PID Controller...")
    print("Done")
