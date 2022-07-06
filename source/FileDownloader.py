import sys
import urllib.request

import PyQt5.QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class FileDownloader(QDialog):
    def __init__(self):
        super(FileDownloader, self).__init__()
        self.load_ui()
        pass

    def load_ui(self):
        layout = QVBoxLayout()
        self.url = QLineEdit()
        self.url.selectedText()
        select_button = QPushButton("Browse")
        self.file_name = QLineEdit()
        download_button = QPushButton("Download")

        self.url.setPlaceholderText("URL from where the download should happen")
        #self.file_name.setDisabled(True)
        self.file_name.setPlaceholderText("Local file path where the file will be downloaded")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.url)
        layout.addWidget(select_button)
        layout.addWidget(self.file_name)
        layout.addWidget(self.progress_bar)
        layout.addWidget(download_button)
        self.setLayout(layout)
        self.setWindowTitle("pyDownloader")
        self.url.setFocus()
        download_button .clicked.connect(self.download_file)
        select_button   .clicked.connect(self.select_file)
        pass

    def select_file(self):
        saveFileName=QFileDialog.getSaveFileName(self, caption="Save File As", directory="../../Downloads", filter="All Files (*.*)")
        print(saveFileName)
        print(type(saveFileName))
        self.file_name.setText(QDir.fromNativeSeparators(saveFileName[0]))
        pass

    def download_file(self):
        url = self.url.text()
        savelocation = self.file_name.text()
        urllib.request.urlretrieve(url, savelocation, self.report)
        pass

    def report(self, blocknum, blocksize, totalsize):
        read_so_far = blocknum * blocksize

        if totalsize > 0:
            percent = read_so_far * 100 / totalsize
            self.progress_bar.setValue(int(percent))
        else:
            self.progress_bar.setValue(50)
            pass

app=QApplication(sys.argv)
dialog=FileDownloader()
dialog.show()
sys.exit(app.exec_())
