from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF, QPointF
import pydicom
import numpy as np
import cv2
import os
from pencil_roi import PencilROI
from multiple_roi import MultipleROI
from utils import *


class Viewer:
    """Viewer class that manages images display
    :param qgraphicsView: QGraphicsView Object that displays the image
    :param seriesList: QListWidget, It's used to show the list of the images (series)
    :param positionLabel: Label for show the current position of the mouse
    :param intensityLabel: Label for show the current Intensity on the current position of the mouse
    :param sliceNoLabel: Laber for show the current slice Index
    :param: roiList: QListWridget for show the ROIs elements
    """

    def __init__(self, qgraphicsView, seriesList, positionLabel, intensityLabel, sliceNoLabel, meanLabel, pixelNumberLabel,
                 areaVolLabel, roiList):
        self.scene = QGraphicsScene()
        self.seriesList = seriesList
        self.positionLabel = positionLabel
        self.intensityLabel = intensityLabel
        self.sliceNoLabel = sliceNoLabel
        self.meanLabel = meanLabel
        self.pixelNumberLabel = pixelNumberLabel
        self.areaVolLabel = areaVolLabel
        self.roiList = roiList

        self.Image = qgraphicsView
        self.Image.setScene(self.scene)
        self.Image.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.Image.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.Image.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.Image.setResizeAnchor(QGraphicsView.NoAnchor)

        self.drag = False
        self.draw = False
        self.pressed = False
        self.originalPixmap = None
        self._pixmapHandle = None
        self._zoom = 0
        self.zoomInFactor = 1.1
        self.zoomOutFactor = 1/self.zoomInFactor

        # Image Factors
        self.imgArrayWidthFactor = 1
        self.imgArrayHeightFactor = 1

        # List
        self.root = None
        self.filesList = []

        # Painter
        self.color = QColor(245, 30, 30)
        self.pen = QPen(self.color, 3, Qt.SolidLine)

        # ROI
        self.multipleROI = MultipleROI()
        self.roi = None
        self.lastPoint = None
        self.processedImage = None
        self.qpixmap = None
        self.imgArray = None
        self.delta = None

        # Process
        self.threshold = False
        self.thresholdMode = "Higher"
        self.cnts = None
        self.__connectEvents()

    def __connectEvents(self):
        """It enables Events"""
        self.Image.mousePressEvent = self.mousePressEvent
        self.Image.mouseReleaseEvent = self.mouseReleaseEvent
        self.Image.mouseMoveEvent = self.mouseMoveEvent
        self.Image.resizeEvent = self.resizeEvent
        self.Image.wheelEvent = self.wheelEvent
        self.seriesList.itemSelectionChanged.connect(self.chooseImage)
        self.roiList.itemSelectionChanged.connect(self.chooseROI)

    def updateThresholdState(self, threshold):
        """ It updates the Threshold state
        :param threshold:
        """
        self.threshold = threshold

    def hasROI(self):
        return self.roi is not None

    def chooseROI(self):
        item = self.roiList.currentItem()
        if item:
            name = item.text()
            self.roi = self.multipleROI.getROI(name=name)
            pixmap = self.getOriginalPixmap()
            if self.hasROI():
                self.roi.drawLine(pixmap)
            if self.hasImage():
                self.setPixmap(pixmap, fit=False)

    def renameROI(self):
        pass

    def addNewROI(self):
        name = "Slice {}".format(self.seriesList.currentRow() + 1)
        self.multipleROI.addNewROI(name)
        self.roiList.clear()
        self.roiList.addItems(self.multipleROI.getNamesList())

    def removeROI(self):
        name = self.roiList.currentItem().text()
        self.multipleROI.deleteROI(name=name)
        self.roiList.clear()
        self.roiList.addItems(self.multipleROI.getNamesList())


    def updateImageScaleFactors(self):
        """It updates the scale factor between Image Array and Scene Object"""
        w1, h1 = self.getArraySize()
        w2, h2 = self.getSceneSize()
        if w1 and w2:
            self.imgArrayWidthFactor = w1/w2
        else:
            self.imgArrayWidthFactor = 1
        if h1 and h2:
            self.imgArrayHeightFactor = h1/h2
        else:
            self.imgArrayHeightFactor = 1

        if self.hasROI():
            self.roi.updateScaleFactors(self.imgArrayWidthFactor, self.imgArrayWidthFactor)

        # print(" width: {:.4f} , height: {:.4f}".format(w2, h2))

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
                #print(" width: {:.4f} , height: {:.4f}".format(factor, factor))
            self.updateImageScaleFactors()

    def clear(self):
        """It clears the view"""
        self.clearImage()
        self.chooseImage(set=True, fit=False)
        if self.hasROI():
            self.roi.clear()

    def hasImage(self):
        """It verifies if there is an Image"""
        return self._pixmapHandle is not None

    def height(self):
        """It returns the QGraphicsView object height"""
        return self.Image.height()

    def width(self):
        """It returns the QGraphicsView object width"""
        return self.Image.width()

    def getSize(self):
        """It returns the QGraphicsView object size"""
        return self.width(), self.height()

    def clearImage(self):
        """It removes the current image pixmap from the scene if it exists"""
        if self.hasImage():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def getCurrentPixmap(self):
        """It returns the current pixmap"""
        if self.hasImage():
            return self._pixmapHandle.pixmap()
        return None

    def getCurrentImage(self):
        """It returns the current image on QImage format"""
        if self.hasImage():
            return self._pixmapHandle.pixmap().toImage()
        return None

    def getImageArray(self):
        """It returns the current Image array"""
        return self.imgArray

    def wheelEvent(self, event):
        """When the wheel mouse was moved or pressed do something
        :param event: QMouseEvent
        """
        oldPos = self.Image.mapToScene(event.pos())
        if self.hasImage():
            if event.angleDelta().y() > 0:
                self._zoom += 1
            else:
                self._zoom -= 1

            if self._zoom == 0:
                self.fitInView()
            else:
                if self._zoom > 0:
                    self.scale(self.zoomInFactor)
                else:
                    self.scale(self.zoomOutFactor)
            newPos = self.Image.mapToScene(event.pos())
            delta = newPos - oldPos
            self.delta = delta
            self.Image.translate(delta.x(), delta.y())

    def scale(self, factor):
        """It scales the QGraphicsView object appliying a transformation
        :param factor: float number
        """
        self.Image.scale(factor, factor)

    def resizeEvent(self, event):
        #self.fitInView()
        pass

    def mousePressEvent(self, event):
        """ When the mouse is pressed  do this
        :param event: QEvent object
        """
        if event.button() == Qt.LeftButton:
            if self.drag: self.Image.setDragMode(QGraphicsView.ScrollHandDrag)
            self.pressed = True
            if self.draw and self.hasROI():
                x, y = self.mapToScene(event.pos().x(), event.pos().y())
                self.roi.addPoint([x, y])
                pixmap = self.getOriginalPixmap()
                self.roi.drawLine(pixmap)
                self.setPixmap(pixmap, fit=False)

        # Do whatever was on the default mousePressEvent function of QGraphicsView object
        QGraphicsView.mousePressEvent(self.Image, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton: self.pressed = False
        x, y = self.mapToScene(event.pos().x(), event.pos().y())
        self.Image.setDragMode(QGraphicsView.NoDrag)
        if self.hasROI():
            self.roi.addPoint([x, y])

    def updatePositionLabel(self, x=0, y=0):
        """It updates the position label"""
        pos_str = "Position: {:.2f} , {:.2f}".format(x, y)
        self.positionLabel.setText(pos_str)

    def updateIntensityLabel(self, x=0, y=0):
        shape = self.imgArray.shape
        if shape[0] > x >= 0 and shape[1] > y >= 0:
            intensity_str = "Intensity: {:.2f}".format(self.imgArray[x][y])
            self.intensityLabel.setText(intensity_str)

    def mapToScene(self, x=0, y=0):
        point = self.Image.mapToScene(x, y)
        return point.x(), point.y()

    def getSceneSize(self):
        """It returns the scene"""
        return self.scene.width(), self.height()

    def mapSceneToArray(self, x, y):
        x = int(self.imgArrayWidthFactor*x)
        y = int(self.imgArrayHeightFactor*y)

        return x, y

    def mouseMoveEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        x, y = self.mapToScene(x, y)
        x_arr, y_arr = self.mapSceneToArray(x, y)
        self.updatePositionLabel(x_arr, y_arr)

        if self.hasImage():
            self.updateIntensityLabel(x_arr, y_arr)
            if self.pressed and self.draw and self.hasROI():
                pixmap = self.getOriginalPixmap()
                self.roi.addPoint([x, y])
                self.roi.drawLine(pixmap)
            else:
                pixmap = self.getCurrentPixmap()
            self.setPixmap(pixmap, fit=False)

        QGraphicsView.mouseMoveEvent(self.Image, event)

    def setPixmap(self, pixmap, fit=True):
        """Set pixmap
        :param pixmap: data
        :param fit: If It's True It will adjust the view
        """
        self._pixmapHandle.setPixmap(pixmap)
        if fit:
            self.fitInView()

    def getArraySize(self):
        """It returns the image array size"""
        if self.hasImage():
            return self.imgArray.shape[0], self.imgArray.shape[1]
        return None, None

    def getPixmapSize(self):
        """It returns the current pixmap size"""
        if self.hasImage():
            return self._pixmapHandle.pixmap().width(), self._pixmapHandle.pixmap().height()
        return None, None

    def zoomPlus(self):
        print("zoom ++")

    def zoomMinus(self):
        print("zoom --")

    def resetZoom(self):
        """It resets the zoom"""
        self._zoom = 0
        if self.hasImage():
            self.fitInView()

    def setDraw(self, draw=True):
        """It enables or disable draw functionality
        :param draw: draw flag, if it's True enables this function
        """
        self.draw = draw
        if draw:
            self.Image.setCursor(QtCore.Qt.CrossCursor)
        else:
            self.Image.setCursor(QtCore.Qt.ArrowCursor)

    def setDrag(self, drag=False):
        """It enables or disable drag functionality
        :param drag: drag flag, if it's True enables this function
        """
        self.drag = drag
        if drag:
            self.Image.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.Image.setDragMode(QGraphicsView.NoDrag)

    def updateSliceNoLabel(self):
        """It updates the value of the Slice Number(No) Label"""
        slice_str = "Slice No.: {} / {}".format(self.seriesList.currentRow() + 1, len(self.filesList))
        self.sliceNoLabel.setText(slice_str)

    def chooseImage(self, set=True, fit=True):
        """Choose a Image from the list of images"""

        item = self.seriesList.currentItem()
        if item:
            img = self.readDicomImage(self.root + "/" + item.text())
            self.imgArray = img
            self.originalPixmap = self.arrayToPixmap(img)
            if set:
                self.setImage(img, fit=fit)
            self.updateSliceNoLabel()
        else:
            img = None

    def getOriginalPixmap(self):
        return QPixmap(self.originalPixmap)

    def setImage(self, img, fit=True):
        """Show image in the Graphic scene widget
        :param img: image Array
        :param fit: If It's True the GraphicsView will automatic fit the view
        """
        pixmap = self.arrayToPixmap(img)
        if pixmap:
            if self.hasImage():
                self._pixmapHandle.setPixmap(pixmap)
            else:
                self._pixmapHandle = self.scene.addPixmap(pixmap)
        self.Image.setSceneRect(QRectF(pixmap.rect()))
        if fit:
            self.fitInView()

    def arrayToPixmap(self, img):
        """Numpy array to QPixmap
        :param img: image array
        :return pixmap: image on QPixmap format
        """
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        w, h = self.Image.width(), self.Image.height()
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        backlash = self.Image.lineWidth() * 2
        pixmap = QPixmap.fromImage(img).scaled(w - backlash, h - backlash, Qt.IgnoreAspectRatio)
        return pixmap

    @staticmethod
    def linearConvert(img):
        """It applies a linear conversion to an image array
        :param img: image array
        :return new_img: image array scaled
        """
        factor = 255 / (np.max(img) - np.min(img))
        new_img = factor * img - (factor * np.min(img))
        return new_img

    def readDicomImage(self, fname, copy=False):
        """It returns a dicom image
        :param fname: file name
        """
        dcm = pydicom.dcmread(fname)
        img = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
        img = self.linearConvert(img).astype(np.uint8)
        return img if copy else img.copy()

    def loadDicomSeries(self, path):
        """Load a list of dicom Files coming from a path
        :param path: files path
        """
        for root, _, files in os.walk(path):
            self.root = root
            self.filesList = sorted(files)
            self.seriesList.addItems(self.filesList)

    def updateThreshold(self, threshold=100, mode="Higher"):
        if self.cnts is not None:
            self.thresholdMode = mode
            out = draw_roi(self.getImageArray(), self.cnts, threshold=threshold, mode=mode)
            self.setImage(out, fit=False)

    def processRoi(self):
        """Process ROI"""
        if self.hasROI():
            cnts = self.roi.getContour(scale=True, wf=self.imgArrayWidthFactor, hf=self.imgArrayHeightFactor)
            self.cnts = cnts
            out = draw_roi(self.getImageArray(), cnts)
            #np.save("conturstest.npy", cnts)
            self.setImage(out)
            areaTotal = out.shape[0]*out.shape[1]
            area = cv2.contourArea(cnts)
            mean = np.mean(out)*areaTotal/area
            mean_str = "Mean: {:.2f} ".format(mean)
            self.meanLabel.setText(mean_str)
            self.pixelNumberLabel.setText("Pixel Number: " + str(int(area)))
            self.areaVolLabel.setText("Area: {} mm2, Vol: NaN mm3".format(int(area)))
            self.roi.clear()
