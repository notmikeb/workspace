import sys
from PyQt4 import QtGui, QtCore


class TreeWidget(QtGui.QTreeWidget):
     def __init__(self, parent=None):
         QtGui.QTreeWidget.__init__(self, parent)
         self.header().setHidden(True)
         self.setSelectionMode(self.ExtendedSelection)
         self.setDragDropMode(self.InternalMove)
         self.setDragEnabled(True)
         self.setDropIndicatorShown(True)
         def add(num):
             item = QtGui.QTreeWidgetItem(
                     self, QtCore.QStringList('Item(%i)' % num))
             for i in xrange(1, 4):
                 QtGui.QTreeWidgetItem(
                     item, QtCore.QStringList('Child(%i,%i)' % (num, i)))
             item.setExpanded(True)
         for i in xrange(1, 3):
             add(i)

     def dropEvent(self, event):
         if event.source() == self:
             QtGui.QAbstractItemView.dropEvent(self, event)

     def dropMimeData(self, parent, row, data, action):
         if action == QtCore.Qt.MoveAction:
             return self.moveSelection(parent, row)
         return False

     def moveSelection(self, parent, position):
         # self.selectedIndexes() is the selected QTreeWidgets' QModelIndex
         # position type:int and position type:QTreeWidget is the target to put          

         # save the selected items' persistentQindex. if we use QModelIndex, it will change after 1 moved
         selection = [QtCore.QPersistentModelIndex(i)
                      for i in self.selectedIndexes()]
         print("{} {} {}".format(position, i, QtCore.QPersistentModelIndex(i)))
         parent_index = self.indexFromItem(parent)  #from parent type:TreeWidgetItem to get its QModelIndex
         if parent_index in selection:
             return False

         # save the drop location in case it gets moved since it doesn't exist yet (no previous item)
         target = self.model().index(position, 0, parent_index).row() # (row,column=0, index) to get the child's QModelIndex
         print("position {} target {}".format(position, target)) # target sometimes is -1 when the row is lastone or empty
         if target < 0:
             target = position

         # remove the selected items
         taken = []
         for index in reversed(selection):
             #index is a QPersistentModelIndex, we need QModelIndex. both are 1-1 mapping
             print("index.row {} {} type(position):{}".format(index.row(), type(index), type(position)))
             item = self.itemFromIndex(QtCore.QModelIndex(index))
             # indexFromItem vs ItemFromIndex could switch betwen WtreeItem and QModelIndex
             if item is None or item.parent() is None:
                 taken.append(self.takeTopLevelItem(index.row()))
             else:
                 taken.append(item.parent().takeChild(index.row()))

         # insert the selected items at their new positions
         while taken:
             if position == -1:
                 # append the items if position not specified
                 if parent_index.isValid():
                     parent.insertChild(
                         parent.childCount(), taken.pop(0))
                 else:
                     self.insertTopLevelItem(
                         self.topLevelItemCount(), taken.pop(0))
             else:
		# insert the items at the specified position
                 if parent_index.isValid():
                     parent.insertChild(min(target,
                         parent.childCount()), taken.pop(0))
                 else:
                     self.insertTopLevelItem(min(target,
                         self.topLevelItemCount()), taken.pop(0))
         return True


if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     tree = TreeWidget()
     tree.resize(200, 300)
     tree.move(300, 300)
     tree.show()
     sys.exit(app.exec_())
