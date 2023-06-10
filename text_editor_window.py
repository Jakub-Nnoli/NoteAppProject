import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QMenuBar, QMenu
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence

class TextEditorWindow(QMainWindow):
    def __init__(self, filePath):
        super().__init__()
        self.iconPath = os.path.join(os.getcwd(),"Icons")
        self.filePath = filePath

        self.setWindowTitle('Notepad')
        self.resize(800, 600)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QTextEdit(parent=self.centralwidget)
        self.textEdit.setGeometry(QRect(10, 0, 781, 571))
        self.textEdit.setObjectName("textEdit")
        self.openFileFunc()

        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")

        self.menuFile = self.createMenu("menuFile", "File")
        self.menuEdit = self.createMenu("menuEdit", "Edit")

        self.actionSave = self.createAction("actionSave", "Save", self.saveFileFunc, "SaveIcon.png", QKeySequence.StandardKey.Save)
        self.actionSave_As = self.createAction("actionSave_As", "Save As", self.saveFileAsFunc, "SaveIcon.png", QKeySequence.StandardKey.SaveAs)
        self.actionClose = self.createAction("actionClose", "Close", self.closeWindowFunc, "CloseIcon.png", QKeySequence.StandardKey.Close)
        self.actionCut = self.createAction("actionCut", "Cut", self.cutSelectedFunc, "CutIcon.png", QKeySequence.StandardKey.Cut)
        self.actionCopy = self.createAction("actionCopy", "Copy", self.copySelectedFunc, "CopyIcon.png", QKeySequence.StandardKey.Copy)
        self.actionPaste = self.createAction("actionPaste", "Paste", self.pasteTextFunc, "PasteIcon.png", QKeySequence.StandardKey.Paste)
        self.actionSelect_All = self.createAction("actionSelect_All", "Select All", self.selectAllFunc, actionKeySequence=QKeySequence.StandardKey.SelectAll)
        self.actionUndo = self.createAction("actionUndo", "Undo", self.undoActionFunc, "UndoIcon.png", QKeySequence.StandardKey.Undo)
        self.actionRedo = self.createAction("actionRedo", "Redo", self.redoActionFunc, "RedoIcon.png", QKeySequence.StandardKey.Redo)

        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        
        self.setMenuBar(self.menubar)

    def createMenu(self, menuName:str, menuText:str):
        menu = QMenu(parent=self.menubar)
        menu.setObjectName(menuName)
        menu.setTitle(menuText)
        return menu

    def createAction(self, actionName:str, actionText:str, actionFunc:callable, actionIconName:str=None, actionKeySequence:QKeySequence=None):
        action = QAction()
        action.setObjectName(actionName)
        action.setText(actionText)
        if actionIconName:
            actionIcon = os.path.join(self.iconPath, actionIconName)
            action.setIcon(QIcon(actionIcon))
        if actionKeySequence:
            action.setShortcut(actionKeySequence)
        action.triggered.connect(actionFunc)
        return action
    
    def openFileFunc(self):
        with open(self.filePath, 'r') as file:
            self.originalText = file.read()
            self.textEdit.setText(self.originalText)

    def saveFileFunc(self):
        with open(self.filePath, 'w') as file:
            file.write(self.textEdit.toPlainText())
    
    def saveFileAsFunc():
        return 0
    
    def closeWindowFunc(self):
        if self.textEdit.toPlainText() != self.originalText:
            self.saveFileFunc()
        self.close()
    
    def cutSelectedFunc(self):
        self.textEdit.cut()
    
    def copySelectedFunc(self):
        self.textEdit.copy()
    
    def pasteTextFunc(self):
        self.textEdit.paste()
    
    def selectAllFunc(self):
        self.textEdit.selectAll()
    
    def undoActionFunc(self):
        self.textEdit.undo()
    
    def redoActionFunc(self):
        self.textEdit.redo()


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = TextEditorWindow()
    window.show()
    sys.exit(app.exec())
