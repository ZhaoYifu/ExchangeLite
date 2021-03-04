from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from UserInterface import LogWindow

class ShowLogWindow():
    log_content = ''
    logwin = None

    def __init__(self,log_content):
        self.log_content = log_content
        self.logwin = QMainWindow()

    def show_log_window(self):
        self.logwin.resize(869, 618)
        palette = QPalette()
        pix = QPixmap('../icons/dream.jpg')
        pix = pix.scaled(self.logwin.width(), self.logwin.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.logwin.setPalette(palette)
        lg = LogWindow.Ui_MainWindow()
        lg.setupUi(self.logwin)
        lg.additional_operations(self.log_content)
        self.logwin.show()

