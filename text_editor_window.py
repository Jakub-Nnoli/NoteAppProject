import sys, os
from datetime import date, datetime
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QMenuBar, QMenu, QDialog, QPushButton, QLabel, QDateEdit, QTimeEdit, QCheckBox
from PyQt6.QtCore import QRect, Qt, QDate
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QCloseEvent

class SaveNoteDialog(QDialog):
    def __init__(self):
        super().__init__()
    
        self.iconPath = os.path.join(os.getcwd(),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(400,94)

        self.saveButton = QPushButton(parent=self)
        self.saveButton.setGeometry(QRect(10, 50, 121, 31))
        self.saveButton.setText("Save")

        self.dontsaveButton = QPushButton(parent=self)
        self.dontsaveButton.setGeometry(QRect(140, 50, 121, 31))
        self.dontsaveButton.setText("Don\'t save")

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QRect(270, 50, 121, 31))
        self.cancelButton.setText("Cancel")

        self.questionLabel = QLabel(parent=self)
        self.questionLabel.setGeometry(QRect(10, 10, 381, 21))
        self.questionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.questionLabel.setText("There are unsaved changes in note. Would you like to save them?")

        self.saveOption = -1

        self.saveButton.clicked.connect(self.saveNote)
        self.dontsaveButton.clicked.connect(self.dontSaveNote)
        self.cancelButton.clicked.connect(self.cancel)


    def saveNote(self):
        self.saveOption = 0
        self.accept()
    
    def dontSaveNote(self):
        self.accept()
    
    def cancel(self):
        self.saveOption = 1
        self.accept()

class TextEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.iconPath = os.path.join(os.getcwd(),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(511,463)

        self.centralNoteWidget = QWidget()
        self.setCentralWidget(self.centralNoteWidget)

        self.reminderCheckBox = QCheckBox(parent=self.centralNoteWidget)
        self.reminderCheckBox.setGeometry(QRect(10, 10, 181, 21))
        self.reminderCheckBox.setText("Add reminder to note")
        self.reminderCheckBox.stateChanged.connect(self.enableReminder)

        self.dateLabel = QLabel(parent=self.centralNoteWidget)
        self.dateLabel.setGeometry(QRect(10, 40, 49, 31))
        self.dateLabel.setText("Date:")

        self.dateEdit = QDateEdit(parent=self.centralNoteWidget)
        self.dateEdit.setGeometry(QRect(50, 40, 161, 31))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setEnabled(False)
        self.dateEdit.setDate(QDate(date.today()))

        self.timeLabel = QLabel(parent=self.centralNoteWidget)
        self.timeLabel.setGeometry(QRect(240, 40, 49, 31))
        self.timeLabel.setText("Time:")

        self.timeEdit = QTimeEdit(parent=self.centralNoteWidget)
        self.timeEdit.setGeometry(QRect(280, 40, 161, 31))
        self.timeEdit.setCalendarPopup(False)
        self.timeEdit.setEnabled(False)

        self.noteLabel = QLabel(parent=self.centralNoteWidget)
        self.noteLabel.setGeometry(QRect(10, 80, 49, 16))
        self.noteLabel.setText("Note:")

        self.noteEdit = QTextEdit(parent=self.centralNoteWidget)
        self.noteEdit.setGeometry(QRect(10, 110, 491, 281))

        self.changedNote = False
        if not self.changedNote:
            self.timeEdit.timeChanged.connect(self.onNoteChanged)
            self.dateEdit.dateChanged.connect(self.onNoteChanged)
            self.noteEdit.textChanged.connect(self.onNoteChanged)

        self.pushButton = QPushButton(parent=self.centralNoteWidget)
        self.pushButton.setGeometry(QRect(350, 400, 151, 31))
        self.pushButton.setText("Save note")

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 22))

        self.menuNote = QMenu("Note")
        self.menuEdit = QMenu("Edit note")

        self.actionSave = QAction("Save")
        self.actionClose = QAction("Close")

        self.actionCut = QAction("Cut")
        self.actionCopy = QAction("Copy")
        self.actionPaste = QAction("Paste")
        self.actionClear = QAction("Clear")
        self.actionUndo = QAction("Undo")
        self.actionRedo = QAction("Redo")

        self.menuNote.addAction(self.actionSave)
        self.menuNote.addAction(self.actionClose)

        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionClear)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.menubar.addAction(self.menuEdit.menuAction())

        self.setMenuBar(self.menubar)
    
    def onNoteChanged(self):
        self.setWindowTitle("* "+self.windowTitle())
        self.changedText = True
        self.timeEdit.timeChanged.disconnect()
        self.dateEdit.dateChanged.disconnect()
        self.noteEdit.textChanged.disconnect()

    def createAction(self, actionText:str, actionFunc:callable, actionIcon:str=None, actionKeySequence:QKeySequence=None):
        action = QAction()
        action.setText(actionText)
        action.setIcon(QIcon(actionIcon))
        if actionKeySequence:
            action.setShortcut(actionKeySequence)
        action.triggered.connect(actionFunc)
        return action

    def enableReminder(self):
        if self.reminderCheckBox.checkState() == Qt.CheckState.Checked:
            self.dateEdit.setEnabled(True)
            self.timeEdit.setEnabled(True)
        else:
            self.dateEdit.setDate(QDate(date.today()))
            self.dateEdit.setEnabled(False)
            self.timeEdit.setEnabled(False)

    def saveNote(self):
        return 0
    
    def closeNote(self):
        return 0
    
    def cutAction(self):
        return 0
    
    def copyAction(self):
        return 0
    
    def pasteAction(self):
        return 0
    
    def clearAction(self):
        return 0
    
    def undoAction(self):
        return 0
    
    def redoAction(self):
        return 0
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        return super().closeEvent(a0)


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = TextEditorWindow()
    window.show()
    sys.exit(app.exec())
