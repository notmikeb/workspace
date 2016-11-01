from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui
import sys

'''
https://www.youtube.com/watch?v=VcN94yMOkyU
'''
class Node(object):
    def __init__(self,  name, parent = None):
        self._name = name
        self._children = []
        self._parent = parent
        if parent is not None:
            parent.addChild(self)
    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name
    def childCount(self):
        return len(self._children)
    def child(self, row):
        return self._children[row]
    def parent(self):
        return self._parent
    def row(self):
        if self._parent is not None:
            return  self._parent._children.index(self)
    def log(self, tabLevel =-1):
        output = ""
        tabLevel += 1
        for i in range(tabLevel):
            output += "\t"
        output += "|------" + self._name + "\n"
        for child in self._children:
            output += child.log(tabLevel)
        tabLevel -= 1
        return output
    def __repr__(self):
        return self.log()
    def typeInfo(self):
        return "NODE"


class TransformNode(object):
    def __init__(self, name, parent):
        super(TransformMode, self).____init__(name, parent)

class SceneGraphModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent = None ):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root
    '''
    input: qmodelindex
    output: int
    use a parent qmodelindex to ask how many child do it have
    '''
    def rowCount(self, parent):
        print ("ask rowcount {} isValid {}".format(repr(parent), parent.isValid()))
        if not parent.isValid(): #root
            parentNode = self._rootNode
        else:
            ''' parent is a qmodelindex and its internalpointer
            is a pointer to internal data structure
            '''
            parentNode = parent.internalPointer()
        return parentNode.childCount()
    ''' 
    input: qmodelindex
    output:  int
    use a parent qmodelindex to ask how many colum child do it has
    and for row, column, parent to get
    '''
    def columnCount(self, parent):
        return 1

    '''
    input : qmodelindex, int
    output: Qvariant, strings are cost to QString which is a Qvariant
    '''
    def data(self, index ,role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            print("ask the name of index {}".format(repr(index)))
            return node.name()
        if role == QtCore.Qt.DecorationRole:
            typeInfo = node.typeInfo()
            return typeInfo

    def headerData(self, section, orientation, role):
        return "Scenegraph"
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
    '''
    input: qmodelindex
    output: qmodelindex
    it is used to get a parent qmodelindex of a given qmodelindex
    should return the parent of the node with the give qmodelindex
    '''
    def parent(self, index):
        print("Ask parent of index {}".format(repr(index)));
        node = index.internalPointer()
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    '''
    input: int, int, qmodelindex
    output: qmodelindex
    ask the child qmodelindex of a parent and then use it at data()
    should returna a qmodelindex that corresponds to the given row, column, and parent node
    '''
    def index(self, row, column, parent):
        print("index row {} column {} parent-index {}".format( row, column, repr(parent)));
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")

    rootNode = Node("rootnode")
    childNode0 = Node("left", rootNode)
    childNode1 = Node("subroot of left ", childNode0)
    #childNode2 = Node("right", rootNode)
    '''childNode3 = Node("right3", childNode2)
    childNode4 = Node("right4", childNode3)
    childNode5 = Node("right5", childNode4)
    '''
    print(rootNode)

    model = SceneGraphModel(rootNode)
    treeView = QtGui.QTreeView()
    treeView.show()
    treeView.setModel(model)
    sys.exit(app.exec_())
