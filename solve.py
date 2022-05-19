from sympy.solvers import solve
from sympy import *
from cmath import cos, sin
from math import radians, degrees
import math
from nodeClass import Node
from loadParams import *
import drawTools
import time as tm
x = Symbol('x')
import cv2
def norm(a, b):
    return simplify(sqrt((a**2) + (b**2)))
def trajectoryGen(tf, startX, startY, goalX, goalY, startAngle, goalAngle, startAngleBed):
    x_r_0 = [startX,startY]
    x_r_t = [goalX,goalY]
    v_0 = startAngle
    v_t = goalAngle
    #print(startAngle, " ", startAngleBed)
    #print("ANGLES")
    h_r_0 = [cos(radians(startAngleBed)).real, sin(radians(startAngleBed)).real]
    h_r_t = [cos(radians(v_t)).real, sin(radians(v_t)).real]

    d = x_r_0[0]
    c = h_r_0[0]
    b = (3/(tf**2))*((x_r_t[0]) - d) - 1/tf * (2*h_r_0[0]+h_r_t[0])
    a = -2/(tf**3)*((x_r_t[0])- d) + 1/(tf**2) * (h_r_0[0]+h_r_t[0])
    d1 = x_r_0[1]
    c1 = h_r_0[1]
    b1 = (3/(tf**2))*((x_r_t[1])- d1) - 1/tf * (2*h_r_0[1]+h_r_t[1])
    a1 = -2/(tf**3)*((x_r_t[1])- d1) + 1/(tf**2) * (h_r_0[1]+h_r_t[1])


    t = Symbol('t')
    xRobot = x = Matrix([a*t**3 + b*t**2 + c*t +d, a1*t**3 + b1*t**2 + c1*t +d1])

    args = Matrix([t])
    dx = x.jacobian(args)#Calculates jacobian
    #print(dx)
    ws = norm(dx[0], dx[1])
    heading = dx/ws
    #ws.subs(t, 10)
    #print(ws.subs(t, 1))
    #print(ws)
    time = [0.05, tf]
    #Constants

    L = 1.5 #Needs to be fixed, not hard programmed
    x_r_0Matrix = Matrix([x_r_0[0],x_r_0[1]])
    h_r_0Matrix = Matrix([h_r_0[0],h_r_0[1]])

    x_b_0 = [x_r_0Matrix - L * h_r_0Matrix]
    h_b_0 = [h_r_0Matrix]


    x_r = []
    y_r = []

    for x in range(int(time[1]/time[0])+1):
        T = x*time[0]
        x_r.append((a*T**3 + b*T**2 + c*T + d).real)
        y_r.append((a1*T**3 + b1*T**2 + c1*T + d1).real)
    length = []
    for x in range(int(time[1]/time[0])+1):
        #x_b_0[-1] = Matrix([1.1955, -0.3726])
        #h_b_0[-1] = Matrix([0.3199, 0.9475])
        T = x * time[0] #Time step of 0.05
        omegaS = ws.subs(t, T)
        dx_1 = dx.subs(t, T)
        #print(dx_1)
        dotProd = h_b_0[x].dot(dx_1/norm(dx_1[0],dx_1[1]))
        dotProdH = dx_1.dot(h_b_0[x])
        #print(dotProdH)
        #print("DotProd")
        #print(h_b_0[x] * omegaS * dotProd)
        dot_x_b = h_b_0[x] * omegaS * dotProd
        
        #print(dotProd)
        #print(dot_x_b)
        dot_h_b = (dx_1 - h_b_0[x] * dotProdH) / L
        x_b_0.append(x_b_0[x] + (time[0] * dot_x_b))
        h_b_0.append(h_b_0[x] + time[0] * dot_h_b)
        h_b_0[-1] = (h_b_0[x+1] / norm(h_b_0[x+1][0], h_b_0[x+1][1]))
        #print(x_r_0[x])
        length.append(sqrt((x_b_0[x][0]-x_r[x])**2+(x_b_0[x][1]-y_r[x])**2))
    
    #print(x_b_0)
    #print(length)
    return x_b_0, h_b_0, xRobot, heading
    #print(x_b_0)
    print(length)
