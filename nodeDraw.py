import cv2
import json
import numpy as np
#image = cv2.imread("images/RunKinAndAngles.png")
#image = cv2.imread("images/RunNoAngularConstraints.png")
image = cv2.imread("images/test.png")
shapes = np.zeros_like(image, np.uint8)
radius = 20
goalRadius = 10
config = open("config.json")
config = json.load(config)
color = (30, 30, 255)
color2 = (80, 80, 80)
image = cv2.circle(image, (222,80), 4, color, -1)
image = cv2.circle(image, (400,160), 4, color, -1)
cv2.circle(shapes, (400,160), 20, color2, 2)
out = image.copy()
alpha = 0.5
mask = shapes.astype(bool)
out[mask] = cv2.addWeighted(image, alpha, shapes, 1 - alpha, 0)[mask]
cv2.imshow('Output', out)
cv2.waitKey()