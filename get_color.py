import cv2
import numpy as np
import serial
import time

img = cv2.imread("origin.png", cv2.IMREAD_COLOR)  # read camera frame

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert from BGR to HSV

lower_blue = np.array([100, 100, 120])  # range of blue
upper_blue = np.array([150, 255, 255])

lower_green = np.array([50, 150, 50])  # range of green
upper_green = np.array([80, 255, 255])

lower_red = np.array([0, 50, 50])  # range of red
upper_red = np.array([30, 255, 255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)  # color range of blue
mask1 = cv2.inRange(hsv, lower_green, upper_green)  # color range of green
mask2 = cv2.inRange(hsv, lower_red, upper_red)  # color range of red

# Bitwise-AND mask and original image
res = cv2.bitwise_and(img, img, mask=mask)  # apply blue mask
res1 = cv2.bitwise_and(img, img, mask=mask1)  # apply green mask
res2 = cv2.bitwise_and(img, img, mask=mask2)  # apply red mask

cv2.imshow("IMAGE", img)  # show original frame
cv2.imshow('BLUE', res)  # show applied blue mask
cv2.imwrite("blue.png", res)
cv2.imshow('GREEN', res1)  # show appliedgreen mask
cv2.imwrite("green.png", res1)
cv2.imshow('RED', res2)  # show applied red mask
cv2.imwrite("red.png", res2)
'''
    k = cv2.waitKey(5) & 0xFF

    if k == 27:
        break
'''
cv2.waitKey()
cv2.destroyAllWindows()
