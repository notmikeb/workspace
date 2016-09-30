from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import * 
import sys

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
  model = PaletteListModel([red,green, blue])

  listView.setModel(model)
  treeView.setModel(model)
  combobox.setModel(model)
  tableView.setModel(model)
  sys.exit(app.exec_())
