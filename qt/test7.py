from PyQt4 import QtCore, QtGui
import sys

class abc(object):
    def __init__(self):
        super(abc, self).__init__()
        self._name= "default"

    def name():
        def fget(self): return self._name
        def fset(self, value): self._name = value
        return locals()
    name = property(**name())

    def show(self):
        print("\n")
        classes = self.__class__.__mro__
        for cls in classes:
            for k, v in cls.__dict__.iteritems():
                #print(k, v)
                if isinstance(v, property):
                    print (k)
 

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("hello")

    b = QtGui.QLabel()
    b.setText("Hello")
    #b.show()
    #b.resize(300,300)
    
    #sys.exit( app.exec_() )
    a = abc()
    a.show()
               
