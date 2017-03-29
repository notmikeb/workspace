import sys

from PyQt4 import QtGui, QtCore
import btdaycase
import logging
import tracelogging

import datetime
import sys

class BtCommand():
    def __init__(self, name = "Unknown"):
        self.name = name
    def setData(self, data):
        self.data = data
    def getData(self):
        return data

class BtDayMainClass(QtGui.QMainWindow, btdaycase.Ui_MainWindow):
    def __init__(self, parent = None):
        super(BtDayMainClass, self).__init__(parent)
        self.setupUi(self)
        logging.info("init down")
        self.tbnAdd.clicked.connect(self.addOneNode)
        self.addOneNode(None)
        self.tree2.itemClicked.connect(self.itemClicked)


    def addOneNode(self, data):
        logging.info("addOneNode {}".format(data))
        obj = BtCommand("hci_connect")
        item = QtGui.QTreeWidgetItem(None, QtCore.QStringList(QtCore.QString( obj.name )))
        item.setData(1 , 0, QtCore.QVariant(obj))
        self.tree2.addTopLevelItem(item)
        pass

    def moveOneNode(self, direction):
        logging.info("hello")
        pass
    def itemClicked(self, a, b):
        logging.info("{} {} {}".format(sys._getframe().f_code.co_name, repr(a), repr(b)))
        data = a.data(1, 0)
        obj = data.toPyObject()
        logging.info("{} {}".format(data.userType(), obj.name) )

if __name__ == "__main__":
  a = QtGui.QApplication(sys.argv)
  m = BtDayMainClass()
  m.show()
  a.exec_()
