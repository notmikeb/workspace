import sys

from PyQt4 import QtGui, QtCore
import btdaycase_ui
import logging
import tracelogging

import datetime
import sys
import random
import time

# for xml manipulate
from lxml import etree
#from lxml import objectify

import btdayelement
from btdayelement import *

class BtCommand():
    def __init__(self, name = "Unknown"):
        self.name = name
    def setData(self, data):
        self.data = data
    def getData(self):
        return self.data
    def runComand(self, recursive = True):
        logging.info("self.name {}".format(self.name))

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
    def runCommand(self):
        logging.info("runCommand: {}".format(self.data(1,0).toPyObject().name))
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

class BtDayMainClass(QtGui.QMainWindow, btdaycase_ui.Ui_MainWindow):
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
        self.tbnUp.clicked.connect(self.runAllNode)

        self.selectedNode = None
        self.tree2.itemClicked.connect(self.itemClicked)
        self.tree2.itemSelectionChanged.connect(self.itemClicked)
        self.tree2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        runAction = QtGui.QAction("Run", self.tree2)
        runAction.triggered.connect(self.runSelectedNode)
        self.tree2.addAction(runAction)

        self.tbl1.itemChanged.connect(self.saveTable)
        self.tbl2.itemChanged.connect(self.saveTable2)

        # load the xml file
        self.readFromXml(False)
        self.writeToXml(False)

        sampleData = [['opcode', 'integer', '123','0'],['parm2', 'text', '{}'.format(random.randint(0, 100))],['parm3', 'hex', 0x1234], ['parm4', 'list', [1,2,3,4]]]
        self.myTreeModel = MyTreeModel()
        #self.myTreeModel.setMyData(sampleData)
        #self.tbl1.setModel(self.myTreeModel)
        #self.updateTable1(sampleData)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            self.itemClicked(None)
        else:
            super(BtDayMainClass, self).keyPressEvent(event)

    def updateTable1(self, node, data):
        self.node = node
        if data == None:
            self.tbl1.setRowCount(0)
            self.tbl1.setColumnCount(0)
            return
        self.tbl1.setRowCount(len(data))
        self.tbl1.setColumnCount(4)
        header_lables = ["Field","Value", "Type", "Len"]
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

    def updateTable2(self, node, data):
        self.node = node
        if data == None:
            self.tbl2.setRowCount(0)
            self.tbl2.setColumnCount(0)
            return
        self.tbl2.setRowCount(len(data))
        self.tbl2.setColumnCount(2)
        header_lables = ["Field","Value"]
        self.tbl1.setHorizontalHeaderLabels(QtCore.QStringList(header_lables))
        for row,r in zip(data, range(len(data))):
            if len(row) > 0:
                self.tbl2.setItem(r, 0, QtGui.QTableWidgetItem(row[0]))
            if len(row) > 1:
                self.tbl2.setItem(r, 1, QtGui.QTableWidgetItem(row[1]))
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
                    self.tbl2.setItem(r, 2, QtGui.QTableWidgetItem(row[2]))

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
        self._exportTree2Xml()

    def _exportTree2Xml(self):
        def build(item, root):
            for row in range(item.childCount()):
                child = item.child(row)
                if isinstance(child, MyTreeWidgetItem):
                    # append all field & as subElement
                    name = child.data(1,0).toPyObject().name
                    fields = child.data(2,0).toPyObject().getData()
                    propertylist = child.data(1,0).toPyObject().getData()
                    if fields:
                        element = etree.SubElement(root, 'TestCase')
                        logging.info(" {}".format( repr(fields) ))
                        for i in fields: #fields
                            fname, fvalue = i
                            etree.SubElement(element, fname).text =  str(fvalue)
                    else:
                        element = etree.SubElement(
                            root, 'node', text=str(child.text(0).toUtf8()))
                    if propertylist:
                        for prow in propertylist:
                            i,j,k = prow
                            p1Element = etree.SubElement(element, 'PropertyList')
                            p2Element = etree.SubElement(p1Element, 'DynamicProperty')
                            paElement = etree.SubElement(p2Element, 'objValueString')
                            paElement.text = i
                            pbElement = etree.SubElement(p2Element, 'sName')
                            pbElement.text = j
                            pcElement = etree.SubElement(p2Element, 'typeString')
                            pcElement.text = k

                elif isinstance(child, PropertyListElement):
                    element = etree.SubElement(
                        root, 'node', text=str(child.text(0).toUtf8()))
                else:
                    element = etree.SubElement(
                        root, 'node', text=str(child.text(0).toUtf8()))
                build(child, element)
        # <TestPlanName TestPlanName="TestPlanDaylong4" IsSeperateLog="true" DAYVersion="2.1.30.2">
        root = etree.Element('TestPlanName')
        attrib = { 'TestPlanName':"TestPlanDaylong4", 'IsSeperateLog':"true", 'DAYVersion':"2.1.30.2"}
        for i in attrib.keys():
            root.set(i, str(attrib[i]))
        build(self.tree2.invisibleRootItem(), root)
        from xml.dom import minidom
        print(minidom.parseString(etree.tostring(root)).toprettyxml())

    def _exportTree(self):
        def build(item, root):
            for row in range(item.childCount()):
                child = item.child(row)
                element = etree.SubElement(
                    root, 'node', text=str(child.text(0).toUtf8()))
                build(child, element)
        root = etree.Element('root')
        build(self.tree2.invisibleRootItem(), root)
        from xml.dom import minidom
        print(minidom.parseString(etree.tostring(root)).toprettyxml())

    def readFromXml(self, clicked):
        filename = "sample.xml"
        for i in range(self.tree2.topLevelItemCount()):
            self.tree2.takeTopLevelItem(0)
        logging.info("readFromXml {}".format(filename))
        xml = "".join( open( str(filename), "r").read() )
        def build(item, root):
            for element in root.getchildren():
              if element.tag.find('}') >= 0:
                 tag = element.tag[element.tag.find('}')+1:]
              else:
                 tag = element.tag
              if isinstance(element, TestCaseElement):
                child = self._genOneNode(element.getPropertyList().getDataList(), str(element.tcName), item, element.getFieldList())
                child.setFlags(
                    child.flags() | QtCore.Qt.ItemIsEditable)
                build(child, element)
            item.setExpanded(True)
        #root = etree.fromstring(xml)
        root = etree.XML(xml, btdayelement.parser)
        remove_namespace(root, g_ns1)
        remove_namespace(root, g_ns2)
        build(self.tree2.invisibleRootItem(), root)

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
            logging.info("data1: " + t)
            pyobj = self.node.data(1,0).toPyObject() #QVariant
            pyobj.setData(data)
        else:
            logging.error("no current node !!!")

    def saveTable2(self, item):
        # save all data into self.node
        if self.node:
            data = []
            for r in range(self.tbl2.rowCount()):
                record = []
                for c in range(self.tbl2.columnCount()):
                    w = self.tbl2.item(r, c)
                    if w:
                        logging.info("w r {} c {} type {} text {}".format(r, c, w.type(), w.text()))
                        record.append( str(w.text()) )
                data.append(record)
            t = ",".join(["-".join(i) for i in data ])
            logging.info("data2: " + t)
            pyobj = self.node.data(2,0).toPyObject() #QVariant
            pyobj.setData(data)

        else:
            logging.error("no current node !!!")
    def runAllNode(self):
        t1 = time.time()*1000
        logging.info("begin: {}".format(t1))
        for i in range(self.tree2.topLevelItemCount()):
            self.runOneNode( self.tree2.topLevelItem(i) )
        t2 = time.time()*1000
        logging.info("end: {}".format(t2-t1))

    def runSelectedNode(self, selected = None):
        item = self.tree2.currentItem()
        self.runOneNode(item)

    def runOneNode(self, item):
        logging.info("runOneNode")

        def loopRun(item):
            t1 = time.time()*1000
            logging.info("begin: {}".format(t1))
            item.runCommand()
            for i in range(item.childCount()):
                loopRun(item.child(i))
            t2 = time.time()*1000
            logging.info("end: {}".format(t2-t1))
        loopRun(item)

    def _genOneNode(self, data = None, name = "UnknownName", parent = None, field = None):
        obj = BtCommand( str(name) )
        obj.name = name
        obj.text = name
        obj.setData(data)
        obj2 = BtCommand( str(name) )
        obj2.setData(field)
        item = MyTreeWidgetItem( parent, QtCore.QStringList(QtCore.QString( name )))
        item.setData(1 , 0, QtCore.QVariant(obj))
        item.setData(2 , 0, QtCore.QVariant(obj2))
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
    def itemClicked(self, a =None, b = None):
        logging.info("{} {} {}".format(sys._getframe().f_code.co_name, repr(a), repr(b)))
        a = self.tree2.currentItem()
        if a != None:
            # save a
            self.updateTable1(a, a.data(1,0).toPyObject().getData())
            self.updateTable2(a, a.data(2,0).toPyObject().getData())

    def test(self):
        pass

if __name__ == "__main__":
  a = QtGui.QApplication(sys.argv)
  m = BtDayMainClass()
  print "begin show"
  m.show()
  print "show done"
  a.exec_()
