from dijkstra import shortestRoute
from nodeClass import Node
import RRT
import cv2
map = cv2.imread("maps/cleanedMap.png")
n0 = Node("a",80,80)
n0.heading = 90
n1 = Node("b",75,250)
n2 = Node("c",140,330)
n3 = Node("d",280,300)
n4 = Node("e",280,360)
n0.addConnection(n1)
n1.addConnection(n2)
n2.addConnection([n3, n4])
n3.addConnection(n4)
route = shortestRoute(n0,n3)
currentTree = RRT.RTT(route[0],route[1],map, 15)
cv2.imshow("RRT algorithm from MiR Map - 2.5 meter clearance", map)
cv2.waitKey() 
print(currentTree)
print(currentTree[-1].connectedNodes)