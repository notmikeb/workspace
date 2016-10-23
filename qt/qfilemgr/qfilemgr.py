
#inspire from
#https://www.youtube.com/watch?v=92biLZST6Vg&t=69s
#https://www.youtube.com/watch?v=M0PZDrDwdHM&t=598s

from PyQt4.QtCore import *

from PyQt4.QtGui import *
import sys
from PyQt4 import uic, QtCore, QtGui

#ui_main, ui_window = uic.loadUi('qfilemgr_ui.ui')

mode= QFileSystemModel()

mwin, bwin = uic.loadUiType('qfilemgr_ui.ui')

#use loadUiType to get the class of class and its based class

class MyWidget(mwin, bwin):
    def __init__(self, parent = None):
        super(MyWidget, self).__init__()
        # need to setupUi and then show
        self.setupUi(self)
        self.btnadd.connect(self.btnadd, QtCore.SIGNAL("clicked()"), self.pressShow)
        self.btndel.connect(self.btndel, QtCore.SIGNAL("clicked()"), self.pressDel)
        model = QDirModel()
        model.setReadOnly(False)
        model.setSorting(QDir.DirsFirst)
        self.model = model
        self.treefolder.setModel(model)
        
        #QModelIndex
        index = model.index("D:/Users")
        self.treefolder.expand(index)
        self.treefolder.scrollTo(index)
        self.treefolder.setCurrentIndex(index)
        self.treefolder.resizeColumnToContents(0)

        # disable editable
        self.treefolder.setEditTriggers(self.treefolder.NoEditTriggers)
        self.treefolder.connect(self.treefolder.selectionModel(), QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.changeFolder)

        sPath = "D:/Users"
        self.filemodel = QFileSystemModel(self)
        #self.filemodel.setFilter(QDir.NoDotAndDotDot)
        self.filemodel.setRootPath(QString(sPath))
        self.listfile.setModel(self.filemodel)
        
        
        self.show()

    def changeFolder(self, current = None, previous = None):
        print(current, previous)
        if current:
            print(self.model.fileInfo(current).absoluteFilePath())
            spath = self.model.fileInfo(current).absoluteFilePath()
            if self.model.fileInfo(current).isDir():
                self.listfile.setRootIndex(self.filemodel.setRootPath(spath))
        
    def pressShow(self, event = None):
        print("pressShow", event)
        index = self.treefolder.currentIndex()
        if not index.isValid():
            return
        print(index)
        name = QInputDialog.getText(self, "Name", "Enter a name")
        print(name[0])
        if len(name[0]) == 0:
            return
        print(len(name[0]))
        self.model.mkdir(index, name[0])
        
            

    def pressDel(self, event = None):
        print("pressDel", event)
        index = self.treefolder.currentIndex()
        if not index.isValid():
            return
        #self.treefolder.setEditTriggers(self.treefolder.AllEditTriggers )
        # NoEditTriggers causes the mode.rmdir out of order, aka not work
        if self.model.fileInfo(index).isDir():
            print("isDir")
            self.model.rmdir(index)
        else:
            print("not isDir")
            self.model.remove(index)

        #self.treefolder.setEditTriggers(self.treefolder.NoEditTriggers)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MyWidget()
    sys.exit( app.exec_() )
