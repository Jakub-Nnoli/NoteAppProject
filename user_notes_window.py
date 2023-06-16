import os, sys, subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableView, QMenuBar, QMenu, QGridLayout, QPushButton, QLabel, QMessageBox, QAbstractItemView
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from database_modules import Users, Notes

class UserNotesWindow(QMainWindow):
    def __init__(self, username:str):
        super().__init__()

        self.engine = create_engine('sqlite:///NotepadDatabase.db')

        with Session(self.engine) as session:
            self.user = session.execute(select((Users)).where(Users.userLogin == username)).fetchone()[0]

        self.iconPath = os.path.join(os.getcwd(),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(800, 600)

        self.centralNoteWidget = QWidget()
        self.setCentralWidget(self.centralNoteWidget)

        self.mainLayout = QGridLayout(self.centralNoteWidget)

        self.createNoteButton = QPushButton(self.centralNoteWidget)
        self.createNoteButton.setGeometry(QRect(10, 10, 141, 31))
        self.createNoteButton.setText("Create new note")
    
        self.notesLayoutLabel = QLabel(self.centralNoteWidget)
        self.notesLayoutLabel.setGeometry(QRect(10, 50, 51, 16))
        self.notesLayoutLabel.setText("Notes: ")

        self.tableView = QTableView(self.centralNoteWidget)
        self.tableView.setGeometry(QRect(10, 70, 781, 461))
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.openNoteButton = QPushButton(self.centralNoteWidget)
        self.openNoteButton.setGeometry(QRect(650, 540, 141, 31))
        self.openNoteButton.setText("Edit note")

        self.deleteButton = QPushButton(self.centralNoteWidget)
        self.deleteButton.setGeometry(QRect(500, 540, 141, 31))
        self.deleteButton.setText("Delete")

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 22))

        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle("File")

        self.menuAccount = QMenu(self.menubar)
        self.menuAccount.setTitle("Account")

        self.actionCreateNote = QAction()
        self.actionCreateNote.setText("Create note")

        self.actionSelectAllNotes = QAction()
        self.actionSelectAllNotes.setText("Select all notes")

        self.actionDelete = QAction()
        self.actionDelete.setText("Delete")

        self.actionClose = QAction()
        self.actionClose.setText("Close")

        self.actionChangeLogin = QAction()
        self.actionChangeLogin.setText("Change login")

        self.actionChangePassword = QAction()
        self.actionChangePassword.setText("Change password")

        self.actionDeleteAccount = QAction()
        self.actionDeleteAccount.setText("Delete account")

        self.menuFile.addAction(self.actionCreateNote)
        self.menuFile.addAction(self.actionSelectAllNotes)
        self.menuFile.addAction(self.actionDelete)
        self.menuFile.addAction(self.actionClose)

        self.menuAccount.addAction(self.actionChangeLogin)
        self.menuAccount.addAction(self.actionChangePassword)
        self.menuAccount.addSeparator()
        self.menuAccount.addAction(self.actionDeleteAccount)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAccount.menuAction())

        self.setMenuBar(self.menubar)

        self.readUserNotes()

    def readUserNotes(self):
        dbView = QSqlDatabase.addDatabase("QSQLITE")
        dbView.setDatabaseName(os.path.join(os.getcwd(),"NotepadDatabase.db"))

        if not dbView.open():
            QMessageBox.warning(self, "Database error", "Can't connect to database.\nTry again later.")
            self.close()

        noteTable = QSqlTableModel()
        noteTable.setTable("Notes")
        noteTable.select()

        userNotes = QSqlQuery()
        userNotes.prepare(f"SELECT noteDate AS Date, noteTime AS Time, noteText AS Note FROM Notes WHERE noteUser = '{self.user.userLogin}'")
        userNotes.exec()

        noteTable.setQuery(userNotes)

        self.tableView.setModel(noteTable)
    
    def createNewNote():
        return 0
    
    def editSelectedNote(self,index):
        return 0
    
    def deleteSelectedNote(self, index):
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #username = sys.argv[1]
    window = UserNotesWindow('user')
    window.show()
    sys.exit(app.exec())
