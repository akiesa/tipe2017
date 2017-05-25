import logging
from parameters import *


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
			logging.debug("Speed : " + str(speed) + "/Real sp." + str(realSpeed))

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
