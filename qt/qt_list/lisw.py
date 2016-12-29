from PyQt4 import QtCore, QtGui, uic, QtSql
import sys
import sqlite3
import Queue
from threading import Thread
import time

# url https://www.youtube.com/watch?v=ZylRxvudgtk&t=1872s

mwin, bwin = uic.loadUiType("listw.ui")

mrow, brow = uic.loadUiType("listi.ui")

def downloadEnclosures(i, q):
    """This is the worker thread function.
    It processes items in the queue one after
    another.  These daemon threads go into an
    infinite loop, and only exit when
    the main thread ends.
    """
    while True:
        print '%s: Looking for the next enclosure' % i
        cmd, cb = q.get()
        print '%s: Downloading:' % cmd
        # instead of really downloading the URL,
        # we just pretend and sleep
        time.sleep(i + 2)
        if cb:
            cb()
        q.task_done()

class myrow(mrow, brow):
    def __init__(self, q):
        super(myrow, self).__init__()
        self.setupUi(self)
        self.name = ""
        self.q = q
        self.pushButton.clicked.connect(self.execute)
        
    def setName(self, name):
        self.name = "name: {}".format( name)
        self.lbltext.setText(self.name)
    def done(self):
        print "job done name:{}".format(self.name)
    def execute(self):
        self.q.put( ("ls -l", self.done))

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        self.btn2.setEnabled(False)
        self.q = Queue.Queue()
        self.i = 0
        self.f1 = worker = Thread(target=downloadEnclosures, args=(0, self.q,))
        worker.setDaemon(True)
        worker.start()
        
        for i in range(5):
             a = myrow(self.q)
             a.setName(self.i)
             self.i += 1             
             self.vlayout.addWidget(a)
        
        self.btn3.clicked.connect(self.add_row)
    def add_row(self):
        a = myrow(self.q)
        a.setName(self.i)
        self.i += 1
        self.vlayout.addWidget(a)
        self.q.put( ("ls ", a.done))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())		