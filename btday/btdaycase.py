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

# for drag and drop
import cPickle
import pickle


import btdayelement
from btdayelement import *

logging.getLogger().setLevel(logging.INFO)

class BtCommand():
    def __init__(self, name = "Unknown"):
        self.name = name
        self.cmd = name
        self.data = self.field = None
    def setData(self, data):
        self.data = data
    def getData(self):
        return self.data
    def setField(self, field):
        if type(field) != dict:
            raise ValueError
            return
        self.field = field
        if self.field.has_key("methodInfoName"):
            self.cmd = self.field['methodInfoName']
        else:
            self.cmd = "Unknown methodInfo"
            logging.error("no methodInfo {}".format(repr(self.field)))

    def getField(self):
        return self.field
    def runSelf(self, recursive = True):
        logging.info("self.name {}".format(self.name))
        try:
            if self.cmd == 'pytest':
                pcmd = self.field['typeOfTCControlTargetName']
                codetext = 'import {};{}({})'.format( pcmd[0:pcmd.rfind('.')], pcmd, repr(self.data))
                logging.info("python-code is:" + codetext)
                codeobj = compile(codetext, 'fakemodule', 'exec')
                exec(codeobj)
            elif self.cmd == 'sl4a':
                pcmd = self.field['typeOfTCControlTargetName']
                valuelist = [i[1] for i in self.data]
                codetext = 'import {};{}({})'.format( pcmd[0:pcmd.rfind('.')], pcmd, repr(valuelist))
                logging.info("python-code is:" + codetext)
                codeobj = compile(codetext, 'fakemodule', 'exec')
                exec(codeobj)
            else:
                logging.info("do not how to run '{}'".format(self.cmd))
        except:
            logging.error("err: {}".format( sys.exc_info()))

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
        obj = self.data(1,0).toPyObject()
        logging.info("runCommand: {}".format(obj.name))
        if obj != None:
            obj.runSelf()

    def getCommandDescription(self):
        selected = self.data(1,0).toPyObject()
        #try:
        if selected:
            objname = selected.name
            cmd = selected.cmd
            info = repr(selected.getData())
        else:
        #except:
            objname = cmd = info = "None"
        return "object = {}; object.{} {}".format(objname, cmd, info)

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

        # tree1 building up with atom sample
        self.tree1.dragEnterEvent = self.tree1DragEnterEvent
        self.tree1.startDrag = self.tree1StartDrag
        self.tree1.mouseMoveEvent = self.tree1MouseMoveEvent
        self._tree1BuildingUp()

        # tree2 building up
        self.selectedNode = None
        self.tree2.itemClicked.connect(self.itemClicked)
        self.tree2.itemSelectionChanged.connect(self.itemClicked)
        self.tree2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        runAction = QtGui.QAction("Run", self.tree2)
        runAction.triggered.connect(self.runSelectedNode)
        self.tree2.addAction(runAction)
        self.tree2.startDrag = self.tree2StartDrag
        self.tree2.mouseMoveEvent = self.tree2MouseMoveEvent
        self._tree2BuildingUp()

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

    def _tree1BuildingUp(self):
        data = [["1", "2", "3"]]
        field = {"tcName": "Hello1", "methodInfoName":"pytest", "typeOfTCControlTargetName": "run_pytest.run1"}
        self._genOneNode(data, str("pytest_run1_func"), self.tree1.invisibleRootItem(), field)

        data = [["a", "b", "c"], ["d", "d", "e"] ]
        field = {"tcName": "Hello2", "methodInfoName":"pytest", "typeOfTCControlTargetName": "run_pytest.run3"}
        self._genOneNode(data, str("pytest_run3_func"), self.tree1.invisibleRootItem(), field)


        data = [['port','0', 'int'], ['method', 'makeToast','string'],["param1", "c-hello~", 'string'] ]
        field = {"tcName": "sl4a_Hello", "methodInfoName":"sl4a", "typeOfTCControlTargetName": "run_sl4a.run1"}
        self._genOneNode(data, str("sl4a_makeToast"), self.tree1.invisibleRootItem(), field)

        data = [['port','0', 'int'], ['method', 'checkBluetoothState','string']]
        field = {"tcName": "sl4a_checkBluetoothState", "methodInfoName":"sl4a", "typeOfTCControlTargetName": "run_sl4a.run1"}
        self._genOneNode(data, str("sl4a_GetBluetoothState"), self.tree1.invisibleRootItem(), field)

    def tree1DragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-person"):
            event.accept()
        else:
            event.ignore()
    def tree1StartDrag(self, event):
        print("draggableList startDrag")
        drag = QtGui.QDrag(self)
        selected = self.tree1.currentItem().data(1,0).toPyObject()
        bstream = cPickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/atom", bstream)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        result = drag.start(QtCore.Qt.CopyAction)

    def tree1MouseMoveEvent(self, event):
        self.tree1.startDrag(event)

    def tree2StartDrag(self, event):
        print ("draggableList startDrag")
        index = self.tree2.indexAt(event.pos())
        drag = QtGui.QDrag(self)
        selected = self.tree2.currentItem().data(1,0).toPyObject()
        bstream = cPickle.dumps(selected)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/atom", bstream)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        result = drag.start(QtCore.Qt.MoveAction)
        if result == QtCore.Qt.MoveAction:
            logging.info("Drag done with {} Moveaction is {}".format(result, QtCore.Qt.MoveAction))
        else:
            logging.info("Drag done with {}".format(result))

    def tree2MouseMoveEvent(self, event):
        self.tree2.startDrag(event)

    def _tree2BuildingUp(self):
        self.tree2.dragEnterEvent = self.tree2DragEnterEvent
        self.tree2.dragMoveEvent = self.tree2DragMoveEvent
        self.tree2.dragLeaveEvent = self.tree2DragLeaveEvent
        self.tree2.dropEvent = self.tree2DropEvent
        self.tree2.dropMimeData = self.tree2DropMimeData
        self.tree2.setAcceptDrops(True)

    def tree2DragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/atom"):
            event.accept()
        else:
            event.ignore()

    def tree2DragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/atom"):
            #event.setDropAction(QtCore.Qt.MoveAction)
            #logging.info( "dragmove check {} {}".format(event.source() , self.tree2))
            if event.source() == self.tree2 or event.source() == self:
                #logging.info("tree2dragmove moveAction")
                event.setDropAction(QtCore.Qt.MoveAction or QtCore.Qt.IgnoreAction)
            else:
                #logging.info("tree2dragmove copyAction")
                event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def tree2DragLeaveEvent(self, event):
        pass

    def tree2DropMimeData(self, parent, row, data, action):
        logging.info("tree2DropMimeData action:{}".format(action))
        if action == QtCore.Qt.MoveAction:
            return self.tree2MoveSelection(parent, row)
        else:
            return self.tree2CopySelection()
        return False
    def moveSelection(self, parent, position):
         # self.selectedIndexes() is the selected QTreeWidgets' QModelIndex
         # position type:int and position type:QTreeWidget is the target to put

         # save the selected items' persistentQindex. if we use QModelIndex, it will change after 1 moved
         selection = [QtCore.QPersistentModelIndex(i)
                      for i in self.tree2.selectedIndexes()]
         print("{} {} {}".format(position, i, QtCore.QPersistentModelIndex(i)))
         parent_index = self.tree2.indexFromItem(parent)  #from parent type:TreeWidgetItem to get its QModelIndex
         if parent_index in selection:
             return False

         # save the drop location in case it gets moved since it doesn't exist yet (no previous item)
         target = self.tree2.model().index(position, 0, parent_index).row() # (row,column=0, index) to get the child's QModelIndex
         print("position {} target {}".format(position, target)) # target sometimes is -1 when the row is lastone or empty
         if target < 0:
             target = position

         # remove the selected items
         taken = []
         for index in reversed(selection):
             #index is a QPersistentModelIndex, we need QModelIndex. both are 1-1 mapping
             print("index.row {} {} type(position):{}".format(index.row(), type(index), type(position)))
             item = self.tree2.itemFromIndex(QtCore.QModelIndex(index))
             # indexFromItem vs ItemFromIndex could switch betwen WtreeItem and QModelIndex
             if item is None or item.parent() is None:
                 taken.append(self.tree2.takeTopLevelItem(index.row()))
             else:
                 taken.append(item.parent().takeChild(index.row()))

         # insert the selected items at their new positions
         while taken:
             if position == -1:
                 # append the items if position not specified
                 if parent_index.isValid():
                     parent.insertChild(
                         parent.childCount(), taken.pop(0))
                 else:
                     self.tree2.insertTopLevelItem(
                         self.tree2.topLevelItemCount(), taken.pop(0))
             else:
		# insert the items at the specified position
                 if parent_index.isValid():
                     parent.insertChild(min(target,
                         parent.childCount()), taken.pop(0))
                 else:
                     self.tree2.insertTopLevelItem(min(target,
                         self.tree2.topLevelItemCount()), taken.pop(0))
         return True

    def tree2DropEvent(self, event):
        logging.info("event DropAction: {}".format(event.dropAction()))
        if event.dropAction() == QtCore.Qt.MoveAction:
            position = event.pos()
            if self.tree2.itemAt(position) == self.tree2.currentItem():
                logging.error("abort to move to itself")
                event.ignore()
                event.setDropAction(QtCore.Qt.IgnoreAction)
                return False


            if self.tree2.currentItem():
                parent = self.tree2.currentItem().parent()
            else:
                parent = self.tree2.invisibleRootItem()
            item = self.tree2.itemAt(position)
            p = self.tree2.indexFromItem(item)
            logging.info("index row p  {} {}".format(p.row(), repr(p)))
            logging.info(type(p))
            q = QtCore.QPersistentModelIndex( p)
            logging.info(type(q))
            self.moveSelection(parent, q.row())
            event.accept()
            return True
            """
            selection = [QtCore.QPersistentModelIndex(i)
                      for i in self.tree2.selectedIndexes()]
            print("{} {} {}".format(position, i, QtCore.QPersistentModelIndex(i)))
            parent_index = self.tree2.indexFromItem(parent)  #from parent type:TreeWidgetItem to get its QModelIndex
            logging.info("parent_index selection: {} {}".format(parent_index, selection ))
            if parent_index in selection:
                event.ignore()
                event.setDropAction(QtCore.Qt.IgnoreAction)
                logging.error("abort drop")
                return False
            # success. move selected item to new parent
            if self.tree2.currentItem() and self.tree2.itemAt(position):
                item = self.tree2.currentItem()
                if item.parent() != None:
                    item.parent().removeChild(item)
                else:
                    self.tree2.takeTopLevelItem(self.tree2.indexOfTopLevelItem(item))
                self.tree2.itemAt(position).addChild(item)
                logging.info("move it")
            else:
                logging.error("abort drop because do not know how to move")
                event.ignore()
                event.setDropAction(QtCore.Qt.IgnoreAction)
                logging.error("abort drop")
                return False
            """


        data = event.mimeData()
        bstream = data.retrieveData("application/atom",
            QtCore.QVariant.ByteArray)
        selected = pickle.loads(bstream.toByteArray())
        logging.info("drop data is: {}".format(selected) )
        # selected is a BTCommand object
        parent = self.tree2.itemAt(event.pos())
        logging.info("event pos {} parent {}".format(event.pos(), repr(parent)))
        if parent == None:
            parent = self.tree2.invisibleRootItem()
        self._genOneNode(selected.getData(), str(selected.name), parent, selected.getField())
        event.accept()

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
        self.tbl1.blockSignals(True)
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
        self.tbl1.blockSignals(False)

    def updateTable2(self, node, fields):
        self.node = node
        if fields == None:
            self.tbl2.setRowCount(0)
            self.tbl2.setColumnCount(0)
            return
        if type(fields) != dict:
            return
        #logging.info("fields len:{}".format(len(fields.keys())))
        self.tbl2.blockSignals(True)
        self.tbl2.setRowCount(len(fields.keys()))
        self.tbl2.setColumnCount(2)
        header_lables = ["Field","Value"]
        self.tbl2.setHorizontalHeaderLabels(QtCore.QStringList(header_lables))

        for r, row in zip(range(len(fields.keys())), sorted(fields.keys())):
            #logging.info(" r row {} {}".format(r, row))
            self.tbl2.setItem(r, 0, QtGui.QTableWidgetItem(row))
            self.tbl2.setItem(r, 1, QtGui.QTableWidgetItem(fields[row]))
        self.tbl2.blockSignals(False)

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
                    selected = child.data(1,0).toPyObject()
                    name = selected.name
                    fields = selected.getField()
                    propertylist = selected.getData()
                    if fields:
                        element = etree.SubElement(root, 'TestCase')
                        logging.info(" {}".format( repr(fields) ))
                        for i in fields.keys(): #fields
                            fname = i
                            fvalue = fields[i]
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
                        #logging.debug("w r {} c {} type {} text {}".format(r, c, w.type(), w.text()))
                        record.append( str(w.text()) )
                data.append(record)
            t = ",".join(["-".join(i) for i in data ])
            logging.debug("data1: " + t)
            pyobj = self.node.data(1,0).toPyObject() #QVariant
            pyobj.setData(data)
        else:
            logging.error("no current node !!!")

    def saveTable2(self, item):
        # save all data into self.node
        if self.node:
            fields = {}
            for r in range(self.tbl2.rowCount()):
                record = []
                if self.tbl2.columnCount() == 2:
                    k  = str(self.tbl2.item(r, 0).text())
                    v = str(self.tbl2.item(r, 1).text())
                    if len(k) > 0:
                        fields[k] = v
            logging.debug("data2: " + repr(fields))
            pyobj = self.node.data(1,0).toPyObject() #QVariant
            pyobj.setField(fields)
        else:
            logging.error("no current node !!!")
    def runAllNode(self):
        t1 = time.time()*1000000
        logging.info("begin: {}".format(t1))
        for i in range(self.tree2.topLevelItemCount()):
            self.runOneNode( self.tree2.topLevelItem(i) )
        t2 = time.time()*1000000
        logging.info("end: {}".format(t2-t1))

    def runSelectedNode(self, selected = None):
        item = self.tree2.currentItem()
        self.runOneNode(item)

    def runOneNode(self, item):
        logging.info("runOneNode")

        def loopRun(item):
            t1 = time.time()*1000000
            logging.info("begin: {}".format(t1))
            item.runCommand() # invoke
            for i in range(item.childCount()):
                loopRun(item.child(i))
            t2 = time.time()*1000000
            logging.info("end: {}".format(t2-t1))
        loopRun(item)

    def _genOneNode(self, data = None, name = "UnknownName", parent = None, field = None):
        obj = BtCommand( str(name) )
        obj.name = name
        obj.text = name
        obj.setData(data)
        obj.setField(field)
        item = MyTreeWidgetItem( parent, QtCore.QStringList(QtCore.QString( name )))
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
    def itemClicked(self, a =None, b = None):
        #logging.info("{} {} {}".format(sys._getframe().f_code.co_name, repr(a), repr(b)))
        a = self.tree2.currentItem()
        p = self.tree2.indexFromItem(a)
        p2 = self.tree2.indexFromItem(a.parent())
        if a != None:
            # save a
            #logging.info("index {} row {} persistent {} p-index {} p2.row {}".format(p, p.row(), repr(QtCore.QPersistentModelIndex( p)), self.tree2.indexFromItem(a.parent()) , p2.row()) )
            selected = a.data(1,0).toPyObject()
            self.updateTable1(a, selected.getData())
            self.updateTable2(a, selected.getField())
            self.updateConsole(a, selected)

    # a plaintext widget to show the running command
    def updateConsole(self, item, atom):
        self.pteRaw1.setPlainText( str(item.getCommandDescription()) )

    def test(self):
        pass

if __name__ == "__main__":
  a = QtGui.QApplication(sys.argv)
  m = BtDayMainClass()
  print("begin show")
  m.show()
  print("show done")
  a.exec_()
