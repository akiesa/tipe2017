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


	def drawSquareline(self, pts):

		#time=np.arange(0,self.plotInterval*len(pts), self.plotInterval)
		x=np.array([elem[0] for elem in pts])
		y=np.array([elem[1] for elem in pts])

		A = np.vstack([x, np.ones(len(x))]).T
		m, c = np.linalg.lstsq(A, y)[0]
		plt.plot(x, y, 'o', label='Original data', markersize=10)
		plt.plot(x, m*x + c, 'r', label='Fitted line')
		plt.legend()
		plt.show()
