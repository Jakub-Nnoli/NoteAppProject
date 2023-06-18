import os, sys
from datetime import date, time
from PyQt6 import QtCore
from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QDialog, QMessageBox, QAbstractSpinBox, QTextBrowser, QDateEdit, QTimeEdit, QApplication
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import  QIcon, QFont

from database_modules import Users
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.engine = create_engine(f'sqlite:///{os.path.dirname(sys.argv[0])}/NotepadDatabase.db')

        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(400,175)

        self.label = QLabel(parent=self)
        self.label.setGeometry(QRect(10, 10, 291, 16))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText("Fill all boxes to create a new account")

        self.usernameLabel = QLabel(parent=self)
        self.usernameLabel.setGeometry(QRect(10, 40, 81, 31))
        self.usernameLabel.setText("Username:")

        self.usernameLineEdit = QLineEdit(parent=self)
        self.usernameLineEdit.setGeometry(QRect(80, 40, 311, 31))

        self.passwordLabel = QLabel(parent=self)
        self.passwordLabel.setGeometry(QRect(10, 80, 81, 31))
        self.passwordLabel.setText("Password:")

        self.passwordLineEdit = QLineEdit(parent=self)
        self.passwordLineEdit.setGeometry(QRect(80, 80, 311, 31))
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QRect(10, 130, 101, 24))
        self.cancelButton.setText("Cancel")
        self.cancelButton.clicked.connect(self.cancel)

        self.registerButton = QPushButton(parent=self)
        self.registerButton.setGeometry(QRect(290, 130, 101, 24))
        self.registerButton.setText("Register")
        self.registerButton.clicked.connect(self.registerUser)

    def registerUser(self):
        newUsername = self.usernameLineEdit.text()
        newPassword = self.passwordLineEdit.text()

        if not newUsername or not newPassword:
            QMessageBox.warning(self, "Empty fields", "Username and password box cannot be empty!")
        else:
            with Session(self.engine) as session:
                doesUserExistQuery = select(Users).where(Users.userLogin == newUsername)
                if session.execute(doesUserExistQuery).scalar():
                    QMessageBox.warning(self, "User Exists", f"User {newUsername} already exists!")
                else:
                    user = Users(userLogin=newUsername, userPassword=newPassword)
                    session.add(user)
                    session.commit()
                    QMessageBox.information(self, "User added", f"User {newUsername} added!")
            self.accept()

    
    def cancel(self):
        self.reject()


class ResetPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.engine = create_engine(f'sqlite:///{os.path.dirname(sys.argv[0])}/NotepadDatabase.db')

        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(450,130)

        self.mainlabel = QLabel(parent=self)
        self.mainlabel.setGeometry(QRect(10, 10, 431, 20))
        font = QFont()
        font.setPointSize(11)
        self.mainlabel.setFont(font)
        self.mainlabel.setText("Type your username to reset your password")

        self.usernameLabel = QLabel(parent=self)
        self.usernameLabel.setGeometry(QRect(10, 42, 81, 31))
        self.usernameLabel.setText("Username:")

        self.usernameLineEdit = QLineEdit(parent=self)
        self.usernameLineEdit.setGeometry(QRect(80, 42, 361, 31))

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QRect(10, 90, 156, 24))
        self.cancelButton.setText("Cancel")
        self.cancelButton.clicked.connect(self.cancel)

        self.newPassButton = QPushButton(parent=self)
        self.newPassButton.setGeometry(QRect(285, 90, 156, 24))
        self.newPassButton.setText("Reset password")
        self.newPassButton.clicked.connect(self.resetPassword)

    def resetPassword(self):
        username = self.usernameLineEdit.text()

        if not username:
            QMessageBox.warning(self, "Empty fields", "Username box cannot be empty!")
        else:
            with Session(self.engine) as session:
                doesUserExistQuery = select(Users).where(Users.userLogin == username)
                if not session.execute(doesUserExistQuery).scalar():
                    QMessageBox.warning(self, "User Not Found", f"User {username} does not exist!")
                else:
                    user = session.execute(doesUserExistQuery).fetchone()[0]
                    user.userPassword = 'password'
                    session.commit()
                    QMessageBox.information(self, "Reset Password", f"Password for user {username} has been set to 'password'.\nRemember to change password after login!")
            self.accept()
    
    def cancel(self):
        self.reject()

class SaveNoteDialog(QDialog):
    def __init__(self):
        super().__init__()
    
        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(400,95)

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

class ChangeLoginDialog(QDialog):
    def __init__(self, userLogin):
        super().__init__()

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(400,95)

        self.userLogin = userLogin

        self.engine = create_engine(f'sqlite:///{os.path.dirname(sys.argv[0])}/NotepadDatabase.db')

        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.newUsernameLabel = QLabel(parent=self)
        self.newUsernameLabel.setGeometry(QRect(10, 50, 81, 31))
        self.newUsernameLabel.setText("New username:")

        self.saveChangesButton = QPushButton(parent=self)
        self.saveChangesButton.setGeometry(QRect(280, 90, 111, 31))
        self.saveChangesButton.setText("Save changes")
        self.saveChangesButton.clicked.connect(self.changeLogin)

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QRect(160, 90, 111, 31))
        self.cancelButton.setText("Cancel")
        self.cancelButton.clicked.connect(self.cancel)
        
        self.newUsernameEdit = QLineEdit(parent=self)
        self.newUsernameEdit.setGeometry(QRect(100, 50, 291, 31))

    def changeLogin(self):
        newUsername = self.newUsernameEdit.text()

        if not newUsername:
            QMessageBox.warning(self, "Empty fields", "Username boxes cannot be empty!")
        else:
            with Session(self.engine) as session:
                doesUserExistQuery = select(Users).where(Users.userLogin == self.userLogin)
                if not session.execute(doesUserExistQuery).scalar():
                    QMessageBox.warning(self, "User Not Found", f"User {self.userLogin} does not exist!")
                else:
                    user = session.execute(doesUserExistQuery).fetchone()[0]
                    user.userLogin = newUsername
                    session.commit()
                    QMessageBox.information(self, "Change Username", f"Username  has been set to {newUsername}!")
            self.accept()
    
    def cancel(self):
        self.reject()

