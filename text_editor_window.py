import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QMenuBar, QMenu, QDialog, QPushButton, QLabel, QDateEdit, QTimeEdit
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QIcon, QAction

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
        self.setFixedSize(511,434)

        self.centralNoteWidget = QWidget()
        self.setCentralWidget(self.centralNoteWidget)

        self.dateLabel = QLabel(parent=self.centralNoteWidget)
        self.dateLabel.setGeometry(QRect(10, 10, 49, 31))
        self.dateLabel.setText("Date:")

        self.dateEdit = QDateEdit(parent=self.centralNoteWidget)
        self.dateEdit.setGeometry(QRect(50, 11, 161, 31))
        self.dateEdit.setCalendarPopup(True)

        self.timeLabel = QLabel(parent=self.centralNoteWidget)
        self.timeLabel.setGeometry(QRect(240, 10, 49, 31))
        self.timeLabel.setText("Time:")

        self.timeEdit = QTimeEdit(parent=self.centralNoteWidget)
        self.timeEdit.setGeometry(QRect(280, 10, 161, 31))
        self.timeEdit.setCalendarPopup(False)

        self.noteLabel = QLabel(parent=self.centralNoteWidget)
        self.noteLabel.setGeometry(QRect(10, 50, 49, 16))
        self.noteLabel.setText("Note:")

        self.noteEdit = QTextEdit(parent=self.centralNoteWidget)
        self.noteEdit.setGeometry(QRect(10, 80, 491, 281))

        self.pushButton = QPushButton(parent=self.centralNoteWidget)
        self.pushButton.setGeometry(QRect(350, 370, 151, 31))
        self.pushButton.setText("Save and close note")

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 22))

        self.menuFile = QMenu("File")

        self.actionOpen = QAction("Open")
        self.actionSave = QAction("Save")
        self.actionClose = QAction("Close")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClose)

        self.menuEdit = QMenu("Edit")

        self.actionCut = QAction("Cut")
        self.actionCopy = QAction("Copy")
        self.actionPaste = QAction("Paste")
        self.actionClear = QAction("Clear")
        self.actionUndo = QAction("Undo")
        self.actionRedo = QAction("Redo")

        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionClear)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.setMenuBar(self.menubar)


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = TextEditorWindow()
    window.show()
    sys.exit(app.exec())
