from PyQt4 import QtCore, QtGui, uic, QtSql
import sys
import sqlite3

# url https://www.youtube.com/watch?v=ZylRxvudgtk&t=1872s

mwin, bwin = uic.loadUiType("personbrowser_ui.ui")

class mywin(mwin, bwin):
    def __init__(self):
        super(mywin, self).__init__()
        self.setupUi(self)
        #self.btn_new.toggle()
        #self.btn_save.hide()
        self.connect(self.btn_cancel, QtCore.SIGNAL("clicked()"), self.on_pressed_cancel)
        self.connect(self.btn_save, QtCore.SIGNAL("clicked()"), self.on_pressed_save)
        self.connect(self.btn_new, QtCore.SIGNAL("clicked()"), self.on_pressed_new)
        self.connect(self.btn_previous, QtCore.SIGNAL("clicked()"), self.on_pressed_previous)
        self.connect(self.btn_next, QtCore.SIGNAL("clicked()"), self.on_pressed_next)

        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("C:\Users\dalone\PycharmProjects\workspace\qt\qt1\persons.db")
        self.db.open()
        self.query = QtSql.QSqlQuery(self.db)
        self.query.exec_("SELECT id, name, email, birthdate from persons")

        if self.query.isActive():
            self.query.first()
            self.on_update_edit()

    def on_update_edit(self):
        print(self.query.value(0).toString())
        self.edit_name.setText(self.query.value(1).toString())
        self.edit_email.setText(self.query.value(2).toString())
        self.date_birthdate.setDate( self.query.value(3).toDate())
        pass
    def on_pressed_new(self):
        pass
    def on_pressed_cancel(self):
        self.btn_new.show()

    def on_pressed_save(self):
        print ("{} {} {} {}".format(self.edit_name.text(), self.edit_email.text(), self.date_birthdate.text(), self.query.value(0).toString()))
        id_old = self.query.value(0)
        updateQuery = QtSql.QSqlQuery(self.db)
        updateQuery.prepare("UPDATE persons SET name = :name, email = :email, birthdate = :birthdate WHERE id = :id")
        updateQuery.bindValue(":id", id_old)
        updateQuery.bindValue(":name", self.edit_name.text())
        updateQuery.bindValue(":email", self.edit_email.text())
        updateQuery.bindValue(":birthdate", self.date_birthdate.text())
        if not updateQuery.exec_():
            self.statusbar.showMessage(QtCore.QString() + updateQuery.lastError().text())
        print(updateQuery.lastError().text())

        #self.query.exec_("SELECT id, name, email, birthdate FROM persons")
        self.query.exec_("SELECT id, name, email, birthdate from persons")
        self.query.first()
        while id_old != self.query.value(0):
            if not self.query.next():
                break
        self.on_update_edit()

    def on_pressed_previous(self):
        if not self.query.previous():
            self.query.last()
        self.on_update_edit()

    def on_pressed_next(self):
        if not self.query.next():
            self.query.first()
        self.on_update_edit()
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    m1 = mywin()
    m1.show()
    sys.exit(app.exec_())