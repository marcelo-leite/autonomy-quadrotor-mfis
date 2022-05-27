
# VERSION STABLE

# from time import sleep
from importlib.resources import path
from math import radians
import re
from threading import Thread
from turtle import degrees, forward
import numpy as np
import geopy as gp
import os

import rospy

from sensor_msgs.msg import Joy
from sensor_msgs.msg import NavSatFix, Imu, LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Vector3Stamped, Point
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Empty, String

from tf.transformations import euler_from_quaternion, quaternion_from_euler

from system.obstacle_avoid_old import ObstacleAvoid
import csv




class Vector2D:
    def __init__(self):
        self.x = 0
        self.y = 0

class Vector3D:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class DataViwer():
    
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        self.t = []
        self.beta = []
        self.alfa = []
        pass

    def coleta_data(self, x, y):
        self.x.append(x)
        self.y.append(y)
        pass
        
    def parser_csv(self):
        with open('datapose.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["x", "y"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i], self.y[i]])
        pass

class HectorNav:
    def __init__(self):

        # BRUTE DATAS
        self.rate = rospy.Rate(10) 
        self.imu_data = Imu()
        self.mag_data = Vector3Stamped()
        self.navsat_data = NavSatFix()
        self.gaz_data = ModelStates()
        self.scan_data = LaserScan()

        # ROTATIONS 
        self.rot_imu = Vector3D()
        self.rot_mag = Vector3D()
        self.rot_gaz = Vector3D()

        # POSITIONS
        self.pos_gaz = Point()

        # SAVE POSE
        self.x = []
        self.y = []

        # SUBSCRIBER
        self.navsat_sub = rospy.Subscriber("/fix", NavSatFix, self.nav_callback)
        self.imu_sub = rospy.Subscriber("/raw_imu", Imu, self.imu_callback)
        self.mag_sub = rospy.Subscriber("/magnetic", Vector3Stamped, self.mag_callback)
        self.gaz_sub = rospy.Subscriber("/ground_truth/state", Odometry, self.gaz_callback)
        self.scan_sub = rospy.Subscriber("/scan", LaserScan, self.scan_callback)


       

        
    def nav_callback(self, msg):
        self.navsat_data = msg
        pass

    def imu_callback(self, msg):
        self.imu_data = msg
        
        aux = euler_from_quaternion(quaternion=(msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w))
        
        self.rot_imu.x = aux[0]
        self.rot_imu.y = aux[1]
        self.rot_imu.z = aux[2]

        
        pass

    def mag_callback(self, msg):
        self.mag_data  = msg
        pass

    def gaz_callback(self, msg):
        self.gaz_data  = msg
       
        self.pos_gaz = self.gaz_data.pose.pose.position

        aux_orientation = self.gaz_data.pose.pose.orientation
        aux = euler_from_quaternion(quaternion=(aux_orientation.x, aux_orientation.y, aux_orientation.z, aux_orientation.w))
       
        self.rot_gaz.x = aux[0]
        self.rot_gaz.y = aux[1]
        self.rot_gaz.z = aux[2]
        pass

    
    def scan_callback(self, msg):
        self.scan_data = msg

    # DEBUG (TEMP)
    def RotPrint(self):
        def print_angle(name, array):
         
            n = 5
            print("Angle " + str(name) + ": " + "Yaw: " + str(round(np.degrees(array.z), n)) + " Pitch: " + str(round(np.degrees(array.x), n))  + " Row: " + str(round(np.degrees(array.y), n)))

        while True:
            os.system('clear')
            print_angle("Imu", self.rot_imu)
            print_angle("Gaz", self.rot_gaz)
            print(self.pos_gaz)
            self.rate.sleep()
    
class HectorControl(HectorNav):
    def __init__(self):
        super().__init__()

        self.rate = rospy.Rate(50) 
        # PUBLISHER
        self.land_pub = rospy.Publisher("/land", Empty, queue_size=1)
        self.takeoff_pub = rospy.Publisher("/takeoff", Empty, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)


        

    def land(self):
        for i in range(3):
            self.land_pub.publish(Empty())
            self.rate.sleep()
        pass

    def takeoff(self):
        for i in range(3):
            self.takeoff_pub.publish(Empty())
            self.rate.sleep()

    def move(self, vel):
        self.cmd_vel_pub.publish(vel)
        pass

    def teleop_keyboard(self):
        pass

    def teleop_gamepad(self):
        pass

class HectorTrack(HectorControl):
    def __init__(self):
        super().__init__()
        self.pose_init = Vector2D()
        self.pose_init.x =  self.navsat_data.longitude
        self.pose_init.y =  self.navsat_data.latitude


        self.pose_goal = Vector2D()
        self.pose_current = Vector2D()
        
        self.d_max = 3
        self.d_min = 0.3
        self.SOA = ObstacleAvoid(self.d_min, self.d_max)
        self.dataviwer = DataViwer()
    

    def distance_geo(self, cord1, cord2):
        return gp.distance.geodesic(cord1, cord2, ellipsoid='GRS-80').m
     
    def save_traj(self):
        self.x.append(self.pose_current.x)
        self.y.append(self.pose_current.y)

    def track_go(self):

        # self.takeoff()
        rospy.sleep(3)
        print("Start")
        self.pose_goal.x = -2
        
        self.pose_goal.y = -2
        
        d_tolerance = 0.1

        while True:
            

            # Calculate Distance
            d = ((self.pose_goal.x -  self.pose_current.x)**2 + (self.pose_goal.y -  self.pose_current.y)**2)**(0.5)
            # d = gp.distance.geodesic(self.navsat_data.latitude,self.navsat_data.longitude, ellipsoid='GRS-80').m

           
            self.path_goal(d)
            self.obstacle_avoid()
            self.dataviwer.coleta_data(self.pose_current.x, self.pose_current.y)


            # # EXIT CONDITION
            if (d < d_tolerance):
                v = Twist()
                self.move(v)
                self.dataviwer.parser_csv()
                break
        pass


    def path_goal(self, d):
       
        
        self.pose_current.x = self.pos_gaz.x
        self.pose_current.y = self.pos_gaz.y
        
        
        # Determine Alfa, Beta and Theta
        alfa = self.rot_gaz.z
        beta = np.arctan2((self.pose_goal.y - self.pose_current.y),(self.pose_goal.x -  self.pose_current.x))
        theta = beta - alfa 

        # os.system('clear')
        # print(d)
        # print(theta)
        # print(pose_current.x)
        # print(pose_current.y)

        # SPEED FORCE
        v_mod = 0
        if(d > 1):
            v_mod = 1
        else:
            v_mod = d
        self.forward_kinematics(v_mod, theta)

        
    def forward_kinematics(self, v_mod, theta):

        # Instance Velocity
        v = Twist()
        
        # Decoposition Velocity
        v.linear.x = v_mod*np.cos(theta)
        v.linear.y = v_mod*np.sin(theta)
        v.linear.z = 0
        # print(v.linear.x)
        # Publishers Velocity
        self.move(v)
        self.rate.sleep()

        pass

    def obstacle_avoid(self):       
        # ALGLE POSITION LASER DIRACTION
        # a_i = self.scan_data.angle_increment
        # a_i = 0.00581776862964

        af_array = []
        ar_array = []
        ab_array = []
        al_array = []

        scan_size = len(self.scan_data.ranges)

        # GENERATION INDEX ARRAY OF ANGLE RANGE
        for angle in np.linspace(-44,45,20):
            if(angle < 0):
                temp = 360 + angle
            else:
                temp = angle

            aux_i = radians(temp)*scan_size/(2*np.pi)
            af_array.append(np.round(aux_i,0))
        
        for angle in np.linspace(46,135,20):
            aux_i = radians(angle)*scan_size/(2*np.pi)
            ar_array.append(np.round(aux_i,0))

        for angle in np.linspace(136, 225, 20):
            
            aux_i = radians(angle)*scan_size/(2*np.pi)
            ab_array.append(np.round(aux_i,0))


        for angle in np.linspace(226, 315, 20):
            
            aux_i = radians(angle)*scan_size/(2*np.pi)
            al_array.append(np.round(aux_i,0))



        
        # GET DISTANCE OF REGIONS (FRONT, BACK, LEFT, RIGHT)
        df_array = []
        dr_array = []
        db_array = []
        dl_array = []

        for i in af_array: 
            df_array.append(self.scan_data.ranges[int(i)])
        for i in ar_array: 
            dr_array.append(self.scan_data.ranges[int(i)])
        for i in ab_array: 
            db_array.append(self.scan_data.ranges[int(i)])
        for i in al_array: 
            dl_array.append(self.scan_data.ranges[int(i)])
        
        
        # # TRANSFORM ARRAY AND REMOVE "inf" AND ROUND
        do_array = [df_array, dr_array, db_array, dl_array]
        # for t in do_array:
        #     print(len(t))
        # print("FIM") 

        # do_array = np.array(do_array)
        # print(do_array[2])
        # print("\n\n")
        for j in range(len(do_array)):
            for k in  range(len(do_array[j])):
                if(str(do_array[j][k]) == "inf"):
                    do_array[j][k] = 100
                elif(do_array[j][k] < self.d_min):
                    do_array[j][k] = 100
                    
        
        # # ROUND ARRAY 
        arr = np.round(do_array, 1)
        # print(af_array)
        # print(arr[0])
        # print()

        
        # MIN AND MAX ARR
        min = np.min(arr)
        max = np.max(arr)
        
        # print(min)

        # FIND INDEX MIN VALUE
        index = "inf"
        find_arr = np.argmin(arr, axis=1)
        for row in range(len(arr)):
            aux = arr[row][int(find_arr[row])]
            if(aux == min):
                index = row
        

    
        
        # print(min)
        # print(index)
        # print(arr)
        # os.system("clear")
        
        # theta = 0
        if(str(index) != "inf" and min <= self.d_max and min >= self.d_min):
            # SELECT REGION TO ENABLE FIS OBSTACLE AVOID 
            p = 1
            if(index == 0):
                theta = self.SOA.avoid_front(min)
                # print(theta)
            elif(index == 1):
                theta = self.SOA.avoid_right(min)
                # print("Direita")
            elif(index == 2):
                theta = self.SOA.avoid_back(min)
                # theta = "inf"
                # print("Tras")
            elif(index == 3):
                # print("Esquerda")
                theta = self.SOA.avoid_left(min)
            else:  
                p =  0

            if(p == 1):
                theta = radians(theta)
                self.forward_kinematics(1, theta)
        # else:
        #     # TESTE
        #     self.forward_kinematics(0,0)   
        #     pass
               
                



class Hector(HectorTrack):
    def __init__(self):
        super().__init__()
        pass

rospy.init_node("drone_track")

drone = Hector()
while(True):
    drone.track_go()