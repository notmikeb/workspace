# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cpuprogress.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainUiWindow(object):
    def setupUi(self, MainUiWindow):
        MainUiWindow.setObjectName(_fromUtf8("MainUiWindow"))
        MainUiWindow.resize(601, 113)
        self.centralwidget = QtGui.QWidget(MainUiWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.progressBar_2 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName(_fromUtf8("progressBar_2"))
        self.horizontalLayout_2.addWidget(self.progressBar_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainUiWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainUiWindow)
        QtCore.QMetaObject.connectSlotsByName(MainUiWindow)

    def retranslateUi(self, MainUiWindow):
        MainUiWindow.setWindowTitle(_translate("MainUiWindow", "MainWindow", None))
        self.label.setText(_translate("MainUiWindow", "CPU Usage", None))
        self.label_2.setText(_translate("MainUiWindow", "Usage", None))

