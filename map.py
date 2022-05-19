from ctypes.wintypes import MSG
from re import sub
from turtle import delay
import rospy
from geometry_msgs.msg import PoseStamped
import matplotlib.pyplot as plt
from matplotlib import image

#img = image.imread("/home/jimmi/catkin_ws/src/mir_robot/ROB6/Lab1.png")

#print(img)

#plt.plot(img,"aa")
#plt.show()

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
rospy.init_node("move")


#! /usr/bin/env python3
 
# This program converts Euler angles to a quaternion.
# Author: AutomaticAddison.com
 
import numpy as np # Scientific computing library for Python
 
def get_quaternion_from_euler(roll, pitch, yaw):
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
    return [qx, qy, qz, qw]


def goTo(x,y, z_rot):

    quaterions = get_quaternion_from_euler(0,0, z_rot)

    goal = PoseStamped()
    goal.header.seq = 0
    goal.header.stamp = rospy.Time.now()
    goal.header.frame_id = "map"



    goal.pose.position.x = x
    goal.pose.position.y = y
    goal.pose.position.z = 0

    goal.pose.orientation.x = quaterions[0]
    goal.pose.orientation.y = quaterions[1]
    goal.pose.orientation.z = quaterions[2]
    goal.pose.orientation.w = quaterions[3]
    
    delay(2)

    pub.publish(goal)


a = (810*0.05, (636-150)*0.05)

b = (210*0.05, (636-412)*0.05)
c = (145*0.05, (636-308)*0.05)
d = (153*0.05, (636-261)*0.05)



goTo(810*0.05, (636-150)*0.05, 1.57*3)

rospy.spin()


