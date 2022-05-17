
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
        self.df = pd.DataFrame({ 
                            
                            'x': [], 
                            'y': [], 
                            'theta' : [],

                            'p0' : [],
                            'p1' : [],
                            'p2' : [],
                            'p3' : [],
                            'p4' : [],
                            'p5' : [],
                            'p6' : [],
                            'p7' : [],
                            'p8' : [],
                            'p9' : [],
                            'p10' : [],
                            'p11' : [],
                            'p12' : [],
                            'p13' : [],
                            'p14' : [],
                            'p15' : [],
                            'p16' : [],
                            'p17' : [],

                            'vx' : [],
                            'vy' : [],
                            'wz' : []
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
        self.gaz_sub = rospy.Subscriber("/ground_truth/state", Odometry, self.gaz_callback)
        
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

        # DATA QUADROTOR
        self.scan_data = LaserScan()
        self.gaz_data = ModelStates()
        self.pos_gaz = Point()


        pass
    def record_data(self):
        # if(self.data[1] == 1):
            
        while True:
            t = len(self.scan_data.ranges)
            print(t/18)
            # for i in np.linspace(0, t, t/18):
            #     print(i)
            self.rate.sleep()


    def callback_joy(self, msg_joy):
        self.data = msg_joy
        self.move.angular.z = self.data.axes[3]
        self.move.linear.x = self.data.axes[1]
        self.move.linear.y = self.data.axes[0]
        self.cmd_vel_pub.publish(self.move)

    def scan_callback(self, msg):
        self.scan_data = msg

    def gaz_callback(self, msg):
        self.gaz_data  = msg
        self.pos_gaz = self.gaz_data.pose.pose.position
        
        aux_orientation = self.gaz_data.pose.pose.orientation
        aux = euler_from_quaternion(quaternion=(aux_orientation.x, aux_orientation.y, aux_orientation.z, aux_orientation.w))
    
        self.rot_gaz.x = aux[0]
        self.rot_gaz.y = aux[1]
        self.rot_gaz.z = aux[2]
    
        pass
        

rospy.init_node('hector_joy', anonymous=True)
TeleopControl = PS2Control()
TeleopControl.record_data()
rospy.spin()