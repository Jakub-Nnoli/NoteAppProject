import os, sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QDialog
from PyQt6.QtCore import QRect
from PyQt6.QtGui import  QIcon, QFont

class ResetPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.iconPath = os.path.join(os.getcwd(),"Icons")

        self.setWindowTitle("NotepadS")
        self.setWindowIcon(QIcon(os.path.join(self.iconPath, "AppIcon.png")))
        self.setFixedSize(450,130)

        self.mainlabel = QLabel(parent=self)
        self.mainlabel.setGeometry(QRect(10, 10, 431, 20))
        font = QFont()
        font.setPointSize(11)
        self.mainlabel.setFont(font)
        self.mainlabel.setText("Type your login to reset your password")

        self.loginLabel = QLabel(parent=self)
        self.loginLabel.setGeometry(QRect(10, 42, 81, 31))
        self.loginLabel.setText("Login:")

        self.loginLineEdit = QLineEdit(parent=self)
        self.loginLineEdit.setGeometry(QRect(80, 42, 361, 31))

        self.cancelButton = QPushButton(parent=self)
        self.cancelButton.setGeometry(QRect(10, 90, 156, 24))
        self.cancelButton.setText("Cancel")

        self.newPassButton = QPushButton(parent=self)
        self.newPassButton.setGeometry(QRect(285, 90, 156, 24))
        self.newPassButton.setText("Reset password")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResetPasswordDialog()
    window.show()
    sys.exit(app.exec())