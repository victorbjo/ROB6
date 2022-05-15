import random
import math
import matplotlib.pyplot as plt
import cv2
from nodeClass import Node
from shapely import geometry as geo
def mesaureDist(node0 : Node, node1 : Node): # Measure the distance between two nodes using pythagoras theorem
    a = node1.pos[0]-node0.pos[0]
    a = a * a
    b = node1.pos[1]-node0.pos[1]
    b = b * b
    return abs(math.sqrt(a+b).real)
def checkLine(imgNew, imgOld): # Check if the line on the current map is placed on a grey/dark pixel on the old map
    for idx, row in enumerate(imgNew):
        for idy, pixel in enumerate(row):
            if (pixel[0] == 255):
                if (imgOld[idx][idy][0] == 205 or imgOld[idx][idy][0] == 0):
                    return False
    return True
def makeLine(imgOld, x0, y0, x1, y1): # Creates line between two different sets of (x,y) coordinates on the new map
    color = (255, 0, 0)
    newImage = imgOld.copy()
    cv2.line(newImage, (x0,y0),(x1,y1), color, 5)
    if checkLine(newImage, imgOld):
        cv2.line(imgOld, (x0,y0),(x1,y1), color, 2)
        return True
    return False

def getRPoint(img): #Takes the .shape of the img to get all the width and height values in an array, and then finds random x and y point 
    shape = img.shape
    randomX = random.randint(0, shape[0])
    randomY = random.randint(0, shape[1])
    return(randomX, randomY)

# Stepsize is the length between the start and end of a line

def createLineToNewPoint(node, point, stepSize): # takes the random generated x,y point (node) and current x,y point (point) and creates a temporary line between.
    try:                                         # a circle (radius of stepSize) is created and the coordinate for its intersection with the tempLine is found. 
        p =  geo.Point(node.pos[0], node.pos[1]) # A permanent line is created between the current point and the intersection point.
        tempLine = geo.LineString([geo.Point(point[0], point[1]),p])
        circle = p.buffer(stepSize)
        intersection = circle.intersection(tempLine)
        x,y = intersection.coords.xy
        return(x[0],y[0])
    except:
        return (point)

def nearestNode(nodes, point): # Iterates through each node generated and measure distance to them from the current node, save all distances in list and find node minimum distance
    distList = []
    tempNode = Node("Temp", point[0], point[1])
    for node in nodes:
        tempDist = mesaureDist(node, tempNode)
        distList.append(tempDist)
    tempNode = min(distList)
    distList.index(tempNode)
    return(nodes[distList.index(tempNode)])

def RTT(node, goal, img, stepSize = 30):
    nodes = [node]
    i = 0
    while i  < 500:
        newCoords = getRPoint(img) # Stores coordinates in newCoords from the new generated point(using getRPoint on the map)
        _nearestNode = nearestNode(nodes, newCoords) # Measures distance too all generated nodes, takes the shortest distance and stores in _nearestnode variable
        x, y = createLineToNewPoint(_nearestNode, newCoords, stepSize) #generates a line to the new point and saves the new points coordinates as x, y
        nodes.append(Node("N/A", int(x), int(y))) #appends new coordinates as a new/next node in the nodes list
        i = i + 1
        if not makeLine(img, _nearestNode.pos[0], _nearestNode.pos[1], nodes[-1].pos[0], nodes[-1].pos[1]): # If the line is false it will reset by not drawing the line and decrementing i 
            nodes.pop(-1)                                                                                   # as the increment happens no matter what
            i = i - 1
        else:
            print(i)
            cv2.imwrite("images/RRT"+str(i)+".png", img)           
        if (mesaureDist(nodes[-1], goal) < stepSize): # If a node is within the stepSize distance of the goal node, a line will be created between the two nodes
            if makeLine(img, goal.pos[0], goal.pos[1], nodes[-1].pos[0], nodes[-1].pos[1]):
                print("Reached goal!!!")
                return nodes


img = cv2.imread("maps/mymap0.pgm")
imgOrig = cv2.imread("maps/mymap0.pgm")

startNode = Node("start", 60, 70)
goal = Node("goal", 134, 3160)
RTT(startNode,goal,img, 15)
getRPoint(img)
cv2.imshow("RRT algorithm from MiR Map - 2.5 meter clearance", img)
cv2.waitKey() 
