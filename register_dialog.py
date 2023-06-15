import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QLabel, QDialog
from PyQt6.QtCore import QRect
from PyQt6.QtGui import  QPixmap, QIcon, QFont

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()

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

        self.loginLabel = QLabel(parent=self)
        self.loginLabel.setGeometry(QRect(10, 40, 81, 31))
        self.loginLabel.setText("Login:")

        self.loginLineEdit = QLineEdit(parent=self)
        self.loginLineEdit.setGeometry(QRect(80, 40, 311, 31))

        self.passwordLabel = QLabel(parent=self)
        self.passwordLabel.setGeometry(QRect(10, 80, 81, 31))
        self.passwordLabel.setText("Password:")

        self.passwordLineEdit = QLineEdit(parent=self)
        self.passwordLineEdit.setGeometry(QRect(80, 80, 311, 31))

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QRect(10, 130, 101, 24))
        self.cancelButton.setText("Cancel")

        self.registerButton = QPushButton(parent=self)
        self.registerButton.setGeometry(QRect(290, 130, 101, 24))
        self.registerButton.setText("Register")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterDialog()
    window.show()
    sys.exit(app.exec())