from PyQt4 import QtGui
import sys
from PyQt4 import QtCore
'''
practice: create a tree view without data structure, only with model
1->2
   -> 3
 ->4
   -> 5
   -> 6
   -> 7
 ->8
   -> 9
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
            print("rowCount parent is valid - return 0")
        return 0
    def columnCount(self, parent):
        return 1
    def data(self, index, role):
        print("data")
        if role == QtCore.Qt.DisplayRole:
            return "1"
        if role == QtCore.Qt.DecorationRole:
            return "Number"
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def parent(self, index):
        print("parent")
        if not index.isValid():
            print("index is not valid")
            return QtCore.QModelIndex()
        else:
            print("\tGet parent by index {}".format(index.internalPointer()))
            return QtCore.QModelIndex()
            #return self.createIndex(0, 0, "1")
    ''' get clild modelindex'''
    def index(self, row, column, parent):
        print("index");
        if not parent.isValid():
            pass
        if parent:
            print("\tGet index {} {} parent {}".format( row, column, parent.internalPointer()))
        else:
            print("\tGet index {} {} parent None".format( row, column))
            
        return self.createIndex(row, column, "1")
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("Num ModeL")
    model = NumModel(10, 2)
    treeview = QtGui.QTreeView()
    treeview.show()
    treeview.setModel(model)

    sys.exit( app.exec_())
