from dijkstra import shortestRoute
from nodeClass import Node
import RRT
import cv2
import json
config = open("config.json")
config = json.load(config)
map = cv2.imread("maps/hallwayCleaned.png")
n0 = Node("a",805,100)
n0.heading = 90
n01 = Node("q", 805, 300)
n1 = Node("b",805,415)
n01.heading = 90
n2 = Node("c",700,422)
n3 = Node("d",815,555)
n1.addConnection(n01)
n1.addConnection([n01, n2, n3])
route = shortestRoute(n01,n2)
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