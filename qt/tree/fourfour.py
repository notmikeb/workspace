from PyQt4 import QtGui
from PyQt4 import QtCore
import sys

class mywin():
  def __init__(self):
    pass
  def show(self):
    app = QtGui.QApplication(sys.argv)
    self.app = app
    mw = QtGui.QMainWindow()
    #mw.setLayout(layout)
    mw.statusBar()
    self.mw = mw
    
    w = QtGui.QWidget(mw)
    layout = QtGui.QGridLayout()
    for i in range(1, 5):
        for j in range(1, 5):
            b = QtGui.QPushButton()
            b.setText("{}".format((i-1)*4+j))
            b.clicked.connect(self.on_button)
            layout.addWidget(b, i, j)

    w.setLayout(layout)
    w.setGeometry(0,0,200,200)
    #w.setWindowTitle("4x4")
    print("w.show()")
    mw.show()
    sys.exit( app.exec_())
  def on_button(self, arg = None):
      print(type(arg))
      if arg:
          print(arg.getText())
      print(type(self))
      sender = self.app.sender()
      if sender:
          print(sender.text())
          self.mw.statusBar().showMessage(sender.text() + ' was pressed')


if __name__ == "__main__":
   w = mywin()
   w.show()
