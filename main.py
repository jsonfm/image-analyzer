import sys
from gui.components.viewer import Viewer
#from gui.components.multipleROI import MultipleROI
from loaders.images import ImageLoader
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import numpy as np 
import time

src_c = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et2w_tse_clear_coronal.nii.gz"
src_s = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_sagital.nii.gz"
src_a = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_axial.nii.gz"

# imageSagital = ImageLoader(src_s).load_array()[:,:,1]
# imageCoronal = ImageLoader(src_c).load_array()[:,1,:]
# imageAxial = ImageLoader(src_a).load_array()[1,:,:]

image = ImageLoader(src_c).load_array()
print(image.shape)
class App(QMainWindow):
    """This an App for analyze medical images"""
    def __init__(self):
        super().__init__()
        uic.loadUi('./gui/main.ui', self)
        self.__configureViewers()
        self.__configureMenuBar()
        self.__configureCursor()
        self.__configureToolBar()
        self.__configureSegmentationTools()
        self.__configureImagesLayoutButtons()
        self.extractFeaturesBtn.clicked.connect(lambda: self.updateViewers(1, 1, 2))

    def __configureViewers(self):
        self.viewer1 = Viewer(self.image1)
        self.viewer2 = Viewer(self.image2)
        self.viewer3 = Viewer(self.image3)
        self.zoomResetBtn1.clicked.connect(lambda: self.viewer1.fitInView())
        self.zoomResetBtn2.clicked.connect(lambda: self.viewer2.fitInView())
        self.zoomResetBtn3.clicked.connect(lambda: self.viewer3.fitInView())
        self.imageScroll1.setMaximum(image.shape[0] - 1)
        self.imageScroll2.setMaximum(image.shape[1] - 1)
        self.imageScroll3.setMaximum(image.shape[2] - 1)
        self.imageScroll1.valueChanged.connect(lambda: self.updateSlide(1))
        self.imageScroll2.valueChanged.connect(lambda: self.updateSlide(2))
        self.imageScroll3.valueChanged.connect(lambda: self.updateSlide(3))

    def updateSlide(self, _id):
        i = self.imageScroll1.value()
        j = self.imageScroll2.value()
        k = self.imageScroll3.value()
        if _id == 1:
            print("Update image 1: ", i)
        elif _id == 2:
            print("Update image21: ", j)
        elif _id == 3:
            print("Update image 3: ", k)
        else: raise("Not valid id for slider!")
        self.updateViewers(i, j, k)

    def __configureMenuBar(self):
        self.actionOpenFile.triggered.connect(self.openFile)

    def __configureCursor(self):
        self.cursorBtn.clicked.connect(lambda: self.updateCursorMode('draw'))
        self.dragBtn.clicked.connect(lambda: self.updateCursorMode('drag'))

    def __configureSegmentationTools(self):
        #self.multipleROI = MultipleROI()
        self.roiLabel.currentTextChanged.connect(lambda: self.multipleROI.use(self.roiLabel.currentText()))

    def __configureToolBar(self):
        # self.cursorBtn.clicked.connect()
        pass

    def __configureImagesLayoutButtons(self):
        self.imageLayoutBtn1.clicked.connect(lambda: self.organizeImagesLayout(1, self.imageLayoutBtn1.isChecked()))
        self.imageLayoutBtn2.clicked.connect(lambda: self.organizeImagesLayout(2, self.imageLayoutBtn2.isChecked()))
        self.imageLayoutBtn3.clicked.connect(lambda: self.organizeImagesLayout(3, self.imageLayoutBtn3.isChecked()))    

    def updateViewers(self, i=1, j=1, k=1):
        self.viewer1.setImage(image[i, : , :])
        self.viewer2.setImage(image[:, j, :])
        self.viewer3.setImage(image[:, :, k])
        # self.viewer1.setImage(imageCoronal)
        # self.viewer2.setImage(imageAxial)
        # self.viewer3.setImage(imageSagital)
        pass

    def updateCursorMode(self, mode=''):
        if mode == 'draw':
            draw, drag = True, False
        if mode == 'drag':
            draw, drag = False, True
        self.dragBtn.setChecked(drag)
        self.cursorBtn.setChecked(draw)
        for i in range(1, 4): getattr(self, f"viewer{i}").toggleDragMode(drag)

    def openFile(self):
        dlg = QFileDialog()
        filesFilter = "NII(*.nii *.nii.gz);; DICOM(*.dic *.dcm) ;; JPEG(*.jpg *.jpeg);; TIFF(*.tiff);; All files(*.*)"
        filepath = dlg.getOpenFileName(self, "Choose a directory", "", filesFilter)
        print("Openning file: ", filepath)

    def organizeImagesLayout(self, indexLayout=1, hide=False):
        """It hides or shows every elements of layout except for the current index elements.
            indexLayout (int): current index of the element who emits the event
            hide (bool): hide or show every other items different from the current element
        """
        for i in range(1, 5):
            if i != indexLayout: 
                getattr(self, f"imageContainer{i}").setHidden(hide)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec_())