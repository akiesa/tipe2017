
class MeasureParameters:

	def __init__(self, fps, markersWidth, markersHeight):
		self.fps=fps
		self.markersWidth=markersWidth
		self.markersHeight=markersHeight


class DetectionParameters:

	def __init__(self, lower, upper):
		self.lower=lower
		self.upper=upper