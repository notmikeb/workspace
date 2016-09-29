import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QMyLineEdit(QLineEdit):
  def __init__(self):
    super(QMyLineEdit,self).__init__()
    print("init done")
    self.setEchoMode(QLineEdit.Password)
    self.returnPressed.connect(self.on_returnPress)
  def on_returnPress(self):
    print("return press {}".format(self.text()))
    

app = QApplication(sys.argv)

w = QMainWindow()

w.setWindowTitle("PyQT python widget")

v = QVBoxLayout()
b = QHBoxLayout()
b.addStretch(1)
frame = QWidget(w)
frame.setLayout(v)
k = QWidget()
k.setLayout(b)
v.addWidget(k)
textbox = QMyLineEdit()
label = QLabel(text="hello")
b.addWidget(textbox)
b.addWidget(label)
b.addWidget(QLabel(text="password"))

v.addWidget(QLabel(text="mycar"))
v.addWidget(QLabel(text="your car"))
v.addWidget(QLabel(text="his car"))

frame.setGeometry(0,0,300,150)
w.resize(300,150)
w.show()

sys.exit(app.exec_())
