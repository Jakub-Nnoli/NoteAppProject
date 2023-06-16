import os, sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QDialog, QMessageBox
from PyQt6.QtCore import QRect
from PyQt6.QtGui import  QIcon, QFont

from database_modules import Users
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.engine = create_engine('sqlite:///NotepadDatabase.db')

        self.iconPath = os.path.join(os.getcwd(),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(400,174)

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
                doesUserExistQuery = select((Users)).where(Users.userLogin == newUsername)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterDialog()
    window.show()
    sys.exit(app.exec())