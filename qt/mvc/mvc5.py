from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import * 
import sys
'''
PyQt4 Model View Tutorial Port 03_0
https://www.youtube.com/watch?v=EmYby3BB3Kk
'''
class PaletteTableModel(QtCore.QAbstractTableModel):
    def __init__(self, colors=[[]], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors = colors
        ''''
        tableData1 = [
                [1,2,3,4],
                [5,6,7,8]
                ]
                '''
    def rowCount(self, parent):
        return len(self.__colors)
    def columnCount(self, parent):
        return len(self.__colors[0])
    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__colors[row][column].name()
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__colors[row][column]
            return value.name()
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            return "hex code:" #+ self.__colors[row][column].name()
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()
            value = self.__colors[row][column]
            pixmap = QtGui.QPixmap(26,26)
            pixmap.fill(value)
            icon = QtGui.QIcon(pixmap)
            return icon
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if len(value.toString()) > 0 and value.toString()[0] != '#':
                value = QtCore.QVariant("#" + value.toString())
            if len(value.toString()) < 7:
                append = "0" * (7 - len(value.toString()))
                value = QtCore.QVariant(value.toString() + append )

            color = QtGui.QColor(value)
            if color.isValid():
                self.__colors[row][column] = color
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
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(), position, position+rows-1)
        #DO REMOVE HERE
        for i in range(rows):
            defaultValues = [QtGui.QColor("#000000") for i in range(self.columnCount(None))]
            self.__colors.insert(position, defaultValues)

        self.endInsertRows( )
        return True
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
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

  columnCount = 6
  rowCount = 4
  tableData0 = [
          [ QtGui.QColor("#ff00ff") for i in range(columnCount)] for j in range(rowCount)
          ]
  model = PaletteTableModel([[QtGui.QColor("#f0f0f0") for i in range(columnCount)] for j in range(rowCount)])

  listView.setModel(model)
  treeView.setModel(model)
  combobox.setModel(model)
  tableView.setModel(model)
  model.insertRows(0,5)
  #// model.insertRows(2, 5, QtCore.QModelIndex())
  #model.removeRows(1, 5, QtCore.QModelIndex())

  sys.exit(app.exec_())

