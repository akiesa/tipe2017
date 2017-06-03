import serial


class TransferManager:
	def __init__(self, deltaX, Z):
		self.deltaX=deltaX
		self.Z=Z


	def Transfer(self, deltaX, Z):
		transferData=[X,Z]
		i=0
		while i<1:
			Data=int(transferData[i])
			ser.write(Data)
			if ser.read() != Data:
				i=i+1

