from PyQt4 import QtGui, QtCore, uic

import sys
'''
https://www.youtube.com/watch?v=Eq7__6y0jwo
'''
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")

    #data
    data = QtCore.QStringList()
    data << "1" << "da" << "apple" << "list"

    listView  = QtGui.QListView()
    listView.show()

    model = QtGui.QStringListModel(data)
    listView.setModel(model)

    combobox = QtGui.QComboBox()
    combobox.setModel(model)
    combobox.show()

    listView2 = QtGui.QListView()
    listView2.setModel(model)
    listView2.show()

    sys.exit(app.exec_())
