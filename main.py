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


class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow() 
		self.ui.setupUi(self)
		self.viewer = Viewer(self.ui.Image, self.ui.seriesView)
		self.ui.openBtn.clicked.connect(self.open_path)
		self.ui.views.hide()
		self.showViews = False
		self.__connectEvents()

	def __connectEvents(self):
		self.ui.zoom_plus.clicked.connect(self.viewer.zoomPlus)
		self.ui.zoom_minus.clicked.connect(self.viewer.zoomMinus)
		self.ui.reset_zoom.clicked.connect(self.viewer.resetZoom)
		self.ui.toggle_line.toggled.connect(self.action_line)
		self.ui.toggle_move.toggled.connect(self.action_move)
		self.ui.clear_all.clicked.connect(self.action_clear)
		self.ui.viewsBtn.clicked.connect(self.action_views)
		self.ui.process.clicked.connect(self.action_process)

	def action_views(self):
		self.showViews = not self.showViews
		self.ui.views.setVisible(self.showViews)
		
	def action_process(self):
		self.viewer.processRoi()

	def action_clear(self):
		self.viewer.clear()

	def action_line(self):
		draw = self.ui.toggle_line.isChecked()
		self.ui.toggle_move.setChecked(not draw)
		self.viewer.setDraw(draw)
		self.viewer.setDrag(not draw)

	def action_move(self):
		drag = self.ui.toggle_move.isChecked()
		self.ui.toggle_line.setChecked(not drag)
		self.viewer.setDraw(not drag)
		self.viewer.setDrag(drag)
		
	def open_path(self):
		dlg = QFileDialog()
		path = dlg.getExistingDirectory(self, "Choose a directory")
		#path = dlg.getOpenFileName(self, "Seleccione un archivo")
		if path: 
			print(path[0])
			self.viewer.loadDicomSeries(path)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = App()
	w.show()	
	sys.exit(app.exec_())
