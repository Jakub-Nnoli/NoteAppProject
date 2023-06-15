import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableView, QMenuBar, QMenu, QGridLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QAction, QIcon,  QFont
from database_modules import Users, Notes

class UserNotesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        self.actionChangeEmail = QAction()
        self.actionChangeEmail.setText("Change email")

        self.actionDeleteAccount = QAction()
        self.actionDeleteAccount.setText("Delete account")

        self.menuFile.addAction(self.actionCreateNote)
        self.menuFile.addAction(self.actionSelectAllNotes)
        self.menuFile.addAction(self.actionDelete)
        self.menuFile.addAction(self.actionClose)

        self.menuAccount.addAction(self.actionChangeLogin)
        self.menuAccount.addAction(self.actionChangePassword)
        self.menuAccount.addAction(self.actionChangeEmail)
        self.menuAccount.addSeparator()
        self.menuAccount.addAction(self.actionDeleteAccount)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAccount.menuAction())

        self.setMenuBar(self.menubar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserNotesWindow()
    window.show()
    sys.exit(app.exec())
