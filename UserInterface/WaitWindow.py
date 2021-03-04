from PyQt5.QtCore import QRect, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QPixmap, QPaintEvent
from PyQt5.QtWidgets import QWidget, qApp
from PyQt5 import QtCore

#####################################################
# Wait Promptation Window
#####################################################


class WaitWindow(QWidget):
    def __init__(self, text):
        super(WaitWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(700, 190, 800, 400)
        self.text = text

    def paintEvent(self, qpaintevent):
        p = QPainter(self)  #  Don't Write like that: self.p = QPainter(self), QPainter(self) returns a Painter pointer,
                            #  But self.p is also a Painter pointer
                            #  So, after doing that original object of self.p will be unaccessable!
        p.setPen(QPen())
        p.setBrush(QBrush())
        qfont = QFont("TimesNewRoman", 27)
        qfont.setBold(True)
        qfont.setItalic(True)
        p.setFont(qfont)
        p.setPen(QColor("#000000"))
        p.drawPixmap(0, 0, QPixmap("../icons/wait.jpg"))
        p.drawText(QRect(0, 0, 500, 350), QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop, self.text)
        p.end()  # Don't forget to close a pen after use!

    def showWaitWindow(self):
        self.paintEvent(QPaintEvent)
        self.update()
        qApp.processEvents()


################################################
# MultiThread for Wait Promptation Window
################################################


class MultiThreadPrompt(QThread):
    signal = pyqtSignal()
    fatherwindow = ''
    win = ''

    def __init__(self, win):
        super(MultiThreadPrompt, self).__init__()
        self.win = win

    def run(self):
        self.signal.connect(self.show_wait_box)
        self.start
        self.signal.emit()

    def show_wait_box(self):
        self.win.show()
        self.win.showWaitWindow()

    def terminate_thread(self):
        self.win.close()
        self.terminate()