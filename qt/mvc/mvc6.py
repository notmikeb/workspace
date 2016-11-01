from PyQt4.QtCore import *
from PyQt4.QtGui import *

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

if __name__ == "__main__":
    rootNode = Node("rootnode")
    childNode0 = Node("left", rootNode)
    childNode1 = Node("middle", rootNode)
    childNode2 = Node("right", childNode1)
    print(rootNode)
