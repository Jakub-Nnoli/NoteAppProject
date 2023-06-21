import os, sys, subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import  QPixmap, QIcon, QKeySequence

from database_modules import Users, createDatabase
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from necessary_dialogs import RegisterDialog, ResetPasswordDialog


class StartLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = create_engine(f'sqlite:///{os.path.join(os.path.dirname(sys.argv[0]), "NotepadDatabase.db")}')

        self.iconPath = os.path.join(os.path.dirname(sys.argv[0]),"Icons")

        self.setWindowTitle("NoteApp")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(800, 600)

        self.mainWidget = QWidget()

        self.userIcon = QLabel(parent=self.mainWidget)
        self.userIcon.setGeometry(QRect(300, 80, 201, 201))
        self.userIcon.setObjectName("userIcon")
        icon = QPixmap(os.path.join(self.iconPath, 'UserIcon.png'))
        icon = icon.scaled(self.userIcon.size())
        self.userIcon.setPixmap(icon)

        self.usernameLabel = QLabel(parent=self.mainWidget)
        self.usernameLabel.setGeometry(QRect(270, 300, 261, 16))
        self.usernameLabel.setText("Username:")

        self.usernameLineEdit = QLineEdit(parent=self.mainWidget)
        self.usernameLineEdit.setGeometry(QRect(270, 320, 261, 31))

        self.passwordLabel = QLabel(parent=self.mainWidget)
        self.passwordLabel.setGeometry(QRect(270, 360, 261, 16))
        self.passwordLabel.setText("Password:")

        self.passwordLineEdit = QLineEdit(parent=self.mainWidget)
        self.passwordLineEdit.setGeometry(QRect(270, 380, 261, 31))
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.loginButton = QPushButton(parent=self.mainWidget)
        self.loginButton.setGeometry(QRect(410, 420, 121, 31))
        self.loginButton.setText("Login")
        self.loginButton.clicked.connect(self.login)
        self.loginButton.setShortcut(QKeySequence(Qt.Key.Key_Return))

        self.registerButton = QPushButton(parent=self.mainWidget)
        self.registerButton.setGeometry(QRect(270, 420, 121, 31))
        self.registerButton.setText("Register")
        self.registerButton.clicked.connect(self.register)

        self.forgotPassButton = QPushButton(parent=self.mainWidget)
        self.forgotPassButton.setGeometry(QRect(330, 460, 141, 31))
        self.forgotPassButton.setText("Forgot password?")
        self.forgotPassButton.clicked.connect(self.resetPassword)

        self.setCentralWidget(self.mainWidget)

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        with Session(self.engine) as session:
            doesUserExistQuery = select(Users).where(Users.userLogin == username)
            if not session.execute(doesUserExistQuery).scalar():
                QMessageBox.warning(self, "User Not Found", f"User {username} does not exist!")
            else:
                user = session.execute(doesUserExistQuery).fetchone()[0]
                if user.userPassword != password:
                    QMessageBox.warning(self, "Invalid password", f"Invalid password for user {username}!")
                else:
                    subprocess.Popen(['python', os.path.join(os.path.dirname(sys.argv[0]),'user_notes_window.py'), username, '1'])
                    self.close()
    
    def register(self):
        registration = RegisterDialog()
        registration.exec()
    
    def resetPassword(self):
        resetPassword = ResetPasswordDialog()
        resetPassword.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartLoginWindow()
    window.show()
    sys.exit(app.exec())