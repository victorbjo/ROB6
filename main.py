from dijkstra import shortestRoute
from nodeClass import Node
import RRT
import cv2
import json
config = open("config.json")
config = json.load(config)
map = cv2.imread("maps/lab map.png")
n0 = Node("a",222,80)
n0.heading = -5
n1 = Node("b",340,80)
n2 = Node("c",380,125)
n3 = Node("d",400,160)
n2.addConnection([n1, n3])
n1.addConnection(n0)
route = shortestRoute(n0,n2)
currentTree = []
#for x in range(len(route)-1):
currentTree.append(RRT.RTT(route[0],route[-1],map, config["stepSize"]))
print(currentTree)
cv2.imshow("RRT algorithm from MiR Map - 2.5 meter clearance", map)
cv2.waitKey() 
print(currentTree)

print(currentTree[0][1].route)
with open('route.txt', 'w') as fp:
    for list in currentTree[0]:
        for coordinateSet in list.route:
            fp.write("%s\n" % coordinateSet)