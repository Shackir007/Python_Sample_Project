import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class HelloWorld(QDialog):
    def __init__(self):
        super(HelloWorld, self).__init__()
        layout = QVBoxLayout()
        label = QLabel("Name")
        text = QLineEdit("Enter Name Here")
        button = QPushButton("Close")
        file_select_button=QPushButton("Select")
        layout.addWidget(label)
        layout.addWidget(text)
        layout.addWidget(file_select_button)
        layout.addWidget(button)
        self.setLayout(layout)
        button.clicked.connect(self.close)
        file_select_button.clicked.connect(selectFileBox)
def selectFileBox():
    #QFileDialog("Select FIle", "./", "*.*")
    QFileSelector("Select FIle", "./", "*.*")

app = QApplication(sys.argv)
dialog = HelloWorld()
dialog.show()
sys.exit(app.exec_())
