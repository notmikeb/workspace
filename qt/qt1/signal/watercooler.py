import sys
import PyQt4
import person
from PyQt4 import QtCore, QtGui


def test():
    p1 = person.Person("Sally")
    p2 = person.Person("Bob")
    p3 = person.Person("John")
    p1.speaker.connect(p2.listen)
    p2.speaker.connect(p3.listen)
    p1.gossip("hello")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mwin = QtGui.QMainWindow()
    test()
    mwin.show()
    sys.exit(app.exec_())