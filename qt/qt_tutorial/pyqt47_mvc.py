from PyQt4 import QtCore, QtGui, uic
import sys
import sys

# tutorial from https://www.youtube.com/watch?v=uDC9L4T59bM

mwin, bwin = uic.loadUiType("pyqt47_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        self.model = QtGui.QStringListModel()
        list = QtCore.QStringList()
        list << "daylong" << "paul" << "jerry"
        self.model.setStringList(list)
        self.list_name.setModel(self.model)
        self.cob_name.setModel(self.model)
        self.btn_add.clicked.connect(self.on_press_add)
        self.btn_insert.clicked.connect(self.on_press_insert)
        self.btn_del.clicked.connect(self.on_press_del)

    def on_press_add(self):
        print("add")
        row = self.model.rowCount()
        self.model.insertRows(row, 1)

        index = self.model.index(row)
        self.list_name.setCurrentIndex(index)
        self.list_name.edit(index)

    def on_press_del(self):
        print("del")
        rows = self.list_name.selectedIndexes()
        if len(rows) > 0:
            for i in rows:
                print repr(i)
                self.model.removeRows(i.row(), 1)


    def on_press_insert(self):
        print("insert")
        row = self.list_name.selectedIndexes()
        if len(row) > 0:
            self.model.insertRows( row[0].row()+1, 1)

            index = self.model.index(row[0].row()+1)
            self.list_name.setCurrentIndex(index)
            self.model.setData(index, QtCore.QVariant("haha"))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())