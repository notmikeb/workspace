from PyQt4 import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys


class MyListView(QtGui.QListView):
    def __init__(self):
        super(MyListView, self).__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            print("dragEnterEvent")
            event.accept()
            #event.accept()
    def dragMoveEvent(self,event):
        if event.mimeData().hasUrls():
            #event.setDropAction(QtCore.Qt.CopyAction)
            #event.accept()
            pass
        else:
            event.ignore()
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            print("dropEvent")
            for u in event.mimeData().urls():
               print(u) 
            event.acceptProposedAction()
            links = []
            for url in event.mimeData().urls():
                links.append(url.toLocalFile())
            self.emit(QtCore.SIGNAL("dropped"), links)
        elif event.mimeData().hasText():
            print("text")
            print(event.mimeData().text())
            event.acceptProposedAction()
        else:
            super(MyListView, self).dropEvent(event)
        print(repr(event))

class MyWindow(QtGui.QWidget):
    def __init__(self):
         super(MyWindow, self).__init__()
         self.setWindowTitle("qlist")
         self.slist = QtCore.QStringList()
         self.slist.append("daylong")

         self.model = QtGui.QStringListModel()
         self.model.setStringList(self.slist)
         model2 = QtGui.QStringListModel()
 
         list1 = MyListView()
         list1.setAcceptDrops(True)
         list1.dragEnabled()
         list1.setModel(self.model)
         list2 = MyListView()
         list2.setAcceptDrops(True)
         list2.dragEnabled()
         list2.setModel(model2)

         model3 = QtGui.QFileSystemModel()
         view3 = QtGui.QTreeView()
         view3.setModel(model3)
         cp = model3.index(  "/")
         view3.setRootIndex( cp)
         #view3.setRootIndex( cp )
         view4 = QtGui.QListView()
         view4.setModel(model3)
         #view4.setRootIndex( cp )
         view5 = QtGui.QTreeView()
         view5.setModel(model3)
    
         btn = QtGui.QPushButton("my", self)
         self.connect(btn, QtCore.SIGNAL("clicked(bool)"), self.buttonClicked)
         layout = QtGui.QVBoxLayout(self)
         layout.addWidget(list1)
         layout.addWidget(list2)
         layout.addWidget(view3)
         layout.addWidget(view4)
         layout.addWidget(view5)
         layout.addWidget(btn)

         self.setLayout(layout)
         self.connect(list1, QtCore.SIGNAL("dropped"), self.fileDrops)

    def fileDrops(self, l):
        print("fileDrops")
        a = l+ [i for i in self.model.stringList()]
        self.model.setStringList(a)
    def buttonClicked(self, on):
        dialog = QtGui.QFileDialog()
        if dialog.exec_():
            fn = dialog.selectedFiles()
            for f in fn:
                print(f.toUtf8())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("Qlist")
    window = MyWindow()
    window.show()
    sys.exit( app.exec_())
