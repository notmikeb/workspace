import sys
from PyQt4.QtCore import QDir, QMimeData, Qt, QTemporaryFile, QUrl
from PyQt4.QtGui import *

class Window(QLabel):

    def __init__(self, parent = None):

        QLabel.__init__(self, parent)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            drag = QDrag(self)
            data = QMimeData()
            data.setData("text/plain", str(self.text()))

            path = QDir.tempPath() + "/hello.txt"
            f = open(path, "w")
            f.write("Hello world!")
            f.close()
            data.setUrls([QUrl.fromLocalFile(path)])
            drag.setMimeData(data)
            drag.exec_()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.setText("Drag me...")
    window.show()

    sys.exit(app.exec_())
