
from PyQt4 import QtGui, QtCore, uic

from PyQt4.QtGui import *
import sys


# use pyrcc4 -o res1_rc.py res1_rc.qrc

mwin, bwin = uic.loadUiType("myslider_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mwin, self).__init__()
        self.setupUi(self)
        self.horizontalSlider.setValue(59)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    
    app.exec_()    