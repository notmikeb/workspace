from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QTextBlockFormat
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# http://stackoverflow.com/questions/9433375/highlight-specific-line-of-output

class Window(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self._offset = 200
        self._closed = False
        self._maxwidth = self.maximumWidth()
        self.widget = QtGui.QWidget(self)
        self.listbox = QtGui.QListWidget(self.widget)
        self.editor = QtGui.QTextEdit(self)
        self.editor.setStyleSheet("QTextEdit {color:red}")
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.widget)
        layout.addWidget(self.editor)
        self.editor.append("this is line 1")
        self.editor.append("this is line 2")
        self.editor.append("this is line 3")
        self.setLineFormat(1, self.setFormat())

    def setLineFormat(self, lineNumber, format):
        cursor = QTextCursor(self.editor.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(format)
        self.editor.setTextCursor(cursor)

        # with
    def setFormat(self):
        format = QTextBlockFormat()
        format.setBackground(QtCore.Qt.yellow)
        return format
        # or
        #format.clearBackground()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.move(500, 300)
    window.show()
    sys.exit(app.exec_())