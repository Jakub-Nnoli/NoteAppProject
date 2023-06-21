import os, sys, subprocess
from datetime import date, time, timedelta
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableView, QMenuBar, QMenu, QPushButton, QLabel, QMessageBox, QAbstractItemView
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from database_modules import Users, Notes

from necessary_dialogs import ChangeLoginDialog, ChangePasswordDialog, ReminderDialog

class UserNotesWindow(QMainWindow):
    def __init__(self, username:str, triggerReminders:int):
        super().__init__()

        self.engine = create_engine(f'sqlite:///{os.path.join(os.path.dirname(sys.argv[0]), "NotepadDatabase.db")}')

        with Session(self.engine) as session:
            self.user = session.execute(select(Users).where(Users.userLogin == username)).fetchone()[0]

        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")
        self.database = os.path.join(os.path.dirname(sys.argv[0]),"NotepadDatabase.db")

        self.setWindowTitle("NoteApp")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(800, 600)

        self.centralNoteWidget = QWidget()
        self.setCentralWidget(self.centralNoteWidget)

        self.createNoteButton = QPushButton(self.centralNoteWidget)
        self.createNoteButton.setGeometry(QRect(10, 10, 141, 31))
        self.createNoteButton.setText("Create new note")
        self.createNoteButton.setIcon(QIcon(os.path.join(self.iconPath, "CreateNoteIcon.png")))
        self.createNoteButton.clicked.connect(self.createNote)
    
        self.notesLayoutLabel = QLabel(self.centralNoteWidget)
        self.notesLayoutLabel.setGeometry(QRect(10, 50, 51, 16))
        self.notesLayoutLabel.setText("Notes: ")

        self.tableView = QTableView(self.centralNoteWidget)
        self.tableView.setGeometry(QRect(10, 70, 781, 461))
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.clicked.connect(self.selectNote)

        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().sectionDoubleClicked.connect(self.sortByColumn)

        self.openNoteButton = QPushButton(self.centralNoteWidget)
        self.openNoteButton.setGeometry(QRect(650, 540, 141, 31))
        self.openNoteButton.setText("Edit note")
        self.openNoteButton.setIcon(QIcon(os.path.join(self.iconPath, "EditNoteIcon.png")))
        self.openNoteButton.clicked.connect(self.editSelectedNote)
        self.openNoteButton.setShortcut(QKeySequence(Qt.Key.Key_Return))

        self.deleteButton = QPushButton(self.centralNoteWidget)
        self.deleteButton.setGeometry(QRect(500, 540, 141, 31))
        self.deleteButton.setText("Delete")
        self.deleteButton.setIcon(QIcon(os.path.join(self.iconPath, "DeleteIcon.png")))
        self.deleteButton.clicked.connect(self.deleteSelectedNote)
        self.deleteButton.setShortcut(QKeySequence(Qt.Key.Key_Delete))

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 22))

        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle("File")

        self.menuAccount = QMenu(self.menubar)
        self.menuAccount.setTitle("Account")

        self.actionCreateNote = self.createAction("Create note", self.createNote, "CreateNoteIcon.png", QKeySequence("Ctrl+N"))
        self.actionEditNote = self.createAction("Edit", self.editSelectedNote, "EditNoteIcon.png")
        self.actionDelete = self.createAction("Delete", self.deleteSelectedNote, "DeleteIcon.png", QKeySequence(Qt.Key.Key_Delete))
        self.actionClose = self.createAction("Close", self.close, "CloseIcon.png", QKeySequence.StandardKey.Close)

        self.actionChangeLogin = self.createAction("Change login", self.changeLogin, "EditDataIcon.png")
        self.actionChangePassword = self.createAction("Change password", self.changePassword, "EditDataIcon.png")
        self.actionLogOut = self.createAction("Log out", self.logOut, "LogOutIcon.png")
        self.actionDeleteAccount = self.createAction("Delete account", self.deleteAccount, "DeleteIcon.png")

        self.menuFile.addAction(self.actionCreateNote)
        self.menuFile.addAction(self.actionDelete)
        self.menuFile.addAction(self.actionClose)

        self.menuAccount.addAction(self.actionChangeLogin)
        self.menuAccount.addAction(self.actionChangePassword)
        self.menuAccount.addSeparator()
        self.menuAccount.addAction(self.actionLogOut)
        self.menuAccount.addAction(self.actionDeleteAccount)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAccount.menuAction())

        self.setMenuBar(self.menubar)

        self.readUserNotes()

        if triggerReminders == 1:
            self.showReminders()

    def createAction(self, actionText:str, actionFunc:callable, actionIcon:str=None, actionKeySequence:QKeySequence=None):
        action = QAction()
        action.setText(actionText)
        if actionIcon:
            action.setIcon(QIcon(os.path.join(self.iconPath, actionIcon)))
        if actionKeySequence:
            action.setShortcut(actionKeySequence)
        action.triggered.connect(actionFunc)
        return action
    
    def changeLogin(self):
        changeLogin = ChangeLoginDialog(self.user.userLogin)
        changeLogin.exec()
    
    def changePassword(self):
        changePassword = ChangePasswordDialog(self.user.userLogin)
        changePassword.exec()
    
    def logOut(self):
        subprocess.Popen(['python', os.path.join(os.path.dirname(sys.argv[0]),'login_window.py')])
        self.close()
    
    def deleteAccount(self):
        with Session(self.engine) as session:
            session.delete(self.user)
            session.commit()

        subprocess.Popen(['python', os.path.join(os.path.dirname(sys.argv[0]),'login_window.py')])
        self.close()

    def readUserNotes(self):
        if not QSqlDatabase.contains('qt_sql_default_connection'):
            dbView = QSqlDatabase.addDatabase("QSQLITE")
            dbView.setDatabaseName(self.database)

            if not dbView.open():
                QMessageBox.warning(self, "Database error", "Can't connect to database.\nTry again later.")
                self.close()
        else:
            dbView = QSqlDatabase.database()

        noteTableModel = QSqlTableModel()
        noteTableModel.setTable("Notes")
        noteTableModel.select()

        userNotes = QSqlQuery()
        userNotes.prepare(f'SELECT noteID, noteDate, noteTime, noteText FROM Notes WHERE noteUser = "{self.user.userLogin}"')
        userNotes.exec()

        noteTableModel.setQuery(userNotes)
        noteTableModel.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        noteTableModel.setHeaderData(1, Qt.Orientation.Horizontal, "Date")
        noteTableModel.setHeaderData(2, Qt.Orientation.Horizontal, "Time")
        noteTableModel.setHeaderData(3, Qt.Orientation.Horizontal, "Note")

        self.tableView.setModel(noteTableModel)

    def showReminders(self):
        today = date.today()
        fiveDaysNext = today + timedelta(days=5)
        with Session(self.engine) as session:
            userReminderNotes = session.execute(select(Notes).
                                                where(and_(Notes.noteUser == self.user.userLogin, Notes.noteDate.isnot(None), 
                                                           Notes.noteDate > today, Notes.noteDate <= fiveDaysNext))).fetchall()
            stopReminding = 0
            index = 0
            while stopReminding != 1 and index < len(userReminderNotes):
                note = userReminderNotes[index][0]
                reminder = ReminderDialog(note.noteText, note.noteDate, note.noteTime)
                reminder.exec()
                stopReminding = reminder.skipAllReminders
                index += 1

    def sortByColumn(self, logicalIndex):
        self.tableView.model().sort(logicalIndex, Qt.SortOrder.AscendingOrder)

    def createNote(self):
        subprocess.Popen(['python', os.path.join(os.path.dirname(sys.argv[0]),'text_editor_window.py'), '-1', self.user.userLogin])
        self.close()
    
    def selectNote(self, index):
        if self.tableView.selectionModel().hasSelection() == 0:
            QMessageBox.information(self, "Note Not Selected", "Please select note first!")
            return -1
        else:
            selectedNote = index.row()
            noteModel = index.model()
            noteIndex = noteModel.index(selectedNote, 0)
            noteID = noteModel.data(noteIndex)
        
            return noteID
    
    def deleteSelectedNote(self):
        noteIndex = self.tableView.currentIndex()
        noteID = self.selectNote(noteIndex)
        
        if not noteID == -1:
            with Session(self.engine) as session:
                note = session.execute(select(Notes).where(Notes.noteID == noteID)).fetchone()[0]
                if note:
                    session.delete(note)
                    session.commit()
                    self.readUserNotes()
                else:
                    QMessageBox.warning(self, "Note Not Existing", "Note does not exist")


    def editSelectedNote(self):
        noteIndex = self.tableView.currentIndex()
        noteID = self.selectNote(noteIndex)
        if not noteID == -1:
            subprocess.Popen(['python', os.path.join(os.path.dirname(sys.argv[0]),'text_editor_window.py'), str(noteID), self.user.userLogin])
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = sys.argv[1]
    triggerReminders = int(sys.argv[2])
    window = UserNotesWindow(username, triggerReminders)
    window.show()
    sys.exit(app.exec())
