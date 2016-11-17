import PyQt4
from PyQt4 import QtCore, QtGui
import sys


class Person(QtCore.QObject):
    speaker = QtCore.pyqtSignal(QtCore.QString, name = "speaker(QtCore.QString)")

    def __init__(self, name):
        super(Person, self).__init__()
        self.name = name

    def gossip(self, msg):
        self.speaker.emit(QtCore.QString(msg))

    def listen(self, msg):
        print("{} hears {} ".format(self.name, msg))
        self.speaker.emit(msg)



