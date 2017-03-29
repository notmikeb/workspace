# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'btdaycase.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(33, 0))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.list1 = QtGui.QListWidget(self.widget)
        self.list1.setMinimumSize(QtCore.QSize(44, 44))
        self.list1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.list1.setFont(font)
        self.list1.setModelColumn(0)
        self.list1.setObjectName(_fromUtf8("list1"))
        self.gridLayout.addWidget(self.list1, 0, 0, 1, 1)
        self.tree1 = QtGui.QTreeWidget(self.widget)
        self.tree1.setMinimumSize(QtCore.QSize(44, 44))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tree1.setFont(font)
        self.tree1.setObjectName(_fromUtf8("tree1"))
        self.tree1.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout.addWidget(self.tree1, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_2 = QtGui.QWidget(self.groupBox)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tbnUp = QtGui.QToolButton(self.widget_2)
        self.tbnUp.setMinimumSize(QtCore.QSize(0, 0))
        self.tbnUp.setObjectName(_fromUtf8("tbnUp"))
        self.horizontalLayout_3.addWidget(self.tbnUp)
        self.tbnDown = QtGui.QToolButton(self.widget_2)
        self.tbnDown.setObjectName(_fromUtf8("tbnDown"))
        self.horizontalLayout_3.addWidget(self.tbnDown)
        self.tbnLeft = QtGui.QToolButton(self.widget_2)
        self.tbnLeft.setObjectName(_fromUtf8("tbnLeft"))
        self.horizontalLayout_3.addWidget(self.tbnLeft)
        self.tbnRight = QtGui.QToolButton(self.widget_2)
        self.tbnRight.setObjectName(_fromUtf8("tbnRight"))
        self.horizontalLayout_3.addWidget(self.tbnRight)
        self.tbnAdd = QtGui.QToolButton(self.widget_2)
        self.tbnAdd.setObjectName(_fromUtf8("tbnAdd"))
        self.horizontalLayout_3.addWidget(self.tbnAdd)
        self.tbnRemove = QtGui.QToolButton(self.widget_2)
        self.tbnRemove.setObjectName(_fromUtf8("tbnRemove"))
        self.horizontalLayout_3.addWidget(self.tbnRemove)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget_2)
        self.tree2 = QtGui.QTreeWidget(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tree2.setFont(font)
        self.tree2.setObjectName(_fromUtf8("tree2"))
        self.tree2.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.tree2)
        self.horizontalLayout.addWidget(self.groupBox)
        self.tbl1 = QtGui.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tbl1.setFont(font)
        self.tbl1.setObjectName(_fromUtf8("tbl1"))
        self.tbl1.setColumnCount(0)
        self.tbl1.setRowCount(0)
        self.horizontalLayout.addWidget(self.tbl1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.tbnUp.setText(_translate("MainWindow", "...", None))
        self.tbnDown.setText(_translate("MainWindow", "...", None))
        self.tbnLeft.setText(_translate("MainWindow", "...", None))
        self.tbnRight.setText(_translate("MainWindow", "...", None))
        self.tbnAdd.setText(_translate("MainWindow", "...", None))
        self.tbnRemove.setText(_translate("MainWindow", "...", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))

