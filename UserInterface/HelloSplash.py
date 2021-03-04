import time

from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap, QPaintEvent, QFont, QColor
from PyQt5.QtWidgets import QWidget, qApp

###################################
# Hello Window
###################################


class HelloSplash(QWidget):
    def __init__(self):
        super(HelloSplash, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(700, 190, 800, 800)
        self.text = "Loading...0%"

    def paintEvent(self, qpaintevent):
        p = QPainter(self)
        p.setPen(QPen())
        p.setBrush(QBrush())
        qfont = QFont("TimesNewRoman", 14)
        qfont.setBold(True)
        qfont.setItalic(True)
        p.setFont(qfont)
        p.setPen(QColor("#FF0000"))
        p.drawPixmap(0, 0, QPixmap("../icons/hello.jpg"))
        p.drawText(QRect(0, 0, 450, 550), QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop, self.text)
        p.end()

    def setText(self, text):
        self.text = text
        self.paintEvent(QPaintEvent)

    def load_Message(self, splash):
        for i in range(1, 5):
            time.sleep(1)
            splash.setText('Loading...' + format(25 * i) + '%' + '\n' + '图片来源:Architect’s Dream - 托马斯·科尔')
            splash.update()
            qApp.processEvents()

