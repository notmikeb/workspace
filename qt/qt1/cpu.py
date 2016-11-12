import sys

from PyQt4 import QtGui, QtCore

import cpuprogress


class MainClass(QtGui.QMainWindow, cpuprogress.Ui_MainUiWindow):
    def __init__(self, parent = None):
        super(MainClass, self).__init__()
        self.setupUi(self)
        self.threadclass = ThreadClass()
        self.threadclass.start()
        self.connect(self.threadclass, QtCore.SIGNAL('CPU_VALUE'), self.updateProgressBar)

    def updateProgressBar(self,val):
        #val = psutil.cpu_percent()
        self.progressBar.setValue(val)

class ThreadClass(QtCore.QThread):
    def __init__(self, parent = None):
        super(ThreadClass, self).__init__(parent)
    def run(self):
        while 1:
            val = psutil.cpu_percent(interval = 1)
            print val
            self.emit(QtCore.SIGNAL('CPU_VALUE'), val)


if __name__ == "__main__":
  a = QtGui.QApplication(sys.argv)
  m = MainClass()
  m.show()
  a.exec_()




