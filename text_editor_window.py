import sys, os, subprocess
from datetime import date
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QMenuBar, QMenu, QPushButton, QLabel, QDateEdit, QTimeEdit, QCheckBox, QMessageBox
from PyQt6.QtCore import QRect, Qt, QDate
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QCloseEvent

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from database_modules import Notes

from necessary_dialogs import SaveNoteDialog

class TextEditorWindow(QMainWindow):
    def __init__(self, noteID, userLogin):
        super().__init__()
        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.engine = create_engine(f'sqlite:///{os.path.dirname(sys.argv[0])}/NotepadDatabase.db')

        self.noteID = noteID
        self.userLogin = userLogin

        self.setWindowTitle("NoteApp")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(511,483)

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

        self.loadCurrentNote()
        self.changedNote = False
        self.onNoteSaved()

        self.saveButton = QPushButton(parent=self.centralNoteWidget)
        self.saveButton.setGeometry(QRect(350, 400, 151, 51))
        self.saveButton.setText("Save and close note\n(Ctrl+Enter)")
        self.saveButton.clicked.connect(self.saveAndClose)
        self.saveButton.setShortcut(QKeySequence("Ctrl+Return"))

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 22))

        self.menuNote = QMenu("Note")
        self.menuEdit = QMenu("Edit")

        self.actionSave =self.createAction("Save", self.saveNote, "SaveIcon.png", QKeySequence.StandardKey.Save)
        self.actionClose = self.createAction("Close", self.close, "CloseIcon.png", QKeySequence.StandardKey.Close)

        self.actionCut = self.createAction("Cut", self.noteEdit.cut, "CutIcon.png", QKeySequence.StandardKey.Cut)
        self.actionCopy = self.createAction("Copy", self.noteEdit.copy, "CopyIcon.png", QKeySequence.StandardKey.Copy)
        self.actionPaste = self.createAction("Paste", self.noteEdit.paste, "PasteIcon.png", QKeySequence.StandardKey.Paste)
        self.actionClear = self.createAction("Clear", self.noteEdit.clear)
        self.actionUndo = self.createAction("Undo", self.noteEdit.undo, "UndoIcon.png", QKeySequence.StandardKey.Undo)
        self.actionRedo = self.createAction("Redo", self.noteEdit.redo, "RedoIcon.png", QKeySequence.StandardKey.Redo)

        self.menuNote.addAction(self.actionSave)
        self.menuNote.addAction(self.actionClose)

        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionClear)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.menubar.addAction(self.menuNote.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.setMenuBar(self.menubar)

    def loadCurrentNote(self):
        if self.noteID != -1:
            with Session(self.engine) as session:
                note = session.execute(select(Notes).where(Notes.noteID == self.noteID)).fetchone()[0]
                if note.noteDate and note.noteTime:
                    self.reminderCheckBox.setChecked(True)
                    self.dateEdit.setDate(note.noteDate)
                    self.timeEdit.setTime(note.noteTime)
                self.noteEdit.setText(note.noteText)
    
    def onNoteChanged(self):
        self.changedNote = True
        self.timeEdit.timeChanged.disconnect()
        self.dateEdit.dateChanged.disconnect()
        self.noteEdit.textChanged.disconnect()
        self.reminderCheckBox.clicked.disconnect()
        self.setWindowTitle("* "+self.windowTitle())

    def onNoteSaved(self):
        self.timeEdit.timeChanged.connect(self.onNoteChanged)
        self.dateEdit.dateChanged.connect(self.onNoteChanged)
        self.noteEdit.textChanged.connect(self.onNoteChanged)
        self.reminderCheckBox.clicked.connect(self.onNoteChanged)
        if self.windowTitle().startswith("* "):
            self.setWindowTitle(self.windowTitle()[2:])

    def createAction(self, actionText:str, actionFunc:callable, actionIcon:str=None, actionKeySequence:QKeySequence=None):
        action = QAction()
        action.setText(actionText)
        if actionIcon:
            action.setIcon(QIcon(os.path.join(self.iconPath, actionIcon)))
        if actionKeySequence:
            action.setShortcut(actionKeySequence)
        action.triggered.connect(actionFunc)
        return action

    def checkReminderState(self):
        if self.reminderCheckBox.checkState() == Qt.CheckState.Checked:
            return True
        return False

    def enableReminder(self):
        if self.checkReminderState():
            self.dateEdit.setEnabled(True)
            self.timeEdit.setEnabled(True)
        else:
            self.dateEdit.setDate(QDate(date.today()))
            self.dateEdit.setEnabled(False)
            self.timeEdit.setEnabled(False)

    def saveNoteOption(self):
        if self.changedNote:
            saveDialog = SaveNoteDialog()
            saveDialog.exec()
            option = saveDialog.saveOption
            if option == 0:
                self.saveNote()
            if option == 1:
                return 0
            else:
                return 1
        return 1
    
    def addNoteReminder(self):
        readDate = self.dateEdit.date().toPyDate()
        readTime = self.timeEdit.time().toPyTime()
        readText = self.noteEdit.toPlainText()
        note = Notes(noteDate=readDate, noteTime=readTime, noteText=readText, noteUser=self.userLogin)
        return note
    
    def addNoteNoReminder(self):
        readText = self.noteEdit.toPlainText()
        note = Notes(noteText=readText, noteUser=self.userLogin)
        return note
    
    def updateNoteReminder(self, note):
        readDate = self.dateEdit.date().toPyDate()
        readTime = self.timeEdit.time().toPyTime()
        readText = self.noteEdit.toPlainText()

        note.noteDate=readDate
        note.noteTime=readTime
        note.noteText=readText
        return note
    
    def updateNoteNoReminder(self, note):
        note.noteDate=None
        note.noteTime=None
        readText = self.noteEdit.toPlainText()
        note.noteText=readText
        return note

    def saveNote(self):
        if self.noteEdit.toPlainText()=='':
            QMessageBox.information(self,"Empty note", "Cannot save empty note!")
        else:
            with Session(self.engine) as session:
                if self.noteID == -1:
                    if self.checkReminderState():
                        note = self.addNoteReminder()
                    else:
                        note = self.addNoteNoReminder()
                    session.add(note)
                else:
                    note = session.execute(select(Notes).where(Notes.noteID == self.noteID)).fetchone()[0]
                    if not note:
                        QMessageBox.warning(self, "Note not existing!", "Note does not exist!")
                    else:
                        if self.checkReminderState():
                            note = self.updateNoteReminder(note)
                        else:
                            note = self.updateNoteNoReminder(note)
                session.commit()
                self.noteID = note.noteID
            self.changedNote = False
            self.onNoteSaved()

    def saveAndClose(self):
        self.saveNote()
        self.close()
    
    def closeEvent(self, a0: QCloseEvent):
        if self.saveNoteOption() == 1:
            a0.accept()
            subprocess.Popen(['python', os.path.join(os.path.dirname(sys.argv[0]),'user_notes_window.py'), self.userLogin, '0'])
        else:
            a0.ignore()


if __name__=='__main__':
    app = QApplication(sys.argv)
    noteID = int(sys.argv[1])
    userLogin = sys.argv[2]
    window = TextEditorWindow(noteID, userLogin)
    window.show()
    sys.exit(app.exec())
