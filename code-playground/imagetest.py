# -*- coding: utf-8 -*-
"""
Created on Mon Jan 02 23:01:02 2017

@author: Aquiésa
"""

import cv2
import numpy as np

#
# General properties
#

#Image general properties
IMAGE_PATH = 'resources/exp2.jpg'
IMAGE_TITLE = 'Chessboard image processing'

#Image processing parameters
COLOR_THRESHOLD = [0,0,255]


#
# Image processing function
#

#Read image
filename = IMAGE_PATH
img = cv2.imread(filename)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=COLOR_THRESHOLD


cv2.imshow(IMAGE_TITLE,img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()