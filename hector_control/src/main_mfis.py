
import numpy as np
import geopy as gp
import os
import csv
import rospy

from math import radians
from sensor_msgs.msg import Joy
from sensor_msgs.msg import NavSatFix, Imu, LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Vector3Stamped, Point
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Empty, String
from tf.transformations import euler_from_quaternion, quaternion_from_euler

from system.obstacle_avoid_mfis import ObstacleAvoid



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
        self.s = []
        self.z = []
        self.t = []
        self.beta = []
        self.alfa = []
        pass

    def coleta_data(self, x, y, s, t, alfa, beta):
        self.x.append(x)
        self.y.append(y)
        self.s.append(s)
        self.t.append(t)
        self.alfa.append(alfa)
        self.beta.append(beta)
        pass
    def reset_data(self):
        self.x = []
        self.y = []
        self.s = []
        self.t = []
        self.alfa = []
        self.beta = []
        
    def parser_csv(self, xg, yg, n, fa, fr):
        print(self.t[-1] - self.t[0])
        file_name = "datapose-s" + str(n) + "-" + str(round(xg)) + "-" + str(round(yg)) + "-fa" + str(fa) + "-fr" +str(fr) + ".csv"
        with open(file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["x", "y", "s", "t", "alfa", "beta"])
            for i in range(len(self.x)):
                writer.writerow([self.x[i], self.y[i], self.s[i], self.t[i], self.alfa[i], self.beta[i]])
        pass

