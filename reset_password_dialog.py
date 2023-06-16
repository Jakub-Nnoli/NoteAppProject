import os, sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QDialog, QMessageBox
from PyQt6.QtCore import QRect
from PyQt6.QtGui import  QIcon, QFont

from database_modules import Users
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

class ResetPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.engine = create_engine('sqlite:///NotepadDatabase.db')

        self.iconPath = os.path.join(os.getcwd(),"Icons")

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
                doesUserExistQuery = select((Users)).where(Users.userLogin == username)
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
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResetPasswordDialog()
    window.show()
    sys.exit(app.exec())