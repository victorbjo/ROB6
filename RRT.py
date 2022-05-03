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
def checkLine(imgNew, imgOld):
    for idx, row in enumerate(imgNew):
        for idy, pixel in enumerate(row):
            if (pixel[0] == 255):
                if (imgOld[idx][idy][0] == 205 or imgOld[idx][idy][0] == 0):
                    return False
    return True
def makeLine(imgOld, x0, y0, x1, y1):
    color = (255, 0, 0)
    newImage = imgOld.copy()
    cv2.line(newImage, (x0,y0),(x1,y1), color, 5)
    if checkLine(newImage, imgOld):
        cv2.line(imgOld, (x0,y0),(x1,y1), color, 2)
        return True
    return False

def getRPoint(img):
    shape = img.shape
    randomX = random.randint(0, shape[0])
    randomY = random.randint(0, shape[1])
    return(randomX, randomY)

def getAngle(node, point, stepSize):
    try:
        p =  geo.Point(node.pos[0], node.pos[1])
        tempLine = geo.LineString([geo.Point(point[0], point[1]),p])
        circle = p.buffer(stepSize)
        intersection = circle.intersection(tempLine)
        x,y = intersection.coords.xy
        return(x[0],y[0])
    except:
        return (point)

def nearestNode(nodes, point):
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
    while i  < 100:
        newCoords = getRPoint(img)
        _nearestNode = nearestNode(nodes, newCoords)
        x, y = getAngle(_nearestNode, newCoords, stepSize)
        nodes.append(Node("N/A", int(x), int(y)))
        i = i + 1
        if not makeLine(img, _nearestNode.pos[0], _nearestNode.pos[1], nodes[-1].pos[0], nodes[-1].pos[1]):
            nodes.pop(-1)
            i = i - 1
        else:
            print(i)

img = cv2.imread("mymap0.pgm")
imgOrig = cv2.imread("mymap0.pgm")
startNode = Node("start", 60, 70)
goal = Node("goal", 134, 316)
RTT(startNode,goal,img, 15)
getRPoint(img)
cv2.imshow("RRT algorithm from MiR Map - 2.5 meter clearance", img)
cv2.waitKey() 
