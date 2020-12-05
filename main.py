import os
import sys
from GUI import *
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QFileDialog
from concurrent.futures import ThreadPoolExecutor
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QStringListModel
import sys, os, threading, re
import numpy as np
from Viewer import Viewer

#/home/jason/Documentos/Python/TESIS/anonymize/Anonymized - 117/Encefalo/eFLAIR_longTR - 602/

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow() 
		self.ui.setupUi(self)

		self.viewer = Viewer(self.ui.Image, self.ui.seriesView)

		self.ui.openBtn.clicked.connect(self.open_path)

		self.__connectEvents()

	def __connectEvents(self):
		self.ui.zoom_plus.clicked.connect(self.viewer.zoomPlus)
		self.ui.zoom_minus.clicked.connect(self.viewer.zoomMinus)
		self.ui.reset_zoom.clicked.connect(self.viewer.resetZoom)
		self.ui.toggle_line.toggled.connect(self.action_line)
		self.ui.toggle_move.toggled.connect(self.action_move)

	def action_line(self):
		draw = self.ui.toggle_line.isChecked()
		self.viewer.setDraw(draw)

	def action_move(self):
		drag = self.ui.toggle_move.isChecked()
		self.viewer.setDrag(drag)
		
	def open_path(self):
		dlg = QFileDialog()
		path = dlg.getExistingDirectory(self, "Choose a directory")
		#path = dlg.getOpenFileName(self, "Seleccione un archivo")
		if path: 
			#self.src = path
			print(path[0])
			#self.viewer.load_dicom_image(path[0])
			self.viewer.loadDicomSeries(path)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = App()
	w.show()	
	sys.exit(app.exec_())