def findAngle(x0, y0, x1, y1):
    delta_x = x1 - x0
    delta_y = y1 - y0
    theta_radians = math.atan2(delta_y, delta_x)
    return math.degrees(theta_radians)


image = cv2.imread('blank.png')
compound = False
compund = True
def drawPath(img, node0 : Node, node1 : Node):
    config = open("config.json")
    config = json.load(config)
    x0 = node0.pos[0]/20
    y0 = node0.pos[1]/20
    x1 = node1.pos[0]/20
    y1 = node1.pos[1]/20
    h0 = node0.heading
    h1 = node1.heading
    angle = findAngle(x0,y0,x1,y1)
    if angle < 0:
        angle+=360
    if h0 > angle + config["maxAngleDelta"] or h0 < angle - config["maxAngleDelta"]:
        return False
    #print(x0, y0, x1, y1, h0, h1)
    #print(angle)
    h0Bed = node0.headingBed
    if h0Bed is None:
        h0Bed = h1
    xBed, hBed, xRobot, hRobot = trajectoryGen(2, x0, y0, x1, y1, h0, h1, h0Bed)
    nimg = img.copy()
    for x in range (len(xBed)-1):
        #nimg = img.copy()
        time = 0.05*x
        bedX = (round(xBed[x][0],2))
        bedY = (round(xBed[x][1],2))
        bedH = degrees(acos(hBed[x][0]))
        robotX = xRobot[0].subs("t", time)
        robotY = xRobot[1].subs("t", time)
        bedY1 = (round(xBed[x+1][1],2))
        robotH = degrees(acos(hRobot[0].subs("t",time)))
        if bedY > robotY :
            #pass
            bedH = -bedH
            robotH = -robotH
        if config["drawBed"] == 1:
            drawTools.drawRect(nimg, bed, bedH, bedX*20, bedY*20)
        if config["drawRobot"] == 1:
            drawTools.drawRect(nimg, robot, robotH, robotX*20, robotY*20)
        node1.route.append([robotX, robotY, robotH])
        cv2.imwrite("images/trailer/"+str(x)+".png", image)
    node1.headingBed = bedH
    #print("BedHead; RobHead " + str(node1.headingBed)+" " + str(node1.heading))
    #print(node1)
    #print("Nodecheck")
    if config["showSteps"] == 1:
        cv2.imshow('image', nimg)
        cv2.waitKey(config["msPerFig"])
        cv2.imwrite("images/"+str(int(tm.time()))+".png", nimg)
    return nimg
if __name__ == "__main__":
    print("Main")
    angle = findAngle(4.65, 6.65, 5.35, 6.55)#When making function make sure that all inputs above 180 be plussed with 360
    if angle < 0:
        angle+=360
    print(angle)
    xBed, hBed, xRobot, hRobot = trajectoryGen(2, 4.65, 6.65, 5.35, 6.75, 286.6992442339936, 306.86989764584405)
    
    for x in range (len(xBed)-1):
        time = 0.05*x
        if (compound):
            image = cv2.imread('blank.png')
        bedX = (round(xBed[x][0],2))
        bedY = (round(xBed[x][1],2))
        bedH = degrees(acos(hBed[x][0]))
        robotX = xRobot[0].subs("t", time)
        robotY = xRobot[1].subs("t", time)
        bedY1 = (round(xBed[x+1][1],2))
        robotH = degrees(acos(hRobot[0].subs("t",time)))
        if bedY > robotY :
            #pass
            bedH = -bedH
            robotH = -robotH
        drawTools.drawRect(image, bed, bedH, bedX*20, bedY*20)
        drawTools.drawRect(image, robot, robotH, robotX*20, robotY*20)
        print(robotH)
        #cv2.imwrite("images/trailer/"+str(x)+".png", image)
        cv2.imshow('image', image)
        cv2.waitKey()

        #print(x)
        #print(time)
    