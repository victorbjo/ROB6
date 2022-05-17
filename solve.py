from sympy.solvers import solve
from sympy import *
from cmath import cos, sin
from math import radians, degrees
from loadParams import *
import drawTools
x = Symbol('x')
import cv2
def norm(a, b):
    return simplify(sqrt((a**2) + (b**2)))
def trajectoryGen(tf, startX, startY, goalX, goalY, startAngle, goalAngle):
    x_r_0 = [startX,startY]
    x_r_t = [goalX,goalY]
    v_0 = startAngle
    v_t = goalAngle
    h_r_0 = [cos(radians(v_0)).real, sin(radians(v_0)).real]
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

    L = 3 #Needs to be fixed, not hard programmed
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
    print(length)
    return x_b_0, h_b_0, xRobot, heading
    #print(x_b_0)
    print(length)

xBed, hBed, xRobot, hRobot = trajectoryGen(2, 7, 7, 14, 14, 135, 45)
image = cv2.imread('blank.png')
compound = True
for x in range (len(xBed)-1):
    time = 0.05*x
    if (compound):
        image = cv2.imread('blank.png')
    bedX = (round(xBed[x][0],2))
    bedY = (round(xBed[x][1],2))
    bedH = degrees(acos(hBed[x][0]))
    robotX = xRobot[0].subs("t", time)
    robotY = xRobot[1].subs("t", time)
    robotH = degrees(acos(hRobot[0].subs("t",time)))
    drawTools.drawRect(image, bed, bedH, bedX, bedY)
    drawTools.drawRect(image, robot, robotH, robotX, robotY)
    #cv2.imwrite("images/trailer/"+str(x)+".png", image)
    cv2.imshow('image', image)
    cv2.waitKey()

    #print(x)
    #print(time)
