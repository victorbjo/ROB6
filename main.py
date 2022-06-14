from queue import Empty
from dijkstra import shortestRoute
from nodeClass import Node
import RRT
import cv2
import json
import os
config = open("config.json")
config = json.load(config)
def getRoute(start : Node, goal : Node):
    listToReturn = []
    currentNode = goal
    while True:
        listToReturn.append(currentNode)
        if currentNode == start:
            listToReturn.reverse()
            return listToReturn
        currentNode = currentNode.backPointer

#map = cv2.imread("maps/hallwayCleaned.png")

map = cv2.imread("maps/lab map.png")
#Nodes for lab map
n0 = Node("a",244,83)

n1 = Node("b",340,80)
n2 = Node("c",380,125)
n3 = Node("d",400,160)
n2.addConnection([n1, n3])
n1.addConnection(n0)
n0.heading = 0



'''
n0 = Node("a",48,350)
n1 = Node("b",810,225)
n2 = Node("c",810,415)
n3 = Node("e",350,35)
n3.heading = 180
n1.addConnection([n0, n2])
n3.addConnection(n2)
'''
#Nodes for two corners
'''
map = cv2.imread("maps/twoCorners.png")
n0 = Node("a",220,60)
n1 = Node("b",220,170)
n2 = Node("c",60,196)
n3 = Node("e",50,380)
n1.addConnection([n0, n2])
n3.addConnection(n2)
n3.heading = 270
'''
print(len(map))
route = shortestRoute(n0,n3)
print(route)
currentTree = []
#for x in range(len(route)-1):
currentTree.append(RRT.RTT(route[0],route[-1],map, config["stepSize"]))
    #print("SHAPE", currentTree[-1][-1].heading)
    #route[x+1].heading = currentTree[-1][-1].heading
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
print(currentTree[0][-1].backPointer)
currentTree : list[Node] = getRoute(currentTree[0][0], currentTree[0][-1])
print(currentTree)
print("FUCK")
try:
    os.remove("route.txt")
except:
    pass
with open('route.txt', 'w') as fp:
    for list in currentTree:
        if list.route == Empty:
            continue
        for number in list.route:
            fp.write("%s\n" % number)
