
from yaml import scan
import rospy
import numpy as np
import pandas as pd
import os

# MSG ROS
from sensor_msgs.msg import Joy
from sensor_msgs.msg import NavSatFix, Imu, LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Vector3Stamped, Point
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Empty, String

from tf.transformations import euler_from_quaternion, quaternion_from_euler

class Vector3D:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class DataRecord:
    def __init__(self):
        self.x = []
        self.y = []
        self.theta = []

        self.laser = []

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

    def record(self, x, y, theta, laser, vx, vy, wz):
        
        self.x.append(x)
        self.y.append(y)
        self.theta.append(theta)
        self.laser.append(laser)
        self.vx.append(vx)
        self.vy.append(vy)
        self.wz.append(wz)
        
    def save(self):
    
        self.df["x"] = self.x
        self.df["y"] = self.y
        self.df["theta"] = self.theta

        l = np.array(self.laser)
        for i in range(18):
            aux = 'p' + str(i)
            self.df[str(aux)] = l[:,i]
        self.df["vx"] = self.vx
        self.df["vy"] = self.vx
        self.df["wz"] = self.wz
        self.df.to_csv(r'test.csv', index=False)
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

        # DATA RECORD
        self.data_record = DataRecord()
        
        
        

        # JOY VARIABLES
        self.data = Joy()
        self.rate = rospy.Rate(500) 
        self.data.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # Lx  Ly  Ry Rx
        self.data.buttons = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #1  2   3   4   L1  R1  L2  R2  SELECT  START   L3  R3 
        self.move = Twist()

        # DATA QUADROTOR
        self.scan_data = LaserScan()
        self.scan_data_r = np.zeros(18)

        self.gaz_data = ModelStates()
        self.pos_gaz = Point()
        self.rot_gaz = Vector3D()
        
        # TIME WAILT 1s NECESSARY FOR SUBSCRIBER CALLBACK
        rospy.sleep(1)
        pass
    def rot_print(self):
        def print_angle(name, array):
         
            n = 5
            print("Angle " + str(name) + ": " + "Yaw: " + str(round(np.degrees(array.z), n)) + " Pitch: " + str(round(np.degrees(array.x), n))  + " Row: " + str(round(np.degrees(array.y), n)))

        while True:
            os.system('clear')
            # print_angle("Imu", self.rot_imu)
            print_angle("Gaz", self.rot_gaz)
            # print(self.pos_gaz)
            self.rate.sleep()
    
    def record_sensor(self):
        
        while True:
           self.rot_print()

            # self.data_record.record(self.pos_gaz.x, self.pos_gaz.y, self.rot_gaz.x, self.scan_data_r, self.move.linear.x, self.move.linear.y, self.move.angular.z)
            # self.rate.sleep()
            # if(self.data.buttons[0] == 1):
            #     self.data_record.save()
            #     print("END")
            #     break


    def callback_joy(self, msg_joy):
        self.data = msg_joy
        self.move.angular.z = self.data.axes[3]
        self.move.linear.x = self.data.axes[1]
        self.move.linear.y = self.data.axes[0]
        self.cmd_vel_pub.publish(self.move)

    def scan_callback(self, msg):
        # scan data brute - 1081 Point
        self.scan_data = msg
        t = len(self.scan_data.ranges)

        # scan data reduction - 18 evenly spaced points
        if(t == 1081):
            index = np.linspace(0,1080 - int(1080/18), 18)
            for i in range(18):
                    aux = self.scan_data.ranges[int(index[i])]
                    if(str(aux) == "inf"): 
                        self.scan_data_r[i] = 100
                    else:
                        self.scan_data_r[i] = aux
        # print(self.scan_data_r)

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
TeleopControl.record_sensor()
# rospy.spin()