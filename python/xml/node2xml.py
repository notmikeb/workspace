from PyQt4 import QtGui, QtCore
from PyQt4 import *
import copy
import tracelogging
import logging
import random
import sys

class MyTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, *p, **k):
        super(MyTreeWidgetItem, self).__init__(*p, **k)
        self.isBox = False
        self.data = None
        self.name = None
    def setType(self, name = "Folder", isBox = False, classname ="HCI_COMMAND"):
        self.name = name
        self.isBox = isBox
        self.classname = classname
    def setData(self, data):
        self.data = copy.deepcopy(data)
        if self.isBox:
            logging.error("{} isbox:{} should not have data:{}".format(self, self.isBox, data))
    def getData(self):
        return self.data
    def toXml(self, outStream):
        if self.isBox:
            # put a box element and invoke its children's toXml
            self._toBoxXml(outStream)
        else:
            # put self's toDataXml
            self._toDataXml(outStream)
    def fromXml(self, inStream):
        pass
    def _toBoxXml(self, out):
        out.write( "<folder name='{}'>\n".format(self.name))
        for i in range(self.childCount()):
            c = self.child(i)
            c.toXml(out)
        out.write( "</folder>\n")
        pass
    def _toDataXml(self, out):
        out.write("<Element name='{}' classname='{}'>\n".format(self.name, self.classname))
        for i in range(len(self.data)):
            d = self.data[i]
            num = len(self.data[i])
            if num > 0:
                out.write("<item ")
                for pn in range(num):
                    out.write("p{}='{}'".format(pn, d[pn]))
                out.write(">")
                out.write("</item>\n")
        out.write("</Element>\n")
        pass
    def _fromBoxXml(self, outStream):
        pass
    def _fromDataXml(self, outStream):
        pass

def dumplist(alist, filename = "output.xml"):
    #a = open(filename, "w")
    #with a:
    if 1:
        for i in alist:
            i.toXml(sys.stdout)

def main():
    toplist = []
    sampleData = [['opcode', 'integer', '123','0'],['parm2', 'text', '{}'.format(random.randint(0, 100))],['parm3', 'hex', 0x1234], ['parm4', 'list', [1,2,3,4]]]
    i = MyTreeWidgetItem()
    i.setType("Folder", True)
    i.setData(sampleData)
    sampleData[0][3] = '999'
    toplist.append(i)

    j= MyTreeWidgetItem()
    j.setType("HCI_Command1", False)
    j.setData(sampleData)
    sampleData[0][3] = '888'
    i.addChild(j)
    j= MyTreeWidgetItem()
    j.setType("HCI_Command2", False)
    j.setData(sampleData)
    sampleData[0][3] = '777'
    i.addChild(j)

    i = MyTreeWidgetItem()
    i.setType("HCI_Command3", False)
    i.setData(sampleData)
    toplist.append(i)

    dumplist(toplist, "output.xml")


if __name__ == '__main__':
    main()
