from ctypes.wintypes import MSG
from re import sub
from turtle import delay
import rospy
from geometry_msgs.msg import PoseStamped
import matplotlib.pyplot as plt
from matplotlib import image

img = image.imread("/home/jimmi/catkin_ws/src/mir_robot/ROB6/Lab1.png")

print(img)

plt.plot(img,"aa")
plt.show()

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
rospy.init_node("move")

def goTo(x,y, x_rot,y_rot,z_rot,w_rot):
    goal = PoseStamped()
    goal.header.seq = 0
    goal.header.stamp = rospy.Time.now()
    goal.header.frame_id = "map"



    goal.pose.position.x = x
    goal.pose.position.y = y
    goal.pose.position.z = 0

    goal.pose.orientation.x = x_rot
    goal.pose.orientation.y = y_rot
    goal.pose.orientation.z = z_rot
    goal.pose.orientation.w = w_rot
    
    delay(2)

    pub.publish(goal)


a = (108*0.05, (636-238)*0.05)
b = (210*0.05, (636-412)*0.05)
c = (145*0.05, (636-308)*0.05)
d = (153*0.05, (636-261)*0.05)

#goTo(5.140, 19.728, 0.0,
#     0.0, 0.0, -0.475, 0.880)

#rospy.spin()


