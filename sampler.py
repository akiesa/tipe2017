import math
class Sampler:
	def __init__(self, samplePeriod, measurePeriod):
		self.measureList=[]
		self.samplePeriod=samplePeriod
		self.measurePeriod=measurePeriod
		self.registerIndex=math.floor(samplePeriod/measurePeriod)

	def registerData(self, data):
		if self.registerIndex==math.floor(self.samplePeriod/self.measurePeriod):
			self.measureList.append(data)
			self.registerIndex=0
		else:
			self.registerIndex = self.registerIndex + 1

	def getData(self):
		return self.measureList
