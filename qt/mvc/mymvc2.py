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
            print("rowCount parent is not valid. ask how may row - return 3");
            return 3
        else:
            print("rowCount parent is valid - return ")
            num = int(parent.internalPointer())
            if num == 1:
                print("return 3")
                return 3 # 2,4,8
            if num == 2:
                return 1 # 3
            if num == 4:
                return 3 # 5,6,7
            if num == 8:
                return 1 # 9
            print("rowCount parent <done>")
        return 0
    def columnCount(self, parent):
        return 1
    def data(self, index, role):
        print("data")
        if role == QtCore.Qt.DisplayRole:
            if index and index.isValid():
                num = index.internalPointer()
                print ("data {}".format(num))
            else:
                num = 0
            return "{}".format(num)
        if role == QtCore.Qt.DecorationRole:
            return "Number"
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def parent(self, index):
        print("parent")
        if not index.isValid():
            print("index is not valid")
            return QtCore.QModelIndex()
        if index.isValid():
            print("\tGet parent by index {}".format(index.internalPointer()))
            num = int(index.internalPointer())
            if None == num:
                print("\t invalid num. return invalid")
                return QtCore.QModelIndex()
            if num == 1:
                print("\t root node return invalid")
                return QtCore.QModelIndex()
            if num == 2:
                #return self.createIndex(0, 0, "1")
                # first level must return invalid 
                pass
            if num == 3:
                return self.createIndex(0, 0, "2")
            if num == 4:
                #return self.createIndex(0, 0, "1")
                # first level must return invalid 
                pass
            if num == 5:
                return self.createIndex(1, 0, "4")
            if num == 6:
                return self.createIndex(1, 0, "4")
            if num == 7:
                return self.createIndex(1, 0, "4")
            if num == 8:
                #return self.createIndex(0, 0, "1") 
                # first level must return invalid 
                pass
            if num == 9:
                return self.createIndex(2, 0, "8")
        print("return default")
        return QtCore.QModelIndex()

    ''' get clild modelindex'''
    def index(self, row, column, parent):
        print("index {} {} {}".format(row, column, not parent.isValid()));
        parentnum = 1
        if not parent.isValid():
            if row == 0: # 2
                print("\tcreate 2")
                return self.createIndex(0, 0, "2")
            if row == 1: # 4
                print("\tcreate 4")
                return self.createIndex(1, 0, "4")
            if row == 2: # 8
                print("\tcreate 8")
                return self.createIndex(2, 0, "8")
            print("\tinvalid !")
            return QtCore.QModelIndex()
        else:
            # valid index
            parentnum = int(parent.internalPointer())
            if parentnum == 2 or parentnum == 4 or parentnum == 8:
                childnum = parentnum + (1 + row)
                print("\tcreate {}".format(childnum))
                child_row = 0
                if childnum == 3:
                    child_row = 0
                    return self.createIndex(child_row, column, str(childnum))
                if childnum == 5:
                    child_row = 0
                    return self.createIndex(child_row, column, str(childnum))
                if childnum == 6:
                    cihld_row = 1
                    return self.createIndex(child_row, column, str(childnum))
                if childnum == 7:
                    child_row = 2
                    return self.createIndex(child_row, column, str(childnum))
                if childnum == 9:
                    child_row = 0
                    return self.createIndex(child_row, column, str(childnum))
        print("return invalid")
        return QtCore.QModelIndex()
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("Num ModeL")
    model = NumModel(10, 2)
    treeview = QtGui.QTreeView()
    treeview.show()
    treeview.setModel(model)

    sys.exit( app.exec_())
