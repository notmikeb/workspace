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

class HciCommand(BtCommand):
    def __init__(self, name = "Unknown"):
        super(HciCommand, self).__init__("hci_" + name)


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

class MyTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, *p, **k):
        super(MyTreeWidgetItem, self).__init__(*p, **k)
        self.isBox = False
    def setType(self, isBox = False):
        self.isBox = isBox
    def toXml(self, outStream):
        if self.isBox:
            # put a box element and invoke its children's toXml
            self._toBoxXml(outStream)
        else:
            # put self's toDataXml
            self._toDataXml(outStream)
    def fromXml(self, inStream):
        pass
    def _toBoxXml(self, outStream):
        pass
    def _toDataXml(self, outStream):
        pass
    def _fromBoxXml(self, outStream):
        pass
    def _fromDataXml(self, outStream):
        pass

# http://stackoverflow.com/questions/8837950/pyqt-xml-to-qtreewidget
class MyTree(QtGui.QTreeWidget):

    def __init__(self, parent):
        # maybe init your data here too
        super(MyTree, self).__init__(parent)

    def populate(self, data):
        # populate the tree with QTreeWidgetItem items
        for row in data:
            # is attached to the root (parent) widget
            rowItem = QtGui.QTreeWidgetItem(parent)
            rowItem.setText(0, row)
            for subRow in row:
                 # is attached to the current row (rowItem) widget
                 subRowItem = QtGui.QTreeWidgetItem(rowItem)
                 subRowItem.setText(0, subRow)

class BtDayMainClass(QtGui.QMainWindow, btdaycase.Ui_MainWindow):
    def __init__(self, parent = None):
        super(BtDayMainClass, self).__init__(parent)
        self.setupUi(self)
        logging.info("init down")
        self.tree2 = MyTree( self.boxMiddle )
        self.verticalLayout.addWidget(self.tree2)
        #self.boxMiddle.addWidget(self.tree2)
        self.tbnAdd.clicked.connect(self.addOneNode)
        self.tbnRemove.clicked.connect(self.removeSelectedNode)
        self.tbnLeft.clicked.connect(self.readFromXml)
        self.tbnRight.clicked.connect(self.writeToXml)

        self.selectedNode = None
        self.tree2.itemClicked.connect(self.itemClicked)
        self.tbl1.itemChanged.connect(self.saveTable)

        ## add one node by default
        #self.addOneNode(None)

        #test
        #self.tbl1.setRowCount(2)
        #self.tbl1.setColumnCount(2)
        #btn = QtGui.QPushButton(self.tbl1)
        #btn.setText("this")

        sampleData = [['opcode', 'integer', '123','0'],['parm2', 'text', '{}'.format(random.randint(0, 100))],['parm3', 'hex', 0x1234], ['parm4', 'list', [1,2,3,4]]]
        self.myTreeModel = MyTreeModel()
        #self.myTreeModel.setMyData(sampleData)
        #self.tbl1.setModel(self.myTreeModel)
        #self.updateTable(sampleData)

    def updateTable(self, node, data):
        self.node = node
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
    def removeSelectedNode(self):
        logging.info("removeSelectedNode columnCount:{} column:{}".format(self.tree2.columnCount(), self.tree2.currentColumn()))
        item = self.tree2.currentItem()
        if item != None:
            #//http://stackoverflow.com/questions/12134069/delete-qtreewidgetitem-in-pyqt
            if item.parent() is not None:
                item.parent().removeChild(item)
            else:
                self.tree2.takeTopLevelItem(self.tree2.indexOfTopLevelItem(item))
            self.itemClicked( self.tree2.currentItem(), None )
        else:
            logging.error("No any selected item")

    def writeToXml(self, filename = "testplan.xml"):
        logging.info("writeToXml {}".format(filename))
        pass
    def readFromXml(self, filename = "testplan.xml"):
        logging.info("readFromXml {}".format(filename))
        pass
                #self.tbl1.setCellWidget()
    def saveTable(self, item):
        # save all data into self.node
        if self.node:
            data = []
            for r in range(self.tbl1.rowCount()):
                record = []
                for c in range(self.tbl1.columnCount()):
                    w = self.tbl1.item(r, c)
                    if w:
                        logging.info("w r {} c {} type {} text {}".format(r, c, w.type(), w.text()))
                        record.append( str(w.text()) )
                data.append(record)
            t = ",".join(["-".join(i) for i in data ])
            logging.info("data: " + t)
            pyobj = self.node.data(1,0).toPyObject() #QVariant
            pyobj.setData(data)
        else:
            logging.error("no current node !!!")

    def _genOneNode(self, data = None):
        obj = BtCommand("hci_connect")
        if data == None:
            obj.setData([['opcode', 'integer', '123','0'],['parm2', 'text', '{}'.format(random.randint(0, 100))],['parm3', 'hex', 0x1234]])
        else:
            obj.setData(data)
        item = MyTreeWidgetItem(None, QtCore.QStringList(QtCore.QString( obj.name )))
        item.setData(1 , 0, QtCore.QVariant(obj))
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        return item

    def addOneNode(self, clicked = False):
        data = None
        logging.info("addOneNode {}".format(data))
        item = self._genOneNode(data)
        if self.tree2.currentItem() is not None:
            self.tree2.currentItem().addChild(item)
            self.tree2.setItemExpanded(self.tree2.currentItem(), True)
        else:
            self.tree2.addTopLevelItem(item)

        pass

    def saveAllNode(self, filename="tree.xml"):
        pass
    def loadAllNode(self, filename="tree.xml"):
        pass

    def moveOneNode(self, direction):
        logging.info("hello")
        pass
    def itemClicked(self, a, b):
        logging.info("{} {} {}".format(sys._getframe().f_code.co_name, repr(a), repr(b)))
        if a != None:
            # save a
            self.updateTable(a, a.data(1,0).toPyObject().getData())

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
