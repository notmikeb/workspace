import sys

from PyQt4 import QtGui, QtCore
import btdaycase
import logging
import tracelogging

import datetime
import sys
import random

class BtCommand():
    def __init__(self, name = "Unknown"):
        self.name = name
    def setData(self, data):
        self.data = data
    def getData(self):
        return self.data

# http://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
class MyTreeModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        super(MyTreeModel, self).__init__()
        self.datatable = [ [1,2,3], [4,5,6]]

    def update(self, dataIn):
        logging.info( 'Updating Model')
        self.datatable = dataIn
        logging.info( 'Datatable : {0}'.format(self.datatable))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.columns.values)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return '{0}'.format(self.datatable.iget_value(i, j))
        else:
            return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled


class BtDayMainClass(QtGui.QMainWindow, btdaycase.Ui_MainWindow):
    def __init__(self, parent = None):
        super(BtDayMainClass, self).__init__(parent)
        self.setupUi(self)
        logging.info("init down")
        self.tbnAdd.clicked.connect(self.addOneNode)
        self.addOneNode(None)
        self.tree2.itemClicked.connect(self.itemClicked)

        #test
        #self.tbl1.setRowCount(2)
        #self.tbl1.setColumnCount(2)
        #btn = QtGui.QPushButton(self.tbl1)
        #btn.setText("this")

        sampleData = [['opcode', 'integer', '123','0'],['parm2', 'text', '{}'.format(random.randint(0, 100))],['parm3', 'hex', 0x1234], ['parm4', 'list', [1,2,3,4]]]
        self.myTreeModel = MyTreeModel()
        #self.myTreeModel.setMyData(sampleData)
        self.tbl1.setModel(self.myTreeModel)
        #self.updateTable(sampleData)

    def updateTable(self, data):
        self.tbl1.setRowCount(len(data))
        self.tbl1.setColumnCount(4)
        header_lables = ["Field","Type", "Value", "Len"]
        self.tbl1.setHorizontalHeaderLabels(QtCore.QStringList(header_lables))
        for row,r in zip(data, range(len(data))):
            if len(row) > 0:
                self.tbl1.setItem(r, 0, QtGui.QTableWidgetItem(row[0]))
            if len(row) > 1:
                self.tbl1.setItem(r, 1, QtGui.QTableWidgetItem(row[1]))
            if len(row) > 2:
                if row[1] == 'list':
                    w = QtGui.QComboBox()
                    for s in row[2]:
                        logging.info("{}".format(s))
                        w.addItem(QtCore.QString("{}".format(s)))
                    self.tbl1.setCellWidget(r,2,w)
                elif row[1] == 'button':
                    pass
                else:
                    self.tbl1.setItem(r, 2, QtGui.QTableWidgetItem(row[2]))


                #self.tbl1.setCellWidget()


    def addOneNode(self, data):
        logging.info("addOneNode {}".format(data))
        obj = BtCommand("hci_connect")
        obj.setData([['opcode', 'integer', '123','0'],['parm2', 'text', '{}'.format(random.randint(0, 100))],['parm3', 'hex', 0x1234]])
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
        for index, item in zip(range(len(obj.getData())), obj.getData()):
            i,j, k = item
            logging.info("{}:{} {} {}".format(index, i,j,k) )

    def test(self):
        pass

print "hello"
if __name__ == "__main__":
  a = QtGui.QApplication(sys.argv)
  m = BtDayMainClass()
  print "begin show"
  m.show()
  print "show done"
  a.exec_()
