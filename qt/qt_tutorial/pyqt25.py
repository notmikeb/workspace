from PyQt4 import QtCore, QtGui, uic
import sys

mwin, bwin = uic.loadUiType("pyqt22_ui.ui")

class mywin(QtGui.QWidget):
    def __init__(self):
        super(mywin, self).__init__()
        timer = QtCore.QTimer(self)
        timer.connect(timer, QtCore.SIGNAL("timeout()"), self.myfunction)
        self.value = 1
        timer.start(1000)
        layout = QtGui.QBoxLayout(1)
        self.label = QtGui.QLabel()
        layout.addWidget(self.label)
        self.setLayout (layout)
        
    def myfunction(self):
        print("trigger {}".format(self.value))
        self.setWindowTitle("trigger {}".format(self.value))
        self.value += 1
        time = QtCore.QTime.currentTime()

        if time.second() %2 == 0:
            time_text = time.toString("hh : mm : ss")
        else:
            time_text = time.toString("hh   mm   ss")
        self.label.setText(time_text)

        
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())