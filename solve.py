from sympy.solvers import solve
from sympy import *
from cmath import cos, sin
from math import radians
x = Symbol('x')
#print(solve(x**2-1, x))
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
    x = Matrix([a*t**3 + b*t**2 + c*t +d, a1*t**3 + b1*t**2 + c1*t +d1])

    args = Matrix([t])
    dx = x.jacobian(args)#Calculates jacobian
    #print(dx)
    ws = norm(dx[0], dx[1])
    print("FUCK0")
    heading = dx/ws
    print(heading.subs(t, "1"))
    #ws.subs(t, 10)
    #print(ws.subs(t, 1))
    #print(ws)
    time = [0.05, tf]

    #Constants

    L = 2.5 #Needs to be fixed, not hard programmed
    R = Matrix([[0, -1],[1,0]])
    r = 0.1#radius of robot wheels
    D = 0.2#distance between wheels
    x_r_0Matrix = Matrix([x_r_0[0],x_r_0[1]])
    h_r_0Matrix = Matrix([h_r_0[0],h_r_0[1]])

    x_b_0 = [x_r_0Matrix - L * h_r_0Matrix]
    h_b_0 = [h_r_0Matrix]
    #print("FYCJ")
    #print(x_b_0)
    #print(ws)
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

trajectoryGen(2, 1, 1, 2, 2, 90, 90)