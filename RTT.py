import random
import math
import matplotlib.pyplot as plt
import cv2
def randomPoint(radius, circleX, circleY):
    # random angle
    alpha = 2 * math.pi * random.random()
    # random radius
    r = radius * math.sqrt(random.random())
    # calculating coordinates
    x = r * math.cos(alpha) + circleX
    y = r * math.sin(alpha) + circleY
    return[x],[y]
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
    cv2.line(newImage, (x0,y0),(x1,y1), color, 3)
    if checkLine(newImage, imgOld):
        cv2.line(imgOld, (x0,y0),(x1,y1), color, 3)

img = cv2.imread("mymap.pgm")
imgOrig = cv2.imread("mymap.pgm")
makeLine(img, 70, 100, 70, 110)
makeLine(img, 100, 100, 70, 110)
makeLine(img, 70, 110, 80, 110)
cv2.imshow("Image", img)
cv2.waitKey()
