import sys, os
import typing
from PyQt6 import QtCore

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QMenuBar, QMenu, QVBoxLayout, QSizePolicy, QDialog, QPushButton, QLabel
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QCloseEvent

class SaveFileDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.resize(400,94)
        self.setWindowTitle("Unsaved changes")

        self.saveButton = QPushButton(parent=self)
        self.saveButton.setGeometry(QtCore.QRect(10, 50, 121, 31))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("Save")

        self.dontsaveButton = QPushButton(parent=self)
        self.dontsaveButton.setGeometry(QtCore.QRect(140, 50, 121, 31))
        self.dontsaveButton.setObjectName("dontsaveButton")
        self.dontsaveButton.setText("Don\'t save")

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QtCore.QRect(270, 50, 121, 31))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Cancel")

        self.questionLabel = QLabel(parent=self)
        self.questionLabel.setGeometry(QtCore.QRect(10, 10, 381, 21))
        self.questionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.questionLabel.setObjectName("questionLabel")
        self.questionLabel.setText("There are unsaved changes in file. Would you like to save them?")

        self.saveOption = -1

        self.saveButton.clicked.connect(self.saveFile)
        self.dontsaveButton.clicked.connect(self.dontSaveFile)
        self.cancelButton.clicked.connect(self.cancel)


    def saveFile(self):
        self.saveOption = 0
        self.accept()
    
    def dontSaveFile(self):
        self.accept()
    
    def cancel(self):
        self.saveOption = 1
        self.accept()

class TextEditorWindow(QMainWindow):
    def __init__(self, filePath):
        super().__init__()
        self.iconPath = os.path.join(os.getcwd(),"Icons")
        self.filePath = filePath

        self.setWindowTitle(os.path.basename(filePath))
        self.resize(800,600)

        self.centralEditWidget = QWidget()
        self.centralEditWidget.setObjectName("centralEditWidget")
        self.setCentralWidget(self.centralEditWidget)

        self.centralLayout = QVBoxLayout(self.centralEditWidget)

        self.textEdit = QTextEdit(parent=self.centralEditWidget)
        self.textEdit.setGeometry(QRect(10, 0, self.centralEditWidget.width(), self.centralEditWidget.height()))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.openFileFunc()
        self.changedText = False
        
        if not self.changedText:
            self.textEdit.textChanged.connect(self.onTextChanged)

        self.centralLayout.addWidget(self.textEdit)

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
    
    def onTextChanged(self):
        self.setWindowTitle("* "+self.windowTitle())
        self.changedText = True
        self.textEdit.textChanged.disconnect()
    
    def openFileFunc(self):
        with open(self.filePath, 'r') as file:
            self.originalText = file.read()
            self.textEdit.setText(self.originalText)

    def saveFileFunc(self):
        with open(self.filePath, 'w') as file:
            file.write(self.textEdit.toPlainText())
    
    def saveFileAsFunc():
        return 0        
    
    def saveOptions(self):
        if self.changedText:
            saveFileDialog = SaveFileDialog()
            saveFileDialog.exec()
            option = saveFileDialog.saveOption
            if option == 0:
                self.saveFileFunc()
            if option == 1:
                return 0
            else:
                return 1
        else:
            return 1
        
    def closeWindowFunc(self):
        if self.saveOptions() == 1:
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

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.saveOptions() == 1:
            a0.accept()
        else:
            a0.ignore()


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = TextEditorWindow(os.path.join(os.getcwd(), "test1.txt"))
    window.show()
    sys.exit(app.exec())
