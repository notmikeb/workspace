from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QWidget

# http://rowinggolfer.blogspot.tw/2010/08/qtextedit-with-autocompletion-using.html

STARTTEXT = ('This TextEdit provides autocompletions for words that have ' +
'more than 3 characters.\nYou can trigger autocompletion using %s\n\n'''% (
QtGui.QKeySequence("Ctrl+E").toString(QtGui.QKeySequence.NativeText)))

class DictionaryCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        words = []
        try:
            f = open("./words.txt","r")
            for word in f:
                words.append(word.strip())
            f.close()
        except IOError:
            print "dictionary not in anticipated location"
        QtGui.QCompleter.__init__(self, words, parent)
class LineInfo(QtGui.QTextEdit):
    def __init__(self, parent = None):
        super(LineInfo, self).__init__(parent)

class CompletionTextEdit(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(CompletionTextEdit, self).__init__(parent)
        self.setMinimumWidth(400)
        self.setPlainText(STARTTEXT)
        self.completer = None
        self.moveCursor(QtGui.QTextCursor.End)
        self.connect(self, QtCore.SIGNAL("cursorPositionChanged()"),self.on_cursorPositionChanged)
        self.neighbor = None
        self.preLineNo = -1

    def setNeighbor(self, n):
        self.neighbor = n

    def setCompleter(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.connect(self.completer,
            QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (completion.length() -
            self.completer.completionPrefix().length())
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion.right(extra))
        self.setTextCursor(tc)
        self.preLineNo = -1 #update neighbor
        self.on_cursorPositionChanged()

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()
    @property
    def textLineUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.LineUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def on_cursorPositionChanged(self):
        print("cursor move")
        currentLineNo = self.textCursor().blockNumber()
        if self.neighbor and self.preLineNo != currentLineNo:
            print self.textLineUnderCursor
            self.neighbor.setText(self.textLineUnderCursor)
            self.preLineNo = currentLineNo

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Backtab):
                event.ignore()
                return

        ## has ctrl-E been pressed??
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
                      event.key() == QtCore.Qt.Key_E)
        if (not self.completer or not isShortcut):
            QtGui.QTextEdit.keyPressEvent(self, event)

        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text().isEmpty():
            # ctrl or shift key on it's own
            return

        eow = QtCore.QString("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=") #end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (not isShortcut and (hasModifier or event.text().isEmpty() or
        completionPrefix.length() < 1 or
        eow.contains(event.text().right(1)))):
            self.completer.popup().hide()
            return

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0,0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!

if __name__ == "__main__":

    app = QtGui.QApplication([])
    completer = DictionaryCompleter()
    layout = QHBoxLayout()
    win = QWidget()

    te = CompletionTextEdit()
    te.setCompleter(completer)
    linfo = LineInfo()
    te.setNeighbor(linfo)

    layout.addWidget(te)
    layout.addWidget(linfo)
    win.setLayout(layout)
    win.show()
    app.exec_()