class HectorNav:
    def __init__(self):

        # BRUTE DATAS
        self.rate = rospy.Rate(100) 
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

        # self.rate = rospy.Rate(50) 
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
        self.rate.sleep()
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


        self.pose_goal = Vector3D()
        self.pose_current = Vector3D()
    
        # self.d_max = 1.2
        self.d_max = 1.4
        self.d_min = 0.4

        # Virtual Force - Atractive and Repulsive - Fa [0,1] - Fr[0,1]
        # Default Value*
        # self.Fa = 0.5
        # self.Fr = 0.6
        
        # Test Value
        # .25 0.5 0.75 1.0
        self.Fa = 0.5
        self.Fr = 0.5

        # State Colision
        self.isColision = False
        
        # Test - Record V Lienar
        self.vlx = 0
        self.vly = 0

        self.SOA = ObstacleAvoid(self.d_min, self.d_max)
        self.dataviwer = DataViwer()
    

    def distance_geo(self, cord1, cord2):
        return gp.distance.geodesic(cord1, cord2, ellipsoid='GRS-80').m
     
    def save_traj(self):
        self.x.append(self.pose_current.x)
        self.y.append(self.pose_current.y)

    def track_go(self,xg, yg):
        sn = 3
        # self.takeoff()
        rospy.sleep(3)
        print(f"START DESTINO (xg, yg) = ({xg}, {yg})")
        # self.pose_goal.x = float(input("Digite x_goal: "))
        # self.pose_goal.y =  float(input("Digite y_goal: "))
        self.pose_goal.x = xg
        self.pose_goal.y = yg
        self.pose_current.x = self.pos_gaz.x
        self.pose_current.y = self.pos_gaz.y
        self.pose_current.z = self.pos_gaz.z

        self.ti = rospy.get_time()

            
        d_tolerance = 0.1
        
        while True:
            

            # Calculate Distance
            d = ((self.pose_goal.x -  self.pose_current.x)**2 + (self.pose_goal.y -  self.pose_current.y)**2)**(0.5)
            # d = gp.distance.geodesic(self.navsat_data.latitude,self.navsat_data.longitude, ellipsoid='GRS-80').m
            # print(d)

            self.path_goal(d)
            
            # self.dataviwer.coleta_data(self.pose_current.x, self.pose_current.y, 0, )


            # # EXIT CONDITION
            if (d < d_tolerance):
                v = Twist()
                self.move(v)
                print("STOP - CHEGOU\n\n")
                self.dataviwer.parser_csv(self.pose_goal.x, self.pose_goal.y, sn,  self.Fa, self.Fr)
                # self.dataviwer.reset_data()
                sn += 1
                break
            if(self.isColision):
                print("STOP - COLEDIU\n\n")
                self.dataviwer.parser_csv(self.pose_goal.x, self.pose_goal.y, sn, self.Fa, self.Fr)
                break
                
        pass


    def path_goal(self, d):
       
        
        self.pose_current.x = self.pos_gaz.x
        self.pose_current.y = self.pos_gaz.y
        
        
        # Determine Alfa, Beta and Theta
        alfa = self.rot_gaz.z
        beta = np.arctan2((self.pose_goal.y - self.pose_current.y),(self.pose_goal.x -  self.pose_current.x))
        theta = beta - alfa 

        self.control_yaw(theta)  
           
        self.pose_current.x = self.pos_gaz.x
        self.pose_current.y = self.pos_gaz.y
        
        # Determine Alfa, Beta and Theta
        alfa = self.rot_gaz.z
        beta = np.arctan2((self.pose_goal.y - self.pose_current.y),(self.pose_goal.x -  self.pose_current.x))
        theta = beta - alfa

        # print(rospy.get_time())
        if(1):
            # SPEED FORCE
            v_mod = 0
            if(d > self.Fa):
                v_mod = self.Fa
            else:
                v_mod = d

            active = self.obstacle_avoid(np.rad2deg(theta))
            if(active):
                self.dataviwer.coleta_data(self.pose_current.x, self.pose_current.y, 1, rospy.get_time(), alfa, beta)
                pass
            else:
                self.forward_kinematics(v_mod, theta, 0)
                self.dataviwer.coleta_data(self.pose_current.x, self.pose_current.y, 0, rospy.get_time(), alfa, beta)
                pass

    def control_yaw(self, err):
        v = Twist()
        # v.angular.z = err*(2)
        v.angular.z = err*(2)
        v.linear.x = self.vlx
        v.linear.y = self.vly
        if(np.abs(v.angular.z) < 1):
            self.move(v)
        else:
            v.angular.z = np.sign(v.angular.z)*1
            self.move(v)
        # print(np.rad2deg(err))
        # print(np.rad2deg(alfa))
       
    def control_rotate_test(self, setpoint):
        rospy.sleep(3)
        print(f"START ROTATE TEST")
        self.ti = rospy.get_time()

        while(rospy.get_time() - self.ti < 20):
            self.pose_current.x = self.pos_gaz.x
            self.pose_current.y = self.pos_gaz.y
            self.pose_current.z = self.pos_gaz.z
            
            # Determine Alfa, Beta and Theta
            alfa = self.rot_gaz.z
            beta = np.deg2rad(setpoint)
            theta = beta - alfa 

            self.dataviwer.coleta_data(self.pose_current.x, self.pose_current.y, 1, rospy.get_time(), alfa, beta)
            self.control_yaw(theta)  
            # print(rospy.get_time())
        
        print("STOP - ORIENTAÇAO CORRIGIDA\n\n")
        self.dataviwer.parser_csv(0, 0, setpoint, self.Fa, self.Fr)
        
        pass

    def forward_kinematics(self, v_mod, theta, state):
        
        # Instance Velocity
        v = Twist()
        
        # Decoposition Velocity
        v.linear.x = v_mod*np.cos(theta)
        v.linear.y = v_mod*np.sin(theta)
        v.linear.z = 0
        # print(v.linear.x)
        # Publishers Velocity
        self.move(v)
        
        
        # Test 
        self.vlx = v.linear.x
        self.vly = v.linear.y
        
        # self.dataviwer.coleta_data(self.pos_gaz.x, self.pos_gaz.y, s)

        pass
        
    def obstacle_avoid(self, yaw):       
        # ALGLE POSITION LASER DIRACTION
        # a_i = self.scan_data.angle_increment
        # a_i = 0.00581776862964
        # self.dataviwer.coleta_data(self.pose_current.x, self.pose_current.y, 1)
        
        af_array = []
        ar_array = []
        ab_array = []
        al_array = []

        scan_size = len(self.scan_data.ranges)

        # GENERATION INDEX ARRAY OF ANGLE RANGE
        for angle in np.linspace(-44,45,20):
        # for angle in np.linspace(-70,70,20):
            if(angle < 0):
                temp = 360 + angle
            else:
                temp = angle

            aux_i = radians(temp)*scan_size/(2*np.pi)
            af_array.append(np.round(aux_i,0))
        
        for angle in np.linspace(46,135,20):
        # for angle in np.linspace(70,110,20):
            aux_i = radians(angle)*scan_size/(2*np.pi)
            ar_array.append(np.round(aux_i,0))

        for angle in np.linspace(136, 225, 20):
        # for angle in np.linspace(111, 250, 20):
            
            aux_i = radians(angle)*scan_size/(2*np.pi)
            ab_array.append(np.round(aux_i,0))

        for angle in np.linspace(226, 315, 20):
        # for angle in np.linspace(250, 290, 20):
            
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
    
    
        for j in range(len(do_array)):
            for k in  range(len(do_array[j])):
                if(str(do_array[j][k]) == "inf"):
                    do_array[j][k] = 100
                # elif(do_array[j][k] < self.d_min ):
                elif(do_array[j][k] < 0.2 ):
                    do_array[j][k] = 100
                    
        
        # # ROUND ARRAY 08539
        arr = np.round(do_array, 2)
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
        

        
        # min = np.round(min, )
        # print([min])
        # print(min)

        if(str(index) != "inf" and min <= self.d_max and min >= self.d_min):
            # SELECT REGION TO ENABLE FIS OBSTACLE AVOID 
            p = 1
            # print(min)
            yaw = int(yaw)
            # print(x)
            if(yaw > 180 or yaw < -180):
                if(yaw < -180):
                    yaw = yaw + 360
                if(yaw > 180):
                    yaw = yaw - 360
                
            if(index == 0):
                theta = self.SOA.avoid_front(min, yaw)
            elif(index == 1):
                theta = self.SOA.avoid_right(min, yaw)
            elif(index == 2):
                theta = self.SOA.avoid_back(min, yaw)
            elif(index == 3):
                theta = self.SOA.avoid_left(min, yaw)
            else:  
                p =  0
                self.forward_kinematics(0, theta)
            if(p == 1):
                theta = radians(theta)
                self.forward_kinematics(self.Fr, theta, 0)
                return True
        elif(min < self.d_min):
            self.isColision = True
        else:
            return False  
                



class Hector(HectorTrack):
    def __init__(self):
        super().__init__()
        pass

rospy.init_node("drone_track")

drone = Hector()

# CONTROL ROTATE TEST
# drone.control_rotate_test(10)


# PATH PLANNING TRACK
xo, yo = 21, 18
drone.track_go(xo, yo)

# while(True):
#     xo, yo = 20, 0
#     drone.track_go(xo, yo)
#     xo, yo = 0, 18
#     drone.track_go(xo, yo)
# o = 1
# while(True):
    # if(o == 1):
    #     a = np.random.randint(90)
    #     a = np.deg2rad(a)

    #     M = np.sqrt(25**2 + 25*2)
    #     p = round(M*np.cos(a)), round(M*np.sin(a))
    #     print(f'Destino {p}')
        
    #     xg = p[0]
    #     yg = p[1]
    #     o = 0
    # else: 
    #     print(f'Destino (0, 0)')
    #     o = 1
    #     xg = 0
    #     yg = 0

    




