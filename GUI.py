# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(995, 674)
        MainWindow.setStyleSheet("QMainWindow{\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"#centralwidget {\n"
"background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QGraphicsView{\n"
"background-color:rgb(0, 0, 0);\n"
"}\n"
"\n"
"#tabWidget{\n"
"background-color:rgb(0,0,0);\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"  background: rgb(22, 24, 30);\n"
"  color: white;\n"
"  padding: 10px;\n"
"\n"
" }\n"
"QTabWidget::pane { \n"
"   border: 1px solid rgb(5, 75, 87);\n"
"    background: rgb(0, 0, 0);\n"
"}\n"
"\n"
" QTabBar::tab:selected {\n"
"  border: 2px solid rgb(5, 75, 87);\n"
" }\n"
"\n"
"#seriesView{\n"
"background-color:rgb(18, 18, 18);\n"
"color:rgb(136, 138, 133);\n"
"}\n"
"\n"
"#console {\n"
"background-color:rgb(18, 18, 18);\n"
"}\n"
"\n"
"/*Labels*/\n"
"#titleLabel{\n"
"color:rgb(186, 189, 182)\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.openBtn = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openBtn.setIcon(icon)
        self.openBtn.setIconSize(QtCore.QSize(20, 20))
        self.openBtn.setObjectName("openBtn")
        self.horizontalLayout_8.addWidget(self.openBtn)
        self.viewsBtn = QtWidgets.QToolButton(self.centralwidget)
        self.viewsBtn.setObjectName("viewsBtn")
        self.horizontalLayout_8.addWidget(self.viewsBtn)
        self.save_im = QtWidgets.QToolButton(self.centralwidget)
        self.save_im.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_im.setToolTip("Save Image")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../PyQt-Image-Viewer-master/icons/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_im.setIcon(icon1)
        self.save_im.setIconSize(QtCore.QSize(20, 20))
        self.save_im.setObjectName("save_im")
        self.horizontalLayout_8.addWidget(self.save_im)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.seriesView = QtWidgets.QListWidget(self.widget)
        self.seriesView.setObjectName("seriesView")
        self.verticalLayout_4.addWidget(self.seriesView)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.process = QtWidgets.QPushButton(self.widget)
        self.process.setObjectName("process")
        self.horizontalLayout_4.addWidget(self.process)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.horizontalLayout_6.addWidget(self.widget)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_6.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.toggle_line = QtWidgets.QToolButton(self.centralwidget)
        self.toggle_line.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toggle_line.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggle_line.setIcon(icon2)
        self.toggle_line.setIconSize(QtCore.QSize(20, 20))
        self.toggle_line.setCheckable(True)
        self.toggle_line.setObjectName("toggle_line")
        self.verticalLayout.addWidget(self.toggle_line)
        self.zoom_plus = QtWidgets.QToolButton(self.centralwidget)
        self.zoom_plus.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoom_plus.setIcon(icon3)
        self.zoom_plus.setIconSize(QtCore.QSize(20, 20))
        self.zoom_plus.setObjectName("zoom_plus")
        self.verticalLayout.addWidget(self.zoom_plus)
        self.zoom_minus = QtWidgets.QToolButton(self.centralwidget)
        self.zoom_minus.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoom_minus.setIcon(icon4)
        self.zoom_minus.setIconSize(QtCore.QSize(20, 20))
        self.zoom_minus.setObjectName("zoom_minus")
        self.verticalLayout.addWidget(self.zoom_minus)
        self.reset_zoom = QtWidgets.QToolButton(self.centralwidget)
        self.reset_zoom.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/enlarge2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_zoom.setIcon(icon5)
        self.reset_zoom.setIconSize(QtCore.QSize(20, 20))
        self.reset_zoom.setObjectName("reset_zoom")
        self.verticalLayout.addWidget(self.reset_zoom)
        self.toggle_rect = QtWidgets.QToolButton(self.centralwidget)
        self.toggle_rect.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/rectangle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggle_rect.setIcon(icon6)
        self.toggle_rect.setIconSize(QtCore.QSize(20, 20))
        self.toggle_rect.setCheckable(True)
        self.toggle_rect.setObjectName("toggle_rect")
        self.verticalLayout.addWidget(self.toggle_rect)
        self.toggle_move = QtWidgets.QToolButton(self.centralwidget)
        self.toggle_move.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toggle_move.setAutoFillBackground(False)
        self.toggle_move.setStyleSheet("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/move.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggle_move.setIcon(icon7)
        self.toggle_move.setIconSize(QtCore.QSize(20, 20))
        self.toggle_move.setCheckable(True)
        self.toggle_move.setChecked(False)
        self.toggle_move.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toggle_move.setAutoRaise(False)
        self.toggle_move.setObjectName("toggle_move")
        self.verticalLayout.addWidget(self.toggle_move)
        self.undo = QtWidgets.QToolButton(self.centralwidget)
        self.undo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/undo2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undo.setIcon(icon8)
        self.undo.setIconSize(QtCore.QSize(20, 20))
        self.undo.setObjectName("undo")
        self.verticalLayout.addWidget(self.undo)
        self.redo = QtWidgets.QToolButton(self.centralwidget)
        self.redo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../PyQt-Image-Viewer-master/icons/redo2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redo.setIcon(icon9)
        self.redo.setIconSize(QtCore.QSize(20, 20))
        self.redo.setObjectName("redo")
        self.verticalLayout.addWidget(self.redo)
        self.clear_all = QtWidgets.QToolButton(self.centralwidget)
        self.clear_all.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("../PyQt-Image-Viewer-master/icons/loop2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_all.setIcon(icon10)
        self.clear_all.setIconSize(QtCore.QSize(20, 20))
        self.clear_all.setObjectName("clear_all")
        self.verticalLayout.addWidget(self.clear_all)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.Image = QtWidgets.QGraphicsView(self.centralwidget)
        self.Image.setObjectName("Image")
        self.horizontalLayout_7.addWidget(self.Image)
        self.views = QtWidgets.QWidget(self.centralwidget)
        self.views.setObjectName("views")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.views)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Image_2 = QtWidgets.QGraphicsView(self.views)
        self.Image_2.setObjectName("Image_2")
        self.verticalLayout_2.addWidget(self.Image_2)
        self.Image_3 = QtWidgets.QGraphicsView(self.views)
        self.Image_3.setObjectName("Image_3")
        self.verticalLayout_2.addWidget(self.Image_3)
        self.graphicsView = QtWidgets.QGraphicsView(self.views)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.horizontalLayout_7.addWidget(self.views)
        self.horizontalLayout_7.setStretch(0, 3)
        self.horizontalLayout_7.setStretch(1, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.imageSlider = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageSlider.sizePolicy().hasHeightForWidth())
        self.imageSlider.setSizePolicy(sizePolicy)
        self.imageSlider.setOrientation(QtCore.Qt.Horizontal)
        self.imageSlider.setObjectName("imageSlider")
        self.horizontalLayout_3.addWidget(self.imageSlider)
        self.horizontalLayout_3.setStretch(0, 8)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2.setStretch(1, 4)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6.setStretch(0, 2)
        self.horizontalLayout_6.setStretch(2, 7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 995, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ImageAnalyzer"))
        self.openBtn.setText(_translate("MainWindow", "..."))
        self.viewsBtn.setText(_translate("MainWindow", "..."))
        self.save_im.setText(_translate("MainWindow", "..."))
        self.process.setText(_translate("MainWindow", "Process ROI"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.toggle_line.setToolTip(_translate("MainWindow", "Mark line"))
        self.toggle_line.setText(_translate("MainWindow", "..."))
        self.zoom_plus.setText(_translate("MainWindow", "+"))
        self.zoom_minus.setText(_translate("MainWindow", "-"))
        self.reset_zoom.setToolTip(_translate("MainWindow", "Fit Image to Canvas"))
        self.reset_zoom.setText(_translate("MainWindow", "..."))
        self.toggle_rect.setToolTip(_translate("MainWindow", "Mark rectangular surface"))
        self.toggle_rect.setText(_translate("MainWindow", "..."))
        self.toggle_move.setToolTip(_translate("MainWindow", "Move Image"))
        self.toggle_move.setText(_translate("MainWindow", "..."))
        self.undo.setToolTip(_translate("MainWindow", "Undo"))
        self.undo.setText(_translate("MainWindow", "..."))
        self.redo.setToolTip(_translate("MainWindow", "Redo"))
        self.redo.setText(_translate("MainWindow", "..."))
        self.clear_all.setToolTip(_translate("MainWindow", "Clear All"))
        self.clear_all.setText(_translate("MainWindow", "..."))


