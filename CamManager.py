from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import math
import logging
import itertools
import matplotlib.pyplot as plt
from sampler import *
from rect import *

#markers (in meters)
MARKERS_WIDTH = 32 * 10**(-2) 
MARKERS_HEIGHT = 32 * 10**(-2)
SUPPOSED_FPS = 30

#masks
GREEN_LOWER = (23, 23, 102)
GREEN_UPPER = (100, 100, 250)
CYAN_LOWER = (23, 50, 100)
CYAN_UPPER = (200, 255, 255)

#input output parameters
BUFFER_SIZE = 64

#Track colors
TRACK_COLOR_LINE = (0, 0, 255)

#Capture properties
PLOT_TIME_INTERVAL=0.1


class DetectionParameters:

	def __init__(self, lower, upper):
		self.lower=lower
		self.upper=upper

logging.basicConfig(filename='cammanager.log',level=logging.DEBUG)
plotSampler=Sampler(PLOT_TIME_INTERVAL, SUPPOSED_FPS)


def run():
	print("Run Camera")
	camera = cv2.VideoCapture(0)
	pts = deque(maxlen=BUFFER_SIZE)

	while True:
		# grab the current frame
		(grabbed, frame) = camera.read()

		frame = imutils.resize(frame, width=600, height=500)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		

		#--------------------------------------------------------------
		#---- Find ping pong table markers
		#--------------------------------------------------------------

		blueDetectionArea = DetectionParameters(CYAN_LOWER, CYAN_UPPER)
		blueMask = buildMask(hsv, blueDetectionArea)
		cv2.imshow("BlueMask", blueMask)
		blueCnts = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
		

		rect=None;
		if len(blueCnts) > 2:
			markers=[]
			for cnt in blueCnts:
				marker = trackBallCenter(cnt)
				markers.append(marker)


			#With all found markers, draw a rectangle
			pointsElected=calculateLongestDistance(markers)
			rect=Rect(pointsElected[0], pointsElected[1])


			#Modelizes the table tennis
			cv2.rectangle(frame, pointsElected[0], pointsElected[1], TRACK_COLOR_LINE)
		

		#--------------------------------------------------------------
		#---- Ball detection
		#--------------------------------------------------------------
		
		greenDetectionArea = DetectionParameters(GREEN_LOWER, GREEN_UPPER)
		greenMask = buildMask(hsv, greenDetectionArea)
		cv2.imshow("GreenMask", greenMask)
		cnts = cv2.findContours(greenMask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
		#Find ball position
		ballCenter = (0,0)
		if len(cnts) > 0:
			largestContour = max(cnts, key=cv2.contourArea)
			ballCenter = trackBallCenter(largestContour)
			drawEnclosingCircle(frame, largestContour, ballCenter)

		print("BallCenter" + str(ballCenter))

		#--------------------------------------------------------------
		#---- Calculate ball speed
		#--------------------------------------------------------------
		
		if rect != None:
			
			#Is data available to creat
			isPtsDataExploitable = len(pts)>0 and pts[-1] != None

			if rect.contains(ballCenter) and isPtsDataExploitable:

				speed = calculateSpeed(pts[-1], ballCenter, rect)
				realSpeed = math.sqrt(speed[0]**2 + speed[1]**2)
				#Take account results - plot/log
				logging.debug("Speed : " + str(speed) + "/Real sp." + str(realSpeed))

				#giveToEat for matplotlib
				plotSampler.registerData(speed)

				


		#--------------------------------------------------------------
		#---- Draw track line to follow ball
		#--------------------------------------------------------------

		pts.appendleft(ballCenter)
		drawTrackLine(frame, pts)

		cv2.imshow("Frame", frame)

		# if the 'q' key is pressed, stop the loop
		key = cv2.waitKey(1) & 0xFF
		if key == ord("p"):
			data=plotSampler.getData()
			drawPlot(data)

		if key == ord("q"):
			break

	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()



def buildMask(hsv, detectionParameters):
	mask = cv2.inRange(hsv, detectionParameters.lower, detectionParameters.upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	return mask

def trackBallCenter(largestContour):
	# find the largest contour in the mask, then use
	# it to compute the centroid
	M = cv2.moments(largestContour)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	return center

def calculateSpeed(last,current,rect):
	deltaX=current[0]-last[0]
	deltaY=current[1]-last[1]

	#Meters by frame
	deltaXRealLife = MARKERS_WIDTH/rect.width()*deltaX
	deltaYRealLife = MARKERS_HEIGHT/rect.height()*deltaY

	speedX = deltaXRealLife * SUPPOSED_FPS
	speedY = deltaYRealLife * SUPPOSED_FPS
	return (speedX, speedY)


def calculateLongestDistance(pointsList):
	max=((), 0.0)
	for couple in itertools.combinations(pointsList,2):
		pt1=Point(couple[0][0], couple[0][1])
		pt2=Point(couple[1][0], couple[1][1])
		distance=pt1.distance_to(pt2)
		if(distance>max[1]):
			max=((pt1.as_tuple(), pt2.as_tuple()), distance)

	return max[0]


def drawEnclosingCircle(frame, largestContour, ballCenter):
	#Will draw circle if radius meets a minimum size
	((x, y), radius) = cv2.minEnclosingCircle(largestContour)
	if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, ballCenter, 5, (0, 0, 255), -1)

def drawTrackLine(frame, pts): 
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(BUFFER_SIZE / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], TRACK_COLOR_LINE, thickness)


def drawPlot(data):
	time=np.arange(0,PLOT_TIME_INTERVAL*len(data), PLOT_TIME_INTERVAL)
	speed=np.array([math.sqrt(elem[0]**2 + elem[1]**2) for elem in data])
	
	plt.plot(time, speed)
	plt.xlabel('time (s)')
	plt.ylabel('speed (m.s-1)')
	plt.title('Notre superbe graphe')
	plt.grid(True)
	plt.savefig("test.png")
	plt.show()



run()