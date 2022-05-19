from cmath import cos, sin
from math import radians
from matplotlib import pyplot as plt
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
    #print(a)
    #print(b)
    #print(c)
    #print(d)
    t = [0.05, tf]
    x_r = []
    y_r = []

    for x in range(int(t[1]/t[0])+1):
        T = x*t[0]
        x_r.append((a*T**3 + b*T**2 + c*T + d).real)
        y_r.append((a1*T**3 + b1*T**2 + c1*T + d1).real)
    return x_r, y_r
#trajectoryGen(2, 14, 7, 14, 14, 270, 235)
mult = 0.5
x0, y0 = trajectoryGen(2, 4.65*mult, 6.7*mult, 4.3*mult, 6.0*mult, 290.22485943116806, 288.434948822922)

x1, y1 = trajectoryGen(2, 1, 0, 2, 1, 90, 45)
x2 , y2 = trajectoryGen(2, 1, 0, 2, 1, 90, 0)
plt.figure("Trajectory Generator")
plt.plot(x0, y0, color="red")
#plt.plot(x1, y1, color="blue")
#plt.plot(x2, y2, color="#0fee0f")

plt.show()