from PyQt5.QtGui import QPolygon, QPolygonF, QPainterPath, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint, QPointF
import numpy as np


class PencilROI(object):
	def __init__(self, ID="default"):
		self.ID = ID
		self.points = []
		self.polygon = None
		self.path = QPainterPath()
		self.brush = QBrush(QColor(235, 70, 70, 90))

		#
		self.widthFactor = 1
		self.heightFactor = 1
		# Painter
		self.color = QColor(245, 30, 30)
		self.pen = QPen(self.color, 2, Qt.SolidLine)

	def readID(self):
		"""It returns ID of the roi"""
		return self.ID

	def setID(self, name):
		"""It sets a new name to the roi"""
		self.ID = name

	def drawLine(self, pixmap):
		if self.hasPoints():
			painter = QPainter()
			painter.begin(pixmap)
			painter.setPen(self.pen)
			for i in range(len(self.points) - 1):
				painter.drawLine(self.points[i], self.points[i + 1])
			painter.end()
			return pixmap

	def addPoint(self, point):
		if isinstance(point, list):
			point = QPointF(*point)
			self.points.append(point)

		if isinstance(point, QPoint):
			point = QPointF(point.x(), point.y())
			self.points.append(point)

	def getPolygon(self):
		"""It returns a QPolygon Object"""
		if len(self.points) > 1:
			return QPolygonF(self.points)
		return None

	def updatePolygon(self):
		"""It creates a new polygon with the current list of points"""
		if len(self.points) > 1:
			self.polygon = QPolygonF(self.points)

	def getPoints(self):
		return self.points

	def scalePoints(self, factorX, factorY):
		"""It scales the points"""
		for i in range(len(self.points)):
			self.points[i].setX(self.points[i].x()*factorX)
			self.points[i].setY(self.points[i].y()*factorY)

	def findArea(self):
		""""""
		area = 0
		for i in range(len(self.points) - 1):
			area += self.points[i][0]*self.points[i+1][1] - self.points[i + 1][0] * self.points[i][1]
		return abs(area/2)

	def getContour(self, scale=False, wf=1, hf=1):
		"""Obtain list of points in contour format, based on opencv
		:param scale: scale points flag
		:param wf: width factor
		:param hf: height factor
		"""
		if scale:
			self.scalePoints(wf, hf)
		contour = []
		if self.hasPoints():
			for point in self.points:
				contour.append([point.x(), point.y()])
		contour = np.around([contour]).astype(np.int32)
		return contour

	def hasPoints(self):
		"""It verifies if there are point"""
		return len(self.points) > 1

	def isClosed(self):
		if self.hasPoints():
			L = len(self.points)
			# Initial point
			p0 = self.points[0] 
			for i in range(L-1):
				# Final point
				pf = self.points[L - i - 1]
				if p0 == pf:
					return True
		return False

	def paintROI(self, pixmap):
		polygon = self.getPolygon()
		self.path.addPolygon(polygon)
		painter = QPainter()
		painter.begin(pixmap)
		painter.fillPath(self.path, self.brush)
		painter.end()

	def updateScaleFactors(self, widthFactor=1, heightFactor=1):
		"""It updates the scale factors
		:param widthFactor: width factor
		:param heightFactor: height factor
		"""
		self.widthFactor = widthFactor
		self.heightFactor = heightFactor

	def clear(self):
		"""It clears the points saved"""
		self.points = []
		self.polygon = None
		self.path = QPainterPath()

