from PyQt4 import QtCore, QtGui, QtXml
from lxml import etree
from lxml import objectify

class myTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, xml, stringlist):
        super(QtGui.QTreeWidgetItem,self).__init__(stringlist, 0)
        self.xml = xml
    
class lxmlTreeWidgetItem(objectify.Element):
    def __init__(self, xml, stringlist):
        super(objectify.Element,self).__init__(stringlist)
        self.xml = xml


class Window(QtGui.QTreeWidget):
    def __init__(self):
        QtGui.QTreeWidget.__init__(self)
        self.header().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setHeaderLabels(['Title', 'Type'])
        a = lxmlTreeWidgetItem( None, QtCore.QStringList(["1", "2", "3"]) )
        self.insertTopLevelItem( 0, a  )
        b = lxmlTreeWidgetItem( None, QtCore.QStringList(["a", "b", "c"]) )
        a.addChild(b)
        self.insertTopLevelItem( 1, lxmlTreeWidgetItem( None, QtCore.QStringList(["x", "y", "z"]) ) )

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())