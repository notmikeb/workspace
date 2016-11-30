import PyQt4
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from os import path
import os

# use a listwidget and listwidgetitem to add extra data
# support contextmenu

class Window(QListWidget):
    def __init__(self):
        QListView.__init__(self)
        for root, dirs, files in os.walk("c:\\MinGW"):
            for f in files:
                a = QListWidgetItem(f, self)
                a.setData(100, QVariant(QString( os.path.join(root, f) )))

        a = QListWidgetItem("xyz", self)
        b = QListWidgetItem("abc")
        self.addItem(b)
        a.setData(100, QVariant(QString("c:\\ckcore.txt")))
        a.setData(101, QVariant(101.1))
        self.itemDoubleClicked.connect(self.on_doubleclicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
    def openMenu(self, position):
        print ("openMenu ", position)
        menu = QMenu()
        pathAction = menu.addAction("Get Filepath")
        action = menu.exec_(self.mapToGlobal(position))
        if action == pathAction:
            print("filepath")
            item = self.itemAt(position)
            if isinstance(item, QListWidgetItem ):
                print(item.data(100).toString())
                cb = QtGui.QApplication.clipboard()
                cb.clear(mode=cb.Clipboard )
                cb.setText(item.data(100).toString(), mode=cb.Clipboard)

    def on_doubleclicked(self, item):
        print(item)
        a = item.data(100)
        if a != None:
            print(a.toString())
        a = item.data(101)
        if a != None:
            print(a.toUInt())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())