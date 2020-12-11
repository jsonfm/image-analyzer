from PyQt5.QtGui import QPolygon, QPolygonF, QPainterPath, QPainter, QColor, QBrush
from PyQt5.QtCore import QPoint, QPointF
import numpy as np


class pencilROI(object):
	def __init__(self):
		self.points = []
		self.polygon = None
		self.path = QPainterPath()
		self.brush = QBrush()

	def addPoint(self, point):
		point = QPointF(*point)
		self.points.append(point)
		
	def updatePolygon(self):
		"""create a new polygon with the current list of point"""
		if len(self.points)>1:
			self.polygon = QPolygonF(self.points)

	def getPoints(self):
		return self.points

	def scalePoints(self, factorX, factorY):
		for i in range(len(self.points)):
			self.points[i].setX(self.points[i].x()/factorX)
			self.points[i].setY(self.points[i].y()/factorY)

	def findArea(self):
		""""""
		area = 0
		for i in range(len(self.points) - 1):
			area+=self.points[i][0]*self.points[i+1][1] - self.points[i + 1][0] * self.points[i][1]
		return abs(area/2)

	def getContour(self):
		"""Obtain list of points in contour format, based on opencv"""
		contour = []
		if self.hasPoints():
			for point in self.points:
				contour.append([point.x(),point.y()])
		contour = np.around([contour]).astype(np.int32)
		return contour

	def hasPoints(self):
		"""verifies if there are point"""
		return len(self.points)>1

	def isClosed(self):
		if self.hasPoints():
			L = len(self.points)
			#Initial point
			p0 = self.points[0] 
			for i in range(L-1):
				#Final point
				pf = self.points[L - i - 1]
				if p0 == pf:
					return True
		return False

	def paintROI(self, pixmap):
		self.updatePolygon()
		brush = QBrush(QColor(235,70,70,90))
		self.path.addPolygon(self.polygon)
		painter = QPainter()
		painter.begin(pixmap)
		painter.fillPath(self.path, brush)
		painter.end()
		closed = self.isClosed()
		return pixmap
		
	def clear(self):
		self.points = []
		self.polygon = None
		self.path = QPainterPath()