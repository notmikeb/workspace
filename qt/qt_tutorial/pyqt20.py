from PyQt4 import QtCore, QtGui, uic
import sys
import sys
import pyqt20_rc

mwin, bwin = uic.loadUiType("pyqt20_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        item1 = QtGui.QListWidgetItem(QtGui.QIcon(":/images/1.jpg"), "daylong")
        self.list_files.addItem(item1)
        item2 = QtGui.QListWidgetItem(QtGui.QIcon(":/images/2.jpg"), "paul")
        self.list_files.addItem(item2)
        item3 = QtGui.QListWidgetItem(QtGui.QIcon(":/images/3.jpg"), "jerry")
        self.list_files.addItem(item3)
        self.btn_change.connect(self.btn_change, QtCore.SIGNAL("clicked()"), self.change_action)

    def change_action(self):
        QtGui.QMessageBox.information(self, "title", self.list_files.currentItem().text())
        self.list_files.currentItem().setBackgroundColor(QtCore.Qt.yellow)
        self.list_files.currentItem().setTextColor(QtCore.Qt.blue)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())