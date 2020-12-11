from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF
import pydicom
import numpy as np
import cv2
import os 
from pencilROI import pencilROI

class Viewer:
    def __init__(self, qgraphicsView, seriesList):
        self.scene = QGraphicsScene()
        self.seriesList = seriesList

        self.Image = qgraphicsView
        self.Image.setScene(self.scene)  
        self.Image.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.Image.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.drag = False
        self.draw = False
        self._zoom = 0
        self._pixmapHandle = None

        self.root = None
        self.color = QColor(245,30,30)
        self.pen = QPen(self.color, 3, Qt.SolidLine)

        self.lastPoint = None
        self.processedImage = None
        self.qpixmap = None
        self.imgArray = None

        self.seriesList.itemSelectionChanged.connect(self.chooseImage)
        self._connectEvents()
        self.delta = None

        self.roi = pencilROI()

    def _connectEvents(self):
        self.Image.mousePressEvent = self.mousePressEvent
        self.Image.mouseReleaseEvent = self.mouseReleaseEvent
        self.Image.mouseMoveEvent = self.mouseMoveEvent
        self.Image.resizeEvent = self.resizeEvent
        self.Image.wheelEvent = self.wheelEvent

    def fitInView(self):
        if self.hasImage():
            rect = QRectF(self._pixmapHandle.pixmap().rect())
            if not rect.isNull():
                self.Image.setSceneRect(rect)
                if self.hasImage():
                    unity = self.Image.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                    self.Image.scale(1 / unity.width(), 1 / unity.height())
                    viewrect = self.Image.viewport().rect()
                    scenerect = self.Image.transform().mapRect(rect)
                    factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
                    self.Image.scale(factor, factor)

    def clear(self):
        """"""
        self.clearImage()
        self.chooseImage()
        self.roi.clear()

    def hasImage(self):
        return self._pixmapHandle is not None

    def clearImage(self):
        """Removes the current image pixmap from the scene if it exists"""
        if self.hasImage():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def getCurrentPixmap(self):
        """Get the current pixmap
        Returns:
            QPixmap | None

        """
        if self.hasImage():
            return self._pixmapHandle.pixmap()
        return None

    def getCurrentImage(self):
        """Get the current Image
        Returns:
            Qimage | None
        """
        if self.hasImage():
            return self._pixmapHandle.pixmap().toImage()
        return None

    def getImageArray(self):
        """Get the current Image Array
        Returns:
            imgArray: Numpy array
        """
        return self.imgArray 

    def wheelEvent(self, event):
        factor = 1.25
        zoomIn = factor 
        zoomOut = 1/factor

        self.Image.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.Image.setResizeAnchor(QGraphicsView.NoAnchor)
        oldPos = self.Image.mapToScene(event.pos())   
            
        if self.hasImage():
            if event.angleDelta().y()>0:
                self._zoom += 1
            else:
                self._zoom -= 1

            if self._zoom == 0:
                self.fitInView()
            else:
                if self._zoom > 0:
                    self.scale(zoomIn)
                else:
                    self.scale(zoomOut)

            newPos = self.Image.mapToScene(event.pos()) 
            delta = newPos - oldPos
            self.delta = delta
            self.Image.translate(delta.x(), delta.y())                  

    def scale(self, factor):
        self.Image.scale(factor, factor)

    def resizeEvent(self, event):
        self.fitInView()

    def mousePressEvent(self, event):
        """ When the mouse is pressed  do this
        """     
        scenePos = self.Image.mapToScene(event.pos())
        if event.button() == Qt.LeftButton:
           if self.draw:
              print("dibujar")
           if self.drag:
              self.Image.setDragMode(QGraphicsView.ScrollHandDrag)
        self.lastPoint = event.pos()
        self.roi.addPoint([event.pos().x(),event.pos().y()])

        #Do whatever was on the default mousePressEvent fucntion of QgraphicsView object            
        QGraphicsView.mousePressEvent(self.Image, event)

    def mouseReleaseEvent(self, event):
        self.roi.addPoint([event.pos().x(),event.pos().y()])
        pass

    def mouseMoveEvent(self, event):
        if self.draw:
            x, y = event.pos().x(), event.pos().y()
            if self.hasImage():
                pixmap = self.getCurrentPixmap()
                painter = QPainter()
                painter.begin(pixmap)
                painter.setPen(self.pen)
                painter.drawLine(self.lastPoint, event.pos())
                painter.end()
                self.setPixmap(pixmap)
                self.lastPoint = event.pos()

                self.roi.addPoint([event.pos().x(), event.pos().y()])
        QGraphicsView.mouseMoveEvent(self.Image, event)

    def setPixmap(self, pixmap):
        """Set a pixmap
        Args:
            pixmap: QPixmap
        """
        self._pixmapHandle.setPixmap(pixmap)
        self.fitInView()

    def zoomPlus(self):
        print("zoom ++")

    def zoomMinus(self):
        print("zoom --")

    def resetZoom(self):
        self._zoom = 0
        if self.hasImage():
           self.fitInView()

    def setDraw(self, draw):
        self.draw = draw
        if draw:
            self.Image.setCursor(QtCore.Qt.CrossCursor)
        else:
            self.Image.setCursor(QtCore.Qt.ArrowCursor)

    def setDrag(self, drag):
        """Set drag flag
        Args:
            drag: Bool 
        """
        self.drag = drag
        if drag:
            self.Image.setDragMode(QGraphicsView.ScrollHandDrag)

        else:
            self.Image.setDragMode(QGraphicsView.NoDrag)

    def chooseImage(self):
        """Choose a Image from the list of images
        """
        item = self.seriesList.currentItem()
        img = self.readDicomImage(self.root + "/" + item.text())
        self.imgArray = img
        self.setImage(img)

    def setImage(self, img):
        """Show image in the Graphic scene widget
        Args:
            img: numpy array
        """
        pixmap = self.arrayToPixmap(img)
        if pixmap:
            if self.hasImage():
               self._pixmapHandle.setPixmap(pixmap)
            else:
               self._pixmapHandle = self.scene.addPixmap(pixmap)
        self.Image.setSceneRect(QRectF(pixmap.rect())) 
        self.fitInView()

    def arrayToPixmap(self, img):
        """Numpy array to Qpixmap
        Args:
            img: numpy array

        Returns:
            pixmap: QPixmap
        """
        qformat = QImage.Format_Indexed8
        if len(img) == 3:
        	if img.shape[2] == 4:
        		qformat = QImage.Format_RGBA8888
        	else:
        		qformat = QImage.Format_RGB888
        w, h = self.Image.width(), self.Image.height()
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        backlash = self.Image.lineWidth()*2
        pixmap = QPixmap.fromImage(img).scaled(w-backlash, h-backlash, Qt.IgnoreAspectRatio)
        return pixmap

    def linearConvert(self, img):
    	"""Convert image
        Args:
            img: numpy array

        Returns
            new_img: new numpy array

        """
    	factor = 255/(np.max(img) - np.min(img))
    	new_img = factor*img - (factor*np.min(img))
    	return new_img	

    def readDicomImage(self, fname, copy=False):
        """read dicom image
        Args:
            fname: filename
            copy: if It's True returns numpy.copy()
        Returns 
            img: numpy array
        """
        dcm = pydicom.dcmread(fname)
        img = dcm.pixel_array*dcm.RescaleSlope + dcm.RescaleIntercept
        img = self.linearConvert(img).astype(np.uint8)
        return img if copy else img.copy()
    	

    def loadDicomSeries(self, path):
        """Load a list of dicom Files coming from a path
        Args:
            path: (str) is a folder with dicom files
        """
        for root, _ , files in os.walk(path):
            self.root = root
            self.seriesList.addItems(sorted(files))

    def processRoi(self):
        """Process ROI"""
        img = self.getImageArray()
        pixmap = self.getCurrentPixmap()
        qimage = self.getCurrentImage()
        w1, h1 = img.shape[0], img.shape[1]
        w2, h2 = pixmap.width(), pixmap.height()
        factorX = w2/w1
        factorY = h2/h1
        cnt = self.roi.getContour()
        pixmap = self.roi.paintROI(pixmap)
        print("Area 1: ", cv2.contourArea(cnt))
        self._pixmapHandle.setPixmap(pixmap)
        self.fitInView()
        self.roi.clear()
