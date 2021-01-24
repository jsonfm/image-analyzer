import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
from viewer import Viewer


class App(QMainWindow):
    """This an App for analyze medical images"""

    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)
        self.viewer = Viewer(self.Image, self.seriesView, self.positionLabel, self.intensityLabel, self.sliceNoLabel,
                             self.meanLabel, self.pixelNumberLabel, self.areaVolLabel, self.roiList)
        self.__connectEvents()

    def __connectEvents(self):
        """It enables GUI Events"""
        self.openBtn.clicked.connect(self.openPath)
        self.zoomPlusBtn.clicked.connect(self.viewer.zoomPlus)
        self.zoomMinusBtn.clicked.connect(self.viewer.zoomMinus)
        self.resetZoomBtn.clicked.connect(self.viewer.resetZoom)
        self.clearBtn.clicked.connect(self.viewer.clear)
        self.process.clicked.connect(self.viewer.processRoi)
        self.drawBtn.toggled.connect(lambda: self.viewer.setDraw(self.drawBtn.isChecked()))
        self.dragBtn.toggled.connect(lambda: self.viewer.setDrag(self.dragBtn.isChecked()))
        # ROI
        self.newBtn.clicked.connect(self.viewer.addNewROI)
        self.removeBtn.clicked.connect(self.viewer.removeROI)
        self.renameBtn.clicked.connect(self.viewer.renameROI)

        # Process
        self.thresholdCheck.clicked.connect(lambda: self.viewer.updateThresholdState(self.thresholdCheck.isChecked()))
        self.thresholdSlider.valueChanged.connect(self.updateThreshold)
        self.thresholdSelector.currentTextChanged.connect(self.updateThresholdMode)

    def updateThreshold(self):
        """It updates slider"""
        threshold = self.thresholdSlider.value()
        mode = self.thresholdSelector.currentText()
        self.viewer.updateThreshold(threshold=threshold, mode=mode)
        self.thresholdEdit.setText(str(threshold))

    def updateThresholdMode(self):
        threshold = self.thresholdSlider.value()
        mode = self.thresholdSelector.currentText()
        self.viewer.updateThreshold(threshold=threshold, mode=mode)


    def openPath(self):
        """It allows to read files directory"""
        dlg = QFileDialog()
        path = dlg.getExistingDirectory(self, "Choose a directory")
        if path:
            self.viewer.loadDicomSeries(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec_())
