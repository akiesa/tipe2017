
class MeasureParameters:

	def __init__(self, fps, markersWidth, markersHeight, cameraFloorDistance, markerZLength):
		self.fps=fps
		self.markersWidth=markersWidth
		self.markersHeight=markersHeight
		self.cameraFloorDistance=cameraFloorDistance
		self.markerZLength=markerZLength



class DetectionParameters:

	def __init__(self, lower, upper, trackingColor=(0,0,255), maskFrameTitle="Masque sans titre"):
		self.lower=lower
		self.upper=upper
		self.trackingColor=trackingColor
		self.maskFrameTitle=maskFrameTitle