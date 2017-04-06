import sip
sip.setapi('QString', 2)

#from xml.etree import cElementTree as etree
from lxml import etree
from lxml import objectify

from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self, xml):
        QtGui.QWidget.__init__(self)
        self.tree = QtGui.QTreeWidget(self)
        self.tree.header().hide()
        self.importTree(xml)
        self.button = QtGui.QPushButton('Export', self)
        self.button.clicked[()].connect(self.exportTree)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.tree)
        layout.addWidget(self.button)

    def importTree(self, xml):
        def build(item, root):
            for element in root.getchildren():
              #print element.tag
              if element.tag.find('}') >= 0:
                 tag = element.tag[element.tag.find('}')+1:]
              else:
                 tag = element.tag
              if tag == "TestCase":
                #print dir(element)
                child = QtGui.QTreeWidgetItem(
                    item, [ str(element.tcName) ])
                child.setFlags(
                    child.flags() | QtCore.Qt.ItemIsEditable)
                build(child, element)
            item.setExpanded(True)
        #root = etree.fromstring(xml)
        root = objectify.fromstring(xml)
        build(self.tree.invisibleRootItem(), root)

    def exportTree(self):
        def build(item, root):
            for row in range(item.childCount()):
                child = item.child(row)
                element = etree.SubElement(
                    root, 'node', text=child.text(0))
                build(child, element)
        root = etree.Element('root')
        build(self.tree.invisibleRootItem(), root)
        from xml.dom import minidom
        print(minidom.parseString(etree.tostring(root)).toprettyxml())

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    text = "".join( open("sample.xml", "r") )
    window = Window(text)
    
    window.setGeometry(800, 300, 300, 300)
    window.show()
    sys.exit(app.exec_())