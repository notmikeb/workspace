from PyQt4 import QtCore, QtGui, uic, QtSql
import sys
import sqlite3

# url https://www.youtube.com/watch?v=ZylRxvudgtk&t=1872s

mwin, bwin = uic.loadUiType("listw.ui")

mrow, brow = uic.loadUiType("listi.ui")

class myrow(mrow, brow):
    def __init__(self):
        super(myrow, self).__init__()
        self.setupUi(self)

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        self.btn2.setEnabled(False)

        for i in range(5):
             a = myrow()
             self.vlayout.addWidget(a)
        
        self.btn3.clicked.connect(self.add_row)
    def add_row(self):
        self.vlayout.addWidget(myrow())	


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())		