import logging
import numpy as np
from parameters import *
from initialisationsingleton import *



logging.basicConfig(filename='cammanager.log',level=logging.DEBUG)

class SpeedCalculator:

	#pts is all tracked points
	#relatedDimensions is width and height scanned by the camera
	#measureParameters contains all measure environment specific parameters
	def __init__(self, pts, relatedDimensions, measureParameters):
		self.pts=pts
		self.relatedDimensions=relatedDimensions
		self.measureParameters=measureParameters

	#Defines a workflow for speed calculation
	def processSpeedCalculation(self, currentPosition):
		
		#Is data available to creat
		speed=None
		isPtsDataExploitable = len(self.pts)>0 and self.pts[-1] != None

		if isPtsDataExploitable:
			speed=self.calculate2DSpeed(self.pts[-1], currentPosition)
			realSpeed=(speed[0]**2+speed[1]**2)**(1/2)
			#logging.debug("Speed : " + str(speed) + "/Real sp." + str(realSpeed))
			'''
			xTarget=self.estimateArduinoTargetPosition(self.pts[-1], currentPosition)
			logging.debug("initPos" + str(InitialisationSingleton.instance.robotInitialPosition) + "/XTarget" + str(xTarget))
			#InitialisationSingleton.instance.xTargets.append(xTarget)
			'''

		return speed


	def calculate2DSpeed(self, last, current):
		deltaX=current[0]-last[0]
		deltaY=current[1]-last[1]

		#Meters by frame
		deltaXRealLife = self.measureParameters.markersWidth/self.relatedDimensions[0]*deltaX
		deltaYRealLife = self.measureParameters.markersHeight/self.relatedDimensions[1]*deltaY

		speedX = deltaXRealLife * self.measureParameters.fps
		speedY = deltaYRealLife * self.measureParameters.fps
		return (speedX, speedY)

	#TODO : Mais l'Arduino ne devra pas bien sur dépasser les bords du rectangle
	def estimateArduinoTargetPosition(self):

		xTarget=None
		isPtsDataExploitable = len(self.pts)>0 and self.pts[-1] != None
		if isPtsDataExploitable:
			robotCoordinates=InitialisationSingleton.instance.robotInitialPosition
			exploitablePoints = np.array([pt for pt in self.pts if pt is not None])
			x=np.array([elem[0] for elem in exploitablePoints])
			y=np.array([elem[1] for elem in exploitablePoints])

			A = np.vstack([x, np.ones(len(x))]).T
			m, c = np.linalg.lstsq(A, y)[0]

			xTarget = (robotCoordinates[1]-c)/m
		return xTarget


		

