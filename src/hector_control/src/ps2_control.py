
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

class DataRecord:
    def __init__(self):
        self.x = []
        self.y = []
        self.theta = []
        
        self.vx = []
        self.vy = []
        self.wz = []

        self.df = pd.DataFrame({ 'x': [], 
                            'y': [], 
                            'theta' : [], 
                            'vx' : [],
                            'vy' : [],
                            'wz' : [],
                        })

    def record(self, x, y, theta, vx, vy, wz):
        
        self.x.append(x)
        self.y.append(y)
        self.theta.append(theta)

        self.vx.append(vx)
        self.vy.append(vy)
        self.wz.append(wz)
    def save(self):

        pass

        


class PS2Control:
    def __init__(self):
        # SUBSCRIBER
        self.joy_sub = rospy.Subscriber("joy", Joy, self.callback_joy)
        self.scan_sub = rospy.Subscriber("/scan", LaserScan, self.scan_callback)
        
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

        # SCAN VARIABLE
        self.scan_data = LaserScan()

        pass
    def record_data(self):
        if(self.data[1] == 1):
            self.rate.sleep()

    def callback_joy(self, msg_joy):
        self.data = msg_joy
        self.move.angular.z = self.data.axes[3]
        self.move.linear.x = self.data.axes[1]
        self.move.linear.y = self.data.axes[0]
        self.cmd_vel_pub.publish(self.move)

    def scan_callback(self, msg):
        self.scan_data = msg

        

rospy.init_node('hector_joy', anonymous=True)
TeleopControl = PS2Control()
# TeleopControl.main()
rospy.spin()