from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import * 
import sys
'''
PyQt4 Model View Tutorial Port 03_0
https://www.youtube.com/watch?v=EmYby3BB3Kk
'''
class PaletteListModel(QtCore.QAbstractListModel):
    def __init__(self, colors=[], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors = colors
    def rowCount(self, parent):
        return len(self.__colors)
    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            return self.__colors[index.row()].name()
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.__colors[row]
            return value.name()
        if role == QtCore.Qt.ToolTipRole:
            return "hex code:" + self.__colors[index.row()].name()
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            value = self.__colors[row]
            pixmap = QtGui.QPixmap(26,26)
            pixmap.fill(value)
            icon = QtGui.QIcon(pixmap)
            return icon
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            color = QtGui.QColor(value)
            if color.isValid():
                self.__colors[row] = color
                self.dataChanged.emit(index, index)
                return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString("Palette")
            else:
                return QtCore.QString("color %1").arg(section)
    def insertRows(self, position, rows, parent):
        self.beginInsertRows(QtCore.QModelIndex(), position, position+rows-1)
        #DO REMOVE HERE
        for i in range(rows):
            self.__colors.insert(position, QtGui.QColor("#000000"))

        self.endInsertRows( )
        return True
    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position+rows-1)
        for i in range(rows):
            value = self.__colors[position]
            self.__colors.remove(value)
        self.endRemoveRows()
        return True



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
  model = PaletteListModel([red,green, blue])

  columnCount = 6
  rowCount = 4
  #model = PaletteTableModel([[QColor("#f0f0f0") for i in range(columnCount)] for j in range(rowCount)])

  listView.setModel(model)
  treeView.setModel(model)
  combobox.setModel(model)
  tableView.setModel(model)
  model.insertRows(2, 5, QtCore.QModelIndex())
  model.removeRows(1, 5, QtCore.QModelIndex())

  sys.exit(app.exec_())

