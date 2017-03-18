# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 20:39:23 2017

@author: Aquiésa
"""

import numpy as np
import cv2


VIDEO_PATH="resources/test.flv"  

# #cv2.COLOR_RGB2HSV
cap = cv2.VideoCapture(VIDEO_PATH)

#if(cap.isOpened()):
#    return -1;

while(cap.isOpened()):

    # Take each frame
    ret, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([150,50,50])
    upper_blue = np.array([200,155,155])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