class ChangePasswordDialog(QDialog):
    def __init__(self, userLogin):
        super().__init__()

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(400,135)

        self.userLogin = userLogin

        self.engine = create_engine(f'sqlite:///{os.path.dirname(sys.argv[0])}/NotepadDatabase.db')

        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.currPasswordLabel = QLabel(parent=self)
        self.currPasswordLabel.setGeometry(QRect(10, 10, 81, 31))
        self.currPasswordLabel.setText("Current password:")

        self.newPasswordLabel = QLabel(parent=self)
        self.newPasswordLabel.setGeometry(QRect(10, 50, 81, 31))
        self.newPasswordLabel.setText("New password:")

        self.saveChangesButton = QPushButton(parent=self)
        self.saveChangesButton.setGeometry(QRect(280, 90, 111, 31))
        self.saveChangesButton.setText("Save changes")
        self.saveChangesButton.clicked.connect(self.changePassword)

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QRect(160, 90, 111, 31))
        self.cancelButton.setText("Cancel")
        self.cancelButton.clicked.connect(self.cancel)

        self.currPasswordEdit = QLineEdit(parent=self)
        self.currPasswordEdit.setGeometry(QRect(100, 10, 291, 31))
        self.currPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.newPasswordEdit = QLineEdit(parent=self)
        self.newPasswordEdit.setGeometry(QRect(100, 50, 291, 31))
        self.newPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def changePassword(self):
        currPassword = self.currUsernameEdit.text()
        newPassword = self.newPasswordEdit.text()

        if not newPassword:
            QMessageBox.warning(self, "Empty fields", "New password cannot be empty!")
        else:
            with Session(self.engine) as session:
                doesUserExistQuery = select(Users).where(Users.userLogin == self.userLogin)
                if not session.execute(doesUserExistQuery).scalar():
                    QMessageBox.warning(self, "User Not Found", f"User {self.userLogin} does not exist!")
                else:
                    user = session.execute(doesUserExistQuery).fetchone()[0]
                    if user.userPassword != currPassword:
                        QMessageBox.warning(self, "Invalid password", "Invalid current password!")
                    else:
                        user.userPassword = newPassword
                        session.commit()
                        QMessageBox.information(self, "Reset Password", f"Password has been changed for {self.userLogin}!")
            self.accept()
    
    def cancel(self):
        self.reject()

class ReminderDialog(QDialog):
    def __init__(self, noteText:str, noteDate:date, noteTime:time):
        super().__init__()

        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(400,280)

        self.skipAllReminders = 0

        self.reminderLabel = QLabel(parent=self)
        self.reminderLabel.setGeometry(QtCore.QRect(10, 10, 381, 31))
        font = QFont()
        font.setPointSize(13)
        font.setBold(False)
        self.reminderLabel.setFont(font)
        self.reminderLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.reminderLabel.setText("Reminder!")

        self.dateLabel = QLabel(parent=self)
        self.dateLabel.setGeometry(QtCore.QRect(20, 50, 49, 31))
        self.dateLabel.setText("Date:")

        self.timeLabel = QLabel(parent=self)
        self.timeLabel.setGeometry(QtCore.QRect(200, 50, 49, 31))
        self.timeLabel.setText("Time:")

        self.noteLabel = QLabel(parent=self)
        self.noteLabel.setGeometry(QtCore.QRect(20, 90, 41, 21))
        self.noteLabel.setText("Note:")

        self.okButton = QPushButton(parent=self)
        self.okButton.setGeometry(QtCore.QRect(280, 240, 100, 24))
        self.okButton.setText("OK")
        self.okButton.clicked.connect(self.close)

        self.skipButton = QPushButton(parent=self)
        self.skipButton.setGeometry(QtCore.QRect(175, 240, 100, 24))
        self.skipButton.setText("Skip all reminders")
        self.skipButton.clicked.connect(self.skipAllNext)

        self.noteBrowser = QTextBrowser(parent=self)
        self.noteBrowser.setGeometry(QtCore.QRect(20, 110, 361, 121))
        self.noteBrowser.setText(noteText)

        self.dateEdit = QDateEdit(parent=self)
        self.dateEdit.setGeometry(QtCore.QRect(60, 50, 110, 31))
        self.dateEdit.setReadOnly(True)
        self.dateEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.dateEdit.setDate(noteDate)

        self.timeEdit = QTimeEdit(parent=self)
        self.timeEdit.setGeometry(QtCore.QRect(250, 50, 118, 31))
        self.timeEdit.setReadOnly(True)
        self.timeEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.timeEdit.setTime(noteTime)

    def skipAllNext(self):
        self.skipAllReminders = 1
        self.close()