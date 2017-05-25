from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import math
from sampler import *
from rect import *
from speedcalculator import *
from plotmanager import *
from config import *


#input output parameters
BUFFER_SIZE = 64

#Track colors
TRACK_COLOR_LINE = (0, 0, 255)

#Capture properties
PLOT_TIME_INTERVAL=0.1
PLOT_SPEED_GRAPH_PATH="speed.png"
PLOT_SPEED_GRAPH_TITLE="Evolution vitesse m.s-1" 

#Import environment parameters


#Parameters
config=Config.createTestGlobalConfiguration()
testMeasureParameters = MeasureParameters(config["SUPPOSED_FPS"], config["MARKERS_WIDTH"], config["MARKERS_HEIGHT"])
greenDetectionArea = DetectionParameters(config["GREEN_LOWER"], config["GREEN_UPPER"])
blueDetectionArea = DetectionParameters(config["CYAN_LOWER"], config["CYAN_UPPER"])

#Plot
plotSampler=Sampler(PLOT_TIME_INTERVAL, testMeasureParameters.fps)
plotManager=PlotManager(PLOT_TIME_INTERVAL)




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

		blueMask = buildMask(hsv, blueDetectionArea)
		cv2.imshow("BlueMask", blueMask)
		blueCnts = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
		

		rectTableTennis=None;
		if len(blueCnts) > 2:
			markers=[]
			for cnt in blueCnts:
				marker = trackBallCenter(cnt)
				markers.append(marker)


			#With all found markers, draw a rectangle
			pointsElected=GeometricUtils.calculateLongestDistance(markers)
			rectTableTennis=Rect(pointsElected[0], pointsElected[1])


			#Modelizes the table tennis
			cv2.rectangle(frame, pointsElected[0], pointsElected[1], TRACK_COLOR_LINE)
		

		#--------------------------------------------------------------
		#---- Ball detection
		#--------------------------------------------------------------
		
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
		
		if rectTableTennis != None and rectTableTennis.contains(ballCenter):
			
			speedcalculator=SpeedCalculator(pts,(rectTableTennis.width(), rectTableTennis.height()), testMeasureParameters)
			speed=speedcalculator.processSpeedCalculation(ballCenter)

			#giveToEat for matplotlib
			if speed != None:
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
			plotManager.drawSpeedPlot(data,PLOT_SPEED_GRAPH_TITLE, PLOT_SPEED_GRAPH_PATH)

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

#TODO : Renommer ce truc là
def trackBallCenter(largestContour):
	# find the largest contour in the mask, then use
	# it to compute the centroid
	M = cv2.moments(largestContour)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	return center


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

run()