from PyQt4 import QtCore, QtGui, uic
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

mwin, bwin = uic.loadUiType("pyqt22_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        self.btn_read.connect(self.btn_write, QtCore.SIGNAL("clicked()"), self.btn_click_write)
        self.btn_read.connect(self.btn_read, QtCore.SIGNAL("clicked()"), self.btn_click_read)
        
    def btn_click_read(self):
        filter = QtCore.QString("All file (*.*);; Text file (*.txt);; XML file (*.xml)")
        filename = QtGui.QFileDialog.getOpenFileName(self, "open a file", "c:/", filter)
        f1 = QtCore.QFile(filename)
        if not f1.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QMessageBox.warning(self, "title", "file not open")
        
        out = QtCore.QTextStream(f1)
        
        self.edit_text.setPlainText(out.readAll())
        
        f1.close()
        
    def btn_click_write(self):
        f1 = QtCore.QFile("test.txt")
        if not f1.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QMessageBox.warning(self, "title", "file not open")
        
        out = QtCore.QTextStream(f1)
        
        text = self.edit_text.toPlainText()
        out << text
        
        f1.flush()
        f1.close()
        
        
if __name__ == "__main__":
    app = QtGui.QApplication()
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())