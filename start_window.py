import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QLabel, QDialog
from PyQt6.QtCore import QRect
from PyQt6.QtGui import  QPixmap, QIcon

class StartLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.iconPath = os.path.join(os.getcwd(),"Icons")

        self.setWindowTitle("NotepadS")
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

        self.registerButton = QPushButton(parent=self.mainWidget)
        self.registerButton.setGeometry(QRect(270, 420, 121, 31))
        self.registerButton.setText("Register")

        self.forgotPassButton = QPushButton(parent=self.mainWidget)
        self.forgotPassButton.setGeometry(QRect(330, 460, 141, 31))
        self.forgotPassButton.setText("Forgot password?")

        self.setCentralWidget(self.mainWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartLoginWindow()
    window.show()
    sys.exit(app.exec())