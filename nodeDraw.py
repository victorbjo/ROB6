import cv2
import json
import numpy as np
#image = cv2.imread("images/RunKinAndAngles.png")
#image = cv2.imread("images/RunNoAngularConstraints.png")
filename = "hallwayNoKinematic1.png"
image = cv2.imread(filename)
shapes = np.zeros_like(image, np.uint8)
radius = 20
goalRadius = 10
config = open("config.json")
config = json.load(config)
color = (30, 30, 255)
color2 = (80, 80, 80)
point0 = (805,105)
point1 = (650,422)
image = cv2.circle(image, point0, 4, color, -1)
image = cv2.circle(image, point1, 4, color, -1)
cv2.circle(shapes, point1, 20, color2, 2)
out = image.copy()
alpha = 0.5
mask = shapes.astype(bool)
out[mask] = cv2.addWeighted(image, alpha, shapes, 1 - alpha, 0)[mask]
cv2.imwrite(filename, out)