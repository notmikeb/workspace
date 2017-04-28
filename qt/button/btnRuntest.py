import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

## https://www.tutorialspoint.com/pyqt/pyqt_qpushbutton_widget.htm

class Form(QDialog):
   def __init__(self, parent=None):
      super(Form, self).__init__(parent)
        
      layout = QVBoxLayout()
      self.b1 = QPushButton("Button1")
      self.b1.setCheckable(True)
      self.b1.toggle()
      self.b1.clicked.connect(lambda:self.whichbtn(self.b1))
      self.b1.clicked.connect(self.btnstate)
      layout.addWidget(self.b1)
        
      self.b2 = QPushButton()
      self.b2.setIcon(QIcon(QPixmap("python.gif")))
      self.b2.clicked.connect(lambda:self.whichbtn(self.b2))
      layout.addWidget(self.b2)
      self.setLayout(layout)
      self.b3 = QPushButton("Disabled")
      self.b3.setEnabled(False)
      layout.addWidget(self.b3)
        
      self.b4 = QPushButton("&Default")
      self.b4.setDefault(True)
      self.b4.clicked.connect(lambda:self.whichbtn(self.b4))
      layout.addWidget(self.b4)
      
      self.setWindowTitle("Button demo")

   def btnstate(self):
      if self.b1.isChecked():
         print "button pressed"
      else:
         print "button released"
            
   def whichbtn(self,b):
      print "clicked button is "+b.text()
      import subprocess
      from subprocess import PIPE, Popen, STDOUT
      cmd = "run.bat"
      print "*" * 10 + "stdout"
      p = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
      o = p.stdout.read()
      print o
      print "*" * 10 + "stderr"
      j = p.stderr.read()
      print j
      print "*" * 10

def main():
   app = QApplication(sys.argv)
   ex = Form()
   ex.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()