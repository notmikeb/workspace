import sys
from PyQt4 import QtGui, QtCore

class Button(QtGui.QPushButton):
    def __init__(self, parent):
        super(Button, self).__init__(parent)
        self.setAcceptDrops(True)
        #self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(Button, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(Button, self).dragMoveEvent(event)

    def dropEvent(self, event):
        accept = False
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if len(str(url.toLocalFile())) > 0:
                    print str(url.toLocalFile())
                    self.setText( str(url.toLocalFile()))
                    accept = True
            event.acceptProposedAction()
        else:
            super(Button,self).dropEvent(event)

class MyWindow(QtGui.QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(100,100,300,400)
        self.setWindowTitle("Filenames")

        self.lbl = QtGui.QLabel()
        self.lbl.setText("Drag a local path to the button to Change window title !")
        self.btn = Button(self)
        self.btn.setGeometry(QtCore.QRect(90, 90, 61, 51))
        self.btn.setText("Change Me!")
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.lbl)
        layout.addWidget(self.btn)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
