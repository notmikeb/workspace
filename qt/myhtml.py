from PyQt4 import QtCore, QtGui, uic
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Mywin(QWidget):
    def __init__(self):
        super(Mywin, self).__init__()
        layout = QBoxLayout(0, self)
        ql = QLabel("<h2><b>hello</b></h2><font color=\"#ff0000\"><h3><i>world</i></h3></font>")
        layout.addWidget(ql)
        self.setWindowTitle("dalong long live")
        self.setLayout(layout)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw1 = Mywin()
    mw1.show()
    app.exec_()