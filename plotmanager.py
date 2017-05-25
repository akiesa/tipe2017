import numpy as np
import matplotlib.pyplot as plt
import math

class PlotManager:

	def __init__(self, plotInterval):
		self.plotInterval=plotInterval


	def drawSpeedPlot(self, data, title, path):
		time=np.arange(0,self.plotInterval*len(data), self.plotInterval)
		speed=np.array([math.sqrt(elem[0]**2 + elem[1]**2) for elem in data])
		
		plt.plot(time, speed)
		plt.xlabel('time (s)')
		plt.ylabel('speed (m.s-1)')
		plt.title(title)
		plt.grid(True)
		plt.savefig(path)
		plt.show()