import sys
from PyQt4 import QtCore, QtGui
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    model = QtGui.QDirModel()
    view = QtGui.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
sys.exit(app.exec_())

