import sys
from gui.components.viewer import Viewer
#from gui.components.multipleROI import MultipleROI
from dataloaders.images import ImageLoader
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import numpy as np 
import time

src_c = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et2w_tse_clear_coronal.nii.gz"
src_s = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_sagital.nii.gz"
src_a = "/home/jason/Documents/TESIS/image-analyzer/data/dataset-nifti/sclerosis/Patient - 10196/encefalo/et1w_se_clear_axial.nii.gz"

imageSagital = ImageLoader(src_s).load_array()[:,:,1]
imageCoronal = ImageLoader(src_c).load_array()[:,1,:]
imageAxial = ImageLoader(src_a).load_array()[1,:,:]



class App(QMainWindow):
    """This an App for analyze medical images"""
    def __init__(self):
        super().__init__()
        uic.loadUi('./gui/main.ui', self)
        self.viewer1 = Viewer(self.image1)
        self.viewer2 = Viewer(self.image2)
        self.viewer3 = Viewer(self.image3)
        self.extractFeaturesBtn.clicked.connect(self.updateViewers)
        self.__configureMenuBar()
        self.__configureCursor()
        self.__configureSegmentationTools()
        self.__configureImagesLayoutButtons()
    
    def updateViewers(self):
        print("Setting")
        self.viewer1.setImage(imageCoronal)
        self.viewer2.setImage(imageAxial)
        self.viewer3.setImage(imageSagital)

    def __configureMenuBar(self):
        pass

    def __configureCursor(self):
        self.cursorBtn.clicked.connect(self.updateCursorMode)
        self.dragBtn.clicked.connect(self.updateCursorMode)

    def __configureSegmentationTools(self):
        #self.multipleROI = MultipleROI()
        self.roiLabel.currentTextChanged.connect(lambda: self.multipleROI.use(self.roiLabel.currentText()))

    def updateCursorMode(self):
        print("Updating: cursor")

    def __configureImagesLayoutButtons(self):
        self.imageLayoutBtn1.clicked.connect(lambda: self.organizeImagesLayout(1, self.imageLayoutBtn1.isChecked()))
        self.imageLayoutBtn2.clicked.connect(lambda: self.organizeImagesLayout(2, self.imageLayoutBtn2.isChecked()))
        self.imageLayoutBtn3.clicked.connect(lambda: self.organizeImagesLayout(3, self.imageLayoutBtn3.isChecked()))    

    def organizeImagesLayout(self, indexLayout=1, hide=False):
        """It hides or shows every elements of layout except for the current index elements.
            indexLayout (int): current index of the element who emits the event
            hide (bool): hide or show every other items different from the current element
        """
        for i in range(1, 5):
            if i != indexLayout: getattr(self, f"imageContainer{i}").setHidden(hide)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec_())