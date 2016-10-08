# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(572, 469)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lstreaders = QtWidgets.QListWidget(self.centralWidget)
        self.lstreaders.setObjectName("lstreaders")
        self.horizontalLayout.addWidget(self.lstreaders)
        self.lstwritters = QtWidgets.QListWidget(self.centralWidget)
        self.lstwritters.setObjectName("lstwritters")
        self.horizontalLayout.addWidget(self.lstwritters)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txtlog = QtWidgets.QTextEdit(self.centralWidget)
        self.txtlog.setObjectName("txtlog")
        self.verticalLayout.addWidget(self.txtlog)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 572, 19))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menuBar)
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/refresh.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRun = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/run.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun.setIcon(icon1)
        self.actionRun.setObjectName("actionRun")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon2)
        self.actionExit.setObjectName("actionExit")
        self.mainToolBar.addAction(self.actionRefresh)
        self.mainToolBar.addAction(self.actionRun)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionExit)
        self.menu_File.addAction(self.actionRefresh)
        self.menu_File.addAction(self.actionRun)
        self.menu_File.addAction(self.actionExit)
        self.menuBar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Format Converter"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.actionExit.setText(_translate("MainWindow", "exit"))

#import icons_rc
