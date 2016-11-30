from PyQt4 import QtGui
import sys
from PyQt4.QtCore import QString


class mytab(QtGui.QWidget):
    def __init__(self):
        super(mytab, self).__init__()
        self.tabs = QtGui.QTabWidget()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        for i in range(10):
            te1 = QtGui.QTextEdit()
            te1.append(QString("{}".format(i)))
            self.tabs.addTab(te1, "file - {}".format(i))
        p = self.tabs.children()
        print (len(p))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w1 = mytab()
    w1.show()
    sys.exit(app.exec_())