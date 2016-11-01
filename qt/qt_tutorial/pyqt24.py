from PyQt4 import QtCore, QtGui, uic
import sys

mwin, bwin = uic.loadUiType("pyqt22_ui.ui")

class mywin(QtGui.QWidget):
    value = 1
    def __init__(self):
        super(mywin, self).__init__()
        #self.setupUi(self)
        timer = QtCore.QTimer(self)
        timer.connect(timer, QtCore.SIGNAL("timeout()"), self.myfunction)
        self.value = 1
        timer.start(5000)
    def myfunction(self):
        print("trigger {}".format(self.value))
        self.setWindowTitle("trigger {}".format(self.value))
        self.value += 1
        
        
if __name__ == "__main__":
    app = QtGui.QApplication()
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())