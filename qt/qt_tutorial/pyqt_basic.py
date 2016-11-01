from PyQt4 import QtCore, QtGui, uic
import sys

mwin, bwin = uic.loadUiType("pyqt22_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        
if __name__ == "__main__":
    app = QtGui.QApplication()
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())