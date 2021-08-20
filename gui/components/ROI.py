import numpy as np
import cv2


class ROI:
	def __init__(self, points=[], maxPoints=1000, segmentLength=10):
		self.maxPoints = maxPoints
		self.segmentLengt = segmentLength
		self.points = points
		self.undoIndex = 0
	
	def setPoints(self, points):
		self.points = points

	def distance(self, point1, point2):
		x1, y1 = point1
		x2, y2 = point2
		dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		return dist

	def addPoint(self, *args):
		if len(args) < 2:
			newPoint = args[0]
		else:
			newPoint = [args[0], args[1]]
		if self.maxPoints <= len(self.points):
			lasPoint = self.points[-1]
			if self.distance(lasPoint, newPoint) >= self.segmentLengt:
				self.points.append(newPoint)
	
	def undo(self):
		self.points.pop()

	def redo(self):
		self.undoIndex += 1
		if self.undoIndex > len(self.points):
			self.undoIndex = 0
	
	def clear(self):
		self.points = []

	def drawLines(self, color=(0, 0, 255)):
		pass

	def paint(self, array, label=1):
		points = np.array(self.points)
		painted = cv2.fillPoly(array, [points], label)
		return painted

# mask = np.zeros((300, 300))
vertices = [[10, 30], [40, 50], [60, 100], [50, 250]]
polygon = ROI(vertices)
polygon.addPoint(2, 3)
# new = polygon.paint(mask, label=2)
# print(new.max())

# cv2.imshow("mask", new)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#print(indx[0])

# polygon = Polygon(vertices)
# polygon.fillZeroArray(mask)