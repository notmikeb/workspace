import sys
import os.path as op
from os.path import isdir

from PyQt4 import QtGui as QtWidgets
from PyQt4 import QtCore, QtGui

class LineEditWithToolButtons(QtWidgets.QLineEdit):
    """ Line edit to which tool buttons (with icons) can be attached.
    """
    
    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)
        self._leftButtons = []
        self._rightButtons = []
    
    def addButtonLeft(self, icon, willHaveMenu=False):
        return self._addButton(icon, willHaveMenu, self._leftButtons)
    
    def addButtonRight(self, icon, willHaveMenu=False):
        return self._addButton(icon, willHaveMenu, self._rightButtons)
    
    def _addButton(self, icon, willHaveMenu, L):
        # Create button
        button = QtWidgets.QToolButton(self)
        L.append(button)
        # Customize appearance
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(16,16))
        button.setStyleSheet("QToolButton { border: none; padding: 0px; }")        
        #button.setStyleSheet("QToolButton { border: none; padding: 0px; background-color:red;}");
        # Set behavior
        button.setCursor(QtCore.Qt.ArrowCursor)
        button.setPopupMode(button.InstantPopup)
        # Customize alignment
        if willHaveMenu:
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            if sys.platform.startswith('win'):
                button.setText(' ')
        # Update self
        self._updateGeometry()
        return button
    
    def setButtonVisible(self, button, visible):
        for but in self._leftButtons:
            if but is button:
                but.setVisible(visible)
        for but in self._rightButtons:
            if but is button:
                but.setVisible(visible)
        self._updateGeometry()
    
    def resizeEvent(self, event):
        QtWidgets.QLineEdit.resizeEvent(self, event)
        self._updateGeometry(True)
    
    def showEvent(self, event):
        QtWidgets.QLineEdit.showEvent(self, event)
        self._updateGeometry()
    
    def _updateGeometry(self, light=False):
        if not self.isVisible():
            return
        
        # Init
        rect = self.rect()
        
        # Determine padding and height
        paddingLeft, paddingRight, height = 1, 1, 0
        #
        for but in self._leftButtons:
            if but.isVisible():
                sz = but.sizeHint()
                height = max(height, sz.height())
                but.move(   1+paddingLeft,
                            (rect.bottom() + 1 - sz.height())/2 )
                paddingLeft += sz.width() + 1
        #
        for but in self._rightButtons:
            if but.isVisible():
                sz = but.sizeHint()
                paddingRight += sz.width() + 1
                height = max(height, sz.height())
                but.move(   rect.right()-1-paddingRight, 
                            (rect.bottom() + 1 - sz.height())/2 )
        
        # Set padding
        ss = "QLineEdit { padding-left: %ipx; padding-right: %ipx} "
        self.setStyleSheet( ss % (paddingLeft, paddingRight) );
        
        # Set minimum size
        if not light:
            fw = QtWidgets.qApp.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
            msz = self.minimumSizeHint()
            w = max(msz.width(), paddingLeft + paddingRight + 10)
            h = max(msz.height(), height + fw*2 + 2)
            self.setMinimumSize(w,h)


class PathInput(LineEditWithToolButtons):
    """ Line edit for selecting a path.
    """
    
    dirChanged = QtCore.pyqtSignal(str)  # Emitted when the user changes the path (and is valid)
    dirUp = QtCore.pyqtSignal()  # Emitted when user presses the up button
    
    def __init__(self, parent):
        LineEditWithToolButtons.__init__(self, parent)
        
        # Create up button
        self._upBut = self.addButtonLeft(QtGui.QIcon(QtGui.QPixmap("pyzo\\pyzo\\tick.png")))
        self._upBut.clicked.connect(self.dirUp)
        
        # To receive focus events
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        # Set completion mode
        self.setCompleter(QtWidgets.QCompleter())
        c = self.completer()
        c.setCompletionMode(c.InlineCompletion)
        
        # Set dir model to completer
        dirModel = QtWidgets.QDirModel(c)
        dirModel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        c.setModel(dirModel)
        
        # Connect signals
        #c.activated.connect(self.onActivated)
        self.textEdited.connect(self.onTextEdited)
        #self.textChanged.connect(self.onTextEdited)
        #self.cursorPositionChanged.connect(self.onTextEdited)
    
    
    def setPath(self, path):
        """ Set the path to display. Does nothing if this widget has focus.
        """
        if not self.hasFocus():
            self.setText(path)
            self.checkValid() # Reset style if it was invalid first
    
    
    def checkValid(self):
        # todo: This kind of violates the abstraction of the file system
        # ok for now, but we should find a different approach someday
        # Check
        text = self.text()
        if 'cleanpath' in globals().keys():
          dir = cleanpath(text)
        else:
          dir = ''
        isvalid = text and isdir(dir) and op.isabs(dir)
        # Apply styling
        ss = self.styleSheet().replace('font-style:italic; ', '')
        if not isvalid:
            ss = ss.replace('QLineEdit {', 'QLineEdit {font-style:italic; ')
        self.setStyleSheet(ss)
        # Return
        return isvalid
    
    
    def event(self, event):
        # Capture key events to explicitly apply the completion and
        # invoke checking whether the current text is a valid directory.
        # Test if QtGui is not None (can happen when reloading tools)
        if QtGui and isinstance(event, QtGui.QKeyEvent):
            qt = QtCore.Qt
            if event.key() in [qt.Key_Tab, qt.Key_Enter, qt.Key_Return]:
                self.setText(self.text()) # Apply completion
                self.onTextEdited() # Check if this is a valid dir
                return True
        return LineEditWithToolButtons.event(self, event)
    
    
    def onTextEdited(self, dummy=None):
        text = self.text()
        if self.checkValid() and 'cleanpath' in globals().keys():            
            self.dirChanged.emit(cleanpath(text))
    
    
    def focusOutEvent(self, event=None):
        """ focusOutEvent(event)
        On focusing out, make sure that the set path is correct.
        """
        if event is not None:
            QtWidgets.QLineEdit.focusOutEvent(self, event)
        if self.parent():
            path = self.parent()._tree.path()
        else:
            path = ''
        self.setPath(path)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    line = PathInput(None)
    line.show()
    sys.exit(app.exec_())