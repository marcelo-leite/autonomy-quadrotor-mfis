#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty


class Action:
    def __init__(self):
        self.rate = rospy.Rate(1)


        self.empty_msg = Empty()
        self.twist_msg = Twist()
        
        # SUBSCRIBER
        self.takeoff_sub = rospy.Subscriber('/takeoff', Empty, self.takeoff_callback)
        self.land_sub = rospy.Subscriber('/land', Empty, self.land_callback)

        # PUBLISHER
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
    def takeoff_callback(self, msg): 
        self.twist_msg.linear.z = 0.4
        i = 0
        while i < 3:
            self.cmd_vel_pub.publish(self.twist_msg)
            i = i + 1
            self.rate.sleep()
        
        self.twist_msg.linear.z = 0
        self.cmd_vel_pub.publish(self.twist_msg)


    def land_callback(self, msg): 
        self.twist_msg.linear.z = -0.5
        i = 0
        while i < 10:
            self.cmd_vel_pub.publish(self.twist_msg)
            i = i + 1
            self.rate.sleep()
        
        self.twist_msg.linear.z = 0
        self.cmd_vel_pub.publish(self.twist_msg)

rospy.init_node("hector_quadrotor_actions")
action = Action()
action.takeoff()
# takeoff = rospy.Publisher('/takeoff', Empty, queue_size=1)
# takeoff.publish()

rospy.spin()