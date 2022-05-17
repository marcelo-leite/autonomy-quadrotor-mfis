
import rospy
import numpy as np
import pandas as pd

# MSG ROS
from sensor_msgs.msg import Joy
from sensor_msgs.msg import NavSatFix, Imu, LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Vector3Stamped, Point
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Empty, String

from tf.transformations import euler_from_quaternion, quaternion_from_euler



class PS2Control:
    def __init__(self):
        # SUBSCRIBER
        # SUBSCRIBER
        rospy.Subscriber("joy", Joy, self.callback_joy)
        
        # PUBLISHER 
        self.land_pub = rospy.Publisher("/land", Empty, queue_size=1)
        self.takeoff_pub = rospy.Publisher("/takeoff", Empty, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

        # JOY VARIABLES
        self.data = Joy()
        self.rate = rospy.Rate(10) 
        self.data.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # Lx  Ly  Ry Rx
        self.data.buttons = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #1  2   3   4   L1  R1  L2  R2  SELECT  START   L3  R3 
        self.move = Twist()

        pass
    def record_data(self):

        self.rate.sleep()

    def callback_joy(self, msg_joy):
        self.data = msg_joy
        self.move.angular.z = self.data.axes[3]
        self.move.linear.x = self.data.axes[1]
        self.move.linear.y = self.data.axes[0]
        self.cmd_vel_pub.publish(self.move)

        

        

rospy.init_node('hector_joy', anonymous=True)
TeleopControl = PS2Control()
# TeleopControl.main()
rospy.spin()