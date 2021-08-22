from PyQt5.QtGui import QBrush, QPixmap, QImage, QPainter, QPen, QColor, QFont, QBrush
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF, QPointF
import cv2

def arrayToPixmap(img, w, h, linewidth, swap=False):
    """Numpy array to Q_pixmapHandle
    :param img: image array
    :return _pixmapHandle: image on Q_pixmapHandle format
    """
    if img.dtype == "":
        pass

    qformat = QImage.Format_Indexed8
    if len(img.shape) == 3:
        if img.shape[2] == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888
    # w, h = self.Image.width(), self.Image.height()
    img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
    if swap:
        img = img.rgbSwapped()
    # backlash = self.Image.lineWidth() * 2
    backlash = linewidth*2
    _pixmapHandle = QPixmap.fromImage(img).scaled(w - backlash, h - backlash)
    return _pixmapHandle


def normalizeArray(image, a=0, b=65535, dtype='uint16'):
    image_min = image.min()
    image_max = image.max()
    _max = (b - a) * (1.0/(image_max - image_min))
    _min = b - _max * image_max
    new = (_max * image + _min).astype(dtype)
    return new


class Viewer:
    #ImageClicked = QtCore.pyqtSignal(QtCore.QPoint)
    def __init__(self,qgraphicsview):
        #super(Viewer, self).__init__(parent)
        self._image = qgraphicsview
        self._image.setDragMode(QGraphicsView.ScrollHandDrag)
        self._scene = QGraphicsScene()
        self._image.setScene(self._scene)
        self._pixmapHandle = None
        self._zoom = 0
        self._image.setTransformationAnchor(QGraphicsView.NoAnchor)
        self._image.setResizeAnchor(QGraphicsView.NoAnchor)
        self.__configureEvents()
        self.drag = True
        self.toggleDragMode(self.drag)
    
    def __configureEvents(self):
        self._image.resizeEvent = self.resizeEvent
        self._image.wheelEvent = self.wheelEvent
        self._image.mouseMoveEvent = self.mouseMoveEvent

    def scene(self):
        return self._image.scene()

    def hasImage(self):
        return self._pixmapHandle is not None

    def width(self) -> int:
        return self._image.width()
    
    def height(self) -> int:
        return self._image.height()
    
    def lineWidth(self) -> int:
        return self._image.lineWidth()
    
    def size(self):
        return self._image.size()
    
    def viewport(self):
        return self._image.viewport()
    
    def transform(self):
        return self._image.transform()
    
    def geometry(self):
        return self._image.geometry()
    
    def scale(self,*args):
        self._image.scale(*args)
    
    def setScene(self, *args):
        self._image.setScene(*args)
    
    def setSceneRect(self, *args):
        self._image.setSceneRect(*args)

    def mapToScene(self, *args):
        return self._image.mapToScene(*args)
    
    def dragMode(self):
        return self._image.dragMode()
    
    def setDragMode(self, *args):
        self._image.setDragMode(*args)
    
    def translate(self, *args):
        self._image.translate(*args)

    def fitInView(self, scale=True):
        if self.hasImage():
            rect = QtCore.QRectF(self._pixmapHandle.pixmap().rect())
            if not rect.isNull():
                self.setSceneRect(rect)
                if self.hasImage():
                    unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                    self.scale(1 / unity.width(), 1 / unity.height())
                    viewrect = self.viewport().rect()
                    scenerect = self.transform().mapRect(rect)
                    factor = min(viewrect.width() / scenerect.width(),
                                viewrect.height() / scenerect.height())
                    self.scale(factor, factor)
                self._zoom = 0
    
    def parseImageArray(self, image, dtype='uint8'):
        if dtype == 'uint8':
            a, b = 0, 255
            dtype = cv2.CV_8U

        elif dtype == 'uint16':
            a, b = 0, 65535
            dtype = cv2.CV_16U
        else:
            raise('Not valid type of image, please try with: uint8 or uint 16')
        image = cv2.normalize(image, None, a, b, cv2.NORM_MINMAX, dtype)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        return image 
    
    def arrayToPixmap(self, image, dtype='uint8'):
        if dtype == 'uint8':
            qformat = QImage.Format_RGB888
        elif dtype == 'uint16':
            qformat = QImage.Format__RGB888

        image = self.parseImageArray(image, dtype=dtype)
        w, h, ch = image.shape
        qtImage = QImage(image.data, w, h, ch * w, qformat)
        pixmap = QPixmap.fromImage(qtImage)
        return pixmap

    def setImage(self, img=None, a=False):      
        self._zoom = 0
        w, h, linewidth = self.width(), self.height(), self.lineWidth()
        print(f"SET: {self.size()} || VIEW: {self.viewport().size()} || GEO: {self.geometry().size()}")
        pixmap = self.arrayToPixmap(img, dtype='uint8')
        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self._scene.addPixmap(pixmap)
        self._image.setSceneRect(QRectF(pixmap.rect()))
        self.fitInView()

    def wheelEvent(self, event):
        oldPos = self.mapToScene(event.pos())
        if self.hasImage() and self.drag:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.6
                self._zoom -= 1

            if self._zoom > 0:
                self.scale(factor, factor)
                
            elif self._zoom <= 0:
                self.fitInView()
            else:
                self._zoom = 0
            newPos = self.mapToScene(event.pos())
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

    def toggleDragMode(self, drag=False):
        self.drag = drag
        if not drag:
            self.setDragMode(QGraphicsView.NoDrag)
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._pixmapHandle.isUnderMouse():
            print(self.scene().width(), self.scene().height())
            self.ImageClicked.emit(self._image.mapToScene(event.pos()).toPoint())
        #QGraphicsView.mousePressEvent(self.Image, event)

    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        x1, y1 = event.pos().x(), event.pos().y()
        x2, y2 = scenePos.x(), scenePos.y()

        if self.hasImage():
            print(f"P1: {x1:.1f} , {y1:.1f}")
            print(f"P2: {x2:.1f} , {y2:.1f}")
        QGraphicsView.mouseMoveEvent(self._image, event)

    def showEvent(self, event):
        if self.hasImage():
            self.fitInView()
        #QGraphicsView.showEvent(self._image, event)

    def resizeEvent(self, event):
        pass
        print(f"RESIZE -> ,SET: {self.size()} || VIEW: {self.viewport().size()} || GEO: {self.geometry().size()}")
        # if self.hasImage():
        #     if not self._pixmapHandle.pixmap().isNull():
        #         self.fitInView()
        # QGraphicsView.resizeEvent(self._image, event)