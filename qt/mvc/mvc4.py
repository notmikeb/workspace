from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import * 
import sys
class PaletteTableModel(QtCore.QAbstractListModel):
    def __init__(self, colors=[[]], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors = colors
    def rowCount(self, parent):
        return len(self.__colors)
    def columnCount(self, parent)
        return len(self.__colors[0])
    def flags(self, index):
        re://www.youtube.com/watch?v=Eq7__6y0jwoturn QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        print(repr(role))
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.__colors[row]
            return value.name()
        if role == QtCore.Qt.EditRole:
            return self.__colors[index.row()].name()
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            value = self.__colors[row]
            pixmap = QtGui.QPixmap(26,26)
            pixmap.fill(value)
            icon = QtGui.QIcon(pixmap)
            return icon
        if setData(self, index, value, role= QtCore.Qt.EditRole):
            if role == QtCore.Qt.EditRole:
                row = index.row()
                color = QtGui.QColor(value)
                if color.isValid():
                    self.__colors[row] = color
                    self.dataChanged.emit(index, index)
                    return True

i
class PaletteListModel(QtCore.QAbstractListModel):
    def __init__(self, colors=[], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors = colors
    def rowCount(self, parent):
        return len(self.__colors)
    def data(self, index, role):
        print(repr(role))
        if role == QtCore.Qt.DisplayRole:
            return "HARDCODED ITEM"

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  app.setStyle("plastique")

  listView = QtGui.QListView()
  listView.show()

  treeView = QtGui.QTreeView()
  treeView.show()

  combobox = QtGui.QComboBox()
  combobox.show()

  tableView = QTableView()
  tableView.show()

  red = QtGui.QColor(255,0,0)
  green = QtGui.QColor(0,255,0)
  blue = QtGui.QColor(0,0,255)
  #model = PaletteListModel([red,green, blue])

  columnCount = 6
  rowCount = 4
  model = PaletteTableModel([[QColor("#f0f0f0") for i in range(columnCount)] for j in range(rowCount)])

  listView.setModel(model)
  treeView.setModel(model)
  combobox.setModel(model)
  tableView.setModel(model)
  sys.exit(app.exec_())
