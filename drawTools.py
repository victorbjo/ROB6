from math import radians, cos, sin
import cv2
import numpy as np
from loadParams import *
# Load image, convert to grayscale, Otsu's threshold for binary image
#image = cv2.imread('1.jpg')
def meterToPixel(meters):
    return meters * 20
def drawRect(tempimg, vehicle, angle, x, y):
    length = meterToPixel(vehicle.length)
    width = meterToPixel(vehicle.width)
    center = meterToPixel(vehicle.x)
    wheelBaseX = length/2 - center
    actualX = int(wheelBaseX * cos(radians(angle)))
    actualY = int(wheelBaseX * sin(radians(angle)))
    x, y = int((x)), int((y))
    rect = ((x+actualX, y+actualY), (length, width), angle)
    box = np.int0(cv2.boxPoints(rect))
    tempimg[y][int(x)] = [0,0,0]
    cv2.drawContours(tempimg, [box], 0, (255,0,0), 1)
if __name__ == "__main__":
    image = cv2.imread('testMap.png')
    drawRect(image, robot, -90, 140, 140)
    drawRect(image, bed, -90, 140, 200)
    #90.00000000000001 14.0000000000000 17.0000000000000
    #-90.00000000000001 14 14
    #drawRect(image, x.bed, 40, 21.5, 20)
    cv2.imshow('image', image)
    cv2.waitKey()