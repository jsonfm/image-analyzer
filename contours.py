import numpy as np

class Contour(object):
	def __init__(self):
		self.lineOfPoints = []
		self.x_list = []
		self.y_list = []

	def addPoint(self, point):
		point = np.array(point)
		self.x_list.append(point[0])
		self.y_list.append(point[1])
		self.lineOfPoints.append(point)

	def clear(self):
		self.lineOfPoints = []

	def getPoints(self):
		return self.lineOfPoints

	def scalePoints(self,factorX, factorY):
		for i in range(len(self.lineOfPoints)):
			x, y = int(self.lineOfPoints[i][0]/factorX), int(self.lineOfPoints[i][1]/factorY)
			self.x_list[i] = x 
			self.y_list[i] = y
			self.lineOfPoints[i] = [x,y]

	def findArea(self):
		area = 0
		print(" ---- x ----")
		print(sorted(self.x_list))
		print("N: ", len(self.x_list))
		print("a: ", min(self.x_list))
		print("b: ", max(self.x_list))
		print(" ---- y ----")
		print(sorted(self.y_list))
		print("N: ", len(self.y_list))
		print("a: ", min(self.y_list))
		print("b: ", max(self.y_list))
		return area