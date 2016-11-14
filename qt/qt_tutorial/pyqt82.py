from PyQt4 import QtCore, QtGui, uic

from PyQt4.QtGui import QGraphicsItem
import sys
import PyQt4
# https://www.youtube.com/watch?v=hgDd2QspuDg

mwin, bwin = uic.loadUiType("pyqt82_ui.ui")

class MySquare(QGraphicsItem):
    def __init__(self):
        super(MySquare, self).__init__()
        self.Pressed = False
        self.setFlags(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return QtCore.QRectF(0,0, 100, 100)

    def paint(self, painter, gitems, widget):
        rec = self.boundingRect()
        brush = QtGui.QBrush(PyQt4.QtCore.Qt.blue)
        if(self.Pressed):
            brush.setColor(PyQt4.QtCore.Qt.red)
        else:
            brush.setColor(PyQt4.QtCore.Qt.blue)
        painter.fillRect(rec, brush)
        painter.drawRect(rec)
    def mousePressEvent(self, event):
        self.Pressed = True
        self.update()
        #super(MySquare).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.Pressed = False
        self.update()
        #super(MySquare).mouseReleaseEvent(event)


class myDialog(mwin, bwin):
    def __init__(self, parent = None):
        super(myDialog, self).__init__(parent)
        self.setupUi(self)

        s = QtGui.QGraphicsScene(self)
        self.square = MySquare()
        self.gview.setScene(s)
        s.addItem(self.square)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    d = myDialog()
    d.show()
    sys.exit(app.exec_())
