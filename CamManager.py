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
from detectionmanager import *
from parameters import *
from initialisationsingleton import *

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
testMeasureParameters = MeasureParameters(config["SUPPOSED_FPS"], config["MARKERS_WIDTH"], config["MARKERS_HEIGHT"], config["CAMERA_FLOOR_DISTANCE"], config["MARKER_Z_LENGTH"])
greenDetectionArea = DetectionParameters(config["GREEN_LOWER"], config["GREEN_UPPER"], TRACK_COLOR_LINE, "Ball detection mask")
blueDetectionArea = DetectionParameters(config["CYAN_LOWER"], config["CYAN_UPPER"], TRACK_COLOR_LINE, "Markers detection mask")
redDetectionArea = DetectionParameters(config["RED_LOWER"], config["RED_UPPER"], TRACK_COLOR_LINE, "Robot detection mask")
#greenpureDetectionArea = DetectionParameters(config["GREENPURE_LOWER"], config["GREENPURE_UPPER"], TRACK_COLOR_LINE, "init detection mask")

#Plot
plotSampler=Sampler(PLOT_TIME_INTERVAL, testMeasureParameters.fps)
plotManager=PlotManager(PLOT_TIME_INTERVAL)

"""
((x, y), radius) = cv2.minEnclosingCircle(largestContour)

"""




def run():
	print("Run Camera")

	camera = cv2.VideoCapture(0)
	pts = deque(maxlen=BUFFER_SIZE)
	while True:
		# grab the current frame
		(grabbed, frame) = camera.read()

		frame = imutils.resize(frame, width=600, height=500)
		detectionManager = DetectionManager(frame)
		#--------------------------------------------------------------
		#---- Find ping pong table markers and modelize TT
		#--------------------------------------------------------------

		rectTableTennis=None;
		estimatedCentroids=detectionManager.processMultiTarget(blueDetectionArea)
		if len(estimatedCentroids) > 0:
			#With all found markers, draw a rectangle simultating table tennis
			pointsElected=GeometricUtils.calculateLongestDistance(estimatedCentroids)
			rectTableTennis=Rect(pointsElected[0], pointsElected[1])
			cv2.rectangle(frame, pointsElected[0], pointsElected[1], blueDetectionArea.trackingColor)
			

		#--------------------------------------------------------------
		#---- Ball detection
		#--------------------------------------------------------------
		
		ballCenter = (0,0)
		estimatedCentroid = detectionManager.processSingleTarget(greenDetectionArea,True)
		if estimatedCentroid != None:
			ballCenter=estimatedCentroid

		#Red Detection
		
		if InitialisationSingleton.instance == None:
			redCentroid =  detectionManager.processSingleTarget(redDetectionArea)
			#focal = detectionManager.determineFocal(testMeasureParameters, greenpureDetectionArea)

			if redCentroid != None:#and focal != None:
				initialisationSingleton=InitialisationSingleton(redCentroid, 0)
		


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