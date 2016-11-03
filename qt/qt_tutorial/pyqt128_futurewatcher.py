from PyQt4 import QtCore, QtGui, uic
import sys
import sys
mwin, bwin = uic.loadUiType("pyqt128_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        self.connect(self.btn_go, QtCore.SIGNAL("clicked()"), self.pressed_btn_go)

    def doTask(self, number):
        QtCore.qDebug("Starting ")
        QtCore.qDebug(str(number))
        max = 10
        for i in range(10):
            QtCore.QThread.currentThread().msleep(50)
            QtCore.qDebug("Processing {}  - {} of {}".format(number, i, max))
        QtCore.qDebug("Stopped {}".format(number))
    def pressed_btn_go(self):
        vector = []

        for i in range(self.spin_num.value()):
            vector.append(i)
        print(repr(vector))

        qpd = QtGui.QProgressDialog()
        qpd.setLabelText("Processing")
        qpd.show()
        qpd.exec_()
        # failed Qt doesn't have QFutureWatcher

        #self.connect(qpd, QtCore.SIGNAL(), self.watcher, self.watcher.)

        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())