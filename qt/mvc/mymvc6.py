from PyQt4 import QtGui
import sys
from PyQt4 import QtCore
'''
practice: create a tree view without data structure, only with model
0 - 1 -- 2 
      |- 3
0 is invisible
'''

class NumModel(QtCore.QAbstractItemModel):
    def __init__(self, max, rate):
        super(NumModel,self).__init__( )
        self.max = max
        self.rate = rate

    def rowCount(self, parent):
        if not parent.isValid():
            print("rowCount parent is not valid. ask how may row - return 1");
            return 1
        else:
            print("rowCount parent is valid - return n. parent.value = {}".format(parent.internalPointer()))
            if parent.internalPointer() == "1":
                print("\thas 2 subnode. so return 2")
                return 2
            else:
                print("\tno so much")
                return 0
        return 0
    def columnCount(self, parent):
        return 1
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                return "value:" +index.internalPointer()
            else:
                return "0"
        if role == QtCore.Qt.DecorationRole:
            return "Number"
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def parent(self, index):
        print("parent")
        if not index.isValid():
            print("index is not valid - return default")
            return QtCore.QModelIndex()
        else:
            if index.internalPointer() == "3":
                return self.createIndex(0,0, "1")
            if index.internalPointer() == "2":
                return self.createIndex(0,0, "1") # root only has 2
            if index.internalPointer() == "1":
                return QtCore.QModelIndex() # !!! root's first child doesn't have parent
            return QtCore.QModelIndex()
    ''' get clild modelindex'''
    def index(self, row, column, parent):
        print("index");
        if parent.isValid():
            print("\tvalid {}".format(parent.internalPointer()))
            if "1" == parent.internalPointer():
                if row == 0:
                    return self.createIndex(0,0, "2")
                if row == 1:
                    return self.createIndex(1,0, "3")
            else:
                print("\tunknow")
        if not parent.isValid():
            print("\tnot valid {} {}".format(row, column))
            return self.createIndex(0,0,"1")
           
        print("\tretun invalid modelindex at {} {}".format(row, column))
        return QtCore.QModelIndex()
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("Num ModeL")
    model = NumModel(10, 2)
    treeview = QtGui.QTreeView()
    treeview.show()
    treeview.setModel(model)

    sys.exit( app.exec_())
