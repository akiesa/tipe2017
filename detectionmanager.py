import cv2
from parameters import *


class DetectionManager:

	def __init__(self, frame):
		self.frame=frame
		self.hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	def processSingleTarget(self, detectionParameters,measureParameters, needsToBeTracked=False, focal=0):
		mask = self.buildMask(detectionParameters)
		cv2.imshow(detectionParameters.maskFrameTitle, mask)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2] 

		centroid=None
		if len(cnts)>0:
			largestContour = max(cnts, key=cv2.contourArea)
			centroid = self.trackCentroid(largestContour)
			if needsToBeTracked:
				self.drawEnclosingCircle(largestContour, centroid, detectionParameters.trackingColor)
				((x, y), radius) = cv2.minEnclosingCircle(largestContour)
				if focal != 0:
					((x, y), radius) = cv2.minEnclosingCircle(largestContour)
					Z=(focal*measureParameters.ballsize)/(2*radius)
					A=[centroid , Z]
					return A

		return centroid



	def processMultiTarget(self, detectionParameters):
		mask = self.buildMask(detectionParameters)
		cv2.imshow(detectionParameters.maskFrameTitle, mask)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2] 

		centroids=[]
		if len(cnts)>=2:
			for cnt in cnts:
				centroid = self.trackCentroid(cnt)
				centroids.append(centroid)

		return centroids

	def determineFocal(self, measureParameters, detectionParameters):
		mask = self.buildMask(detectionParameters)
		cv2.imshow(detectionParameters.maskFrameTitle, mask)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2] 

		focal=None
		if len(cnts)>0:
			largestContour = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(largestContour)
			focal=radius*2*measureParameters.cameraFloorDistance/measureParameters.markerZLength

		return focal


	def buildMask(self, detectionParameters):
		mask = cv2.inRange(self.hsv, detectionParameters.lower, detectionParameters.upper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		return mask

	def trackCentroid(self, largestContour):
		# find the largest contour in the mask, then use
		# it to compute the centroid
		M = cv2.moments(largestContour)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		return center

	def drawEnclosingCircle(self, largestContour, ballCenter, trackingColor):
		#Will draw circle if radius meets a minimum size
		((x, y), radius) = cv2.minEnclosingCircle(largestContour)
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#TODO : Voir ce qu'est la couleur
			cv2.circle(self.frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(self.frame, ballCenter, 5, trackingColor, -1)
