# https://www.youtube.com/watch?v=d0CDMtfefB4
# Try to convert c++ qt demo program to pyqt script

from PyQt4 import QtGui, QtCore, uic

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

# use pyrcc4 -o res1_rc.py res1_rc.qrc
mwin, bwin = uic.loadUiType("mymove_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        #self.lblMouse.connect(self.lblMouse, QtCore.SIGNAL("mouseMoveEvent(QMouseEvent)"), self.mouseMove)
        self.label.setMouseTracking(True)
        self.label.mouseMoveEvent = self.mouseMove
        self.label.mousePressEvent = self.mousePress
        self.label.mouseReleaseEvent = self.mouseRelease
        self.label.leaveEvent = self.mouseLeave
    
    def mouseMove(self, event):
        print("mouseMove ", event)
        print(event)
        self.lblMouse_pos.setText(QString("X = {}, Y = {}".format(event.pos().x(), event.pos().y())))
        self.lbMouse_status.setText("Mouse Move !")
    
    def mousePress(self, event):
        print("mousePress ", event)
        self.lbMouse_status.setText("Mouse Press !")

    def mouseRelease(self, event):
        print("mouseRelease ", event)        
        self.lbMouse_status.setText("Mouse Release !")
    def mouseLeave(self, event):
        self.lbMouse_status.setText("Mouse Left !")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    
    app.exec_()          