import serial


class TransferManager:
	def __init__(self, deltaX, Z):
		self.deltaX=deltaX
		self.Z=Z


	def transfer(self):
		transferData=[self.deltaX,self.Z]
		ser = serial.Serial("COM5", 9600)
		print("deltaX" + str(self.deltaX) + "Z" + str(self.Z))
		i=0
		while i<1:
			print(bytearray(transferData[i]))
			ser.write(bytearray(transferData[i]))
			i=i+1
		ser.close()

