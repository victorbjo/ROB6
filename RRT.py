import random
import math
import matplotlib.pyplot as plt
import cv2
from nodeClass import Node
from shapely import geometry as geo
import solve
import json
config = open("config.json")
config = json.load(config)
def findAngle(x0, y0, x1, y1):
    delta_x = x1 - x0
    delta_y = y1 - y0
    theta_radians = math.atan2(delta_y, delta_x)
    return math.degrees(theta_radians)
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
def makeLine(imgOld,node0 : Node, node1 : Node): # Creates line between two different sets of (x,y) coordinates on the new map
    x0 = node0.pos[0]
    y0 = node0.pos[1]
    x1 = node1.pos[0]
    y1 = node1.pos[1]
    color = (255, 0, 0)
    newImage = imgOld.copy()#Creates new image to draw on. This is done in case the changes need to be reverted, the old image can still be used..
    tempAngle = [findAngle(x0, y0, x1, y1)] #Finds angle between old node and new node, compared to x axis
    if tempAngle[0] < 0:
        tempAngle[0] = tempAngle[0] + 360#This is done to make sure that anything above 180 is actually something like 190 and not -170
    tempAngle.append(tempAngle[0]+45) #Finds two new angles, this one +45 deg of orig angle
    tempAngle.append(tempAngle[0]-45) #This one -45 of orig angle
    #print(node1.id)
    #print(tempAngle)
    cv2.line(newImage, (x0,y0),(x1,y1), color, 2)
    for x in range(3):
        node1.heading = tempAngle[x]
        try:
            status =  solve.drawPath(newImage, node0, node1)
            if status is not False:
                if checkLine(status, imgOld):
                    #print("Works")
                    #cv2.imshow("SOm", status)
                    #cv2.waitKey()
                    #imgOld = status.copy()
                    cv2.line(imgOld, (x0,y0),(x1,y1), color, 2)
                    return True
        except:
            pass
    return False
    if checkLine(newImage, imgOld):
        cv2.line(imgOld, (x0,y0),(x1,y1), color, 2)
        return True
    return False

def getRPoint(img): #Takes the .shape of the img to get all the width and height values in an array, and then finds random x and y point 
    shape = img.shape
    valid = False
    while valid is False:
        randomX = random.randint(0, shape[0])
        randomY = random.randint(0, shape[1])
        if img[abs(randomX-1)][abs(randomY-1)][0] > 250:
            break
    return(randomY, abs(randomX))

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
    nodes : list[Node] = [node]
    i = 0
    triesCounter = 0
    while i  < 500:
        newCoords = getRPoint(img) # Stores coordinates in newCoords from the new generated point(using getRPoint on the map)
        _nearestNode = nearestNode(nodes, newCoords) # Measures distance too all generated nodes, takes the shortest distance and stores in _nearestnode variable
        x, y = createLineToNewPoint(_nearestNode, newCoords, stepSize) #generates a line to the new point and saves the new points coordinates as x, y
        nodes.append(Node(i, int(x), int(y))) #appends new coordinates as a new/next node in the nodes list
        i = i + 1
        if not makeLine(img, _nearestNode, nodes[-1]): # If the line is false it will reset by not drawing the line and decrementing i 
            nodes.pop(-1)                                                                                   # as the increment happens no matter what
            i = i - 1
            _nearestNode.failedConnections += 1
            if _nearestNode.failedConnections > 20 and _nearestNode.hasChild == False and _nearestNode.backPointer != [] :
                _nearestNode.backPointer.hasChild = False
                nodes.remove(_nearestNode)
        else:
            #print(i)
            triesCounter = 0
            print(newCoords)
            print(img[abs(newCoords[1]-1)][abs(newCoords[0]-1)][0])
            nodes[-1].backPointer = _nearestNode
            _nearestNode.hasChild = True
            #cv2.imwrite("images/RRT"+str(i)+".png", img)      
            nodes[-1].addConnection(nodes[-2])
        if nodes[-1].failedConnections > 20: #config["amountOfTries"]:
            for i in range(2):
                if (nodes[-1] != nodes[0]):
                    nodes[-1].backPointer.hasChild = False
                    nodes.pop()
        '''
                    nodesToDelete = []
            for i in range(len(nodes)):
                if (nodes[i] != nodes[0] and nodes[i].hasChild == False and nodes[i].failedConnections > config["amountOfTries"]):
                    nodes[i].backPointer.hasChild = False
                    nodes.pop(i) 
                    ''' 
        if (mesaureDist(nodes[-1], goal) < config["goalRadius"]): # If a node is within the stepSize distance of the goal node, a line will be created between the two nodes
            if makeLine(img, nodes[-1], goal):
                print("Reached goal!!!")
            nodes.append(Node("Goal", goal.pos[0], goal.pos[1]))
            nodes[-1].addConnection(nodes[-2])
            nodes[-1].backPointer = nodes[-2]
            return nodes 


if __name__ == "__main__":
    #print(findAngle(1,1,0,2))
    img = cv2.imread("maps/lab map.png")
    imgOrig = cv2.imread("maps/lab map.png")
    startNode = Node("start", 222,80)
    goal = Node("goal", 400,160)
    RTT(startNode, goal, img, config["stepSize"])
    #getRPoint(img)
    cv2.imshow("RRT algorithm from MiR Map - 2.5 meter clearance", img)
    cv2.waitKey() 
