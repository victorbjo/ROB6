from dijkstra import shortestRoute
from nodeClass import Node
import RRT
import cv2
import json
import os
config = open("config.json")
config = json.load(config)
map = cv2.imread("maps/hallwayCleaned.png")
'''
map = cv2.imread("maps/lab map.png")
Nodes for lab map
n0 = Node("a",222,80)
n0.heading = 0
n1 = Node("b",340,80)
n2 = Node("c",380,125)
n3 = Node("d",400,160)
n2.addConnection([n1, n3])
n1.addConnection(n0)
'''
n0 = Node("a",805,105)
n1 = Node("b",810,225)
n2 = Node("c",810,415)
n3 = Node("e",650,422)
n0.heading = 90
n1.addConnection([n0, n2])
n3.addConnection(n2)
route = shortestRoute(n0,n1)
print(route)
currentTree = []
#for x in range(len(route)-1):
currentTree.append(RRT.RTT(route[0],route[-1],map, config["stepSize"]))
'''
for x in range(len(route)-1):
    currentTree.append(RRT.RTT(route[x],route[x+1],map, config["stepSize"]))
'''
print(currentTree)
cv2.imshow("RRT algorithm from MiR Map - 2.5 meter clearance", map)
cv2.waitKey() 
print(currentTree)
#route = shortestRoute(currentTree[0],currentTree[-1])
print(currentTree[0][1].route)
try:
    os.remove("route.txt")
except:
    pass
with open('route.txt', 'w') as fp:
    for list in currentTree[0]:
        for coordinateSet in list.route:
            fp.write("%s\n" % coordinateSet)
