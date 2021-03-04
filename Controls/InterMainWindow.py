import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)).split('ExchangeLite')[0],'ExchangeLite'))
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow

from UserInterface import HelloSplash
from UserInterface import MainWindow
from Controls import HandleToken


#Show Welcome Picture
hello = QApplication(sys.argv)
splash = HelloSplash.HelloSplash()
splash.show()
splash.load_Message(splash)
splash.close()

#Show Main Window
app = QApplication(sys.argv)
mainwin = QMainWindow()
mainwin.resize(1671, 914)
palette = QPalette()
pix = QPixmap('../icons/dream.jpg')
pix = pix.scaled(mainwin.width(), mainwin.height())
palette.setBrush(QPalette.Background, QBrush(pix))
mainwin.setPalette(palette)
ui = MainWindow.Ui_MainWindow()
ui.setupUi(mainwin)
mainwin.show()


#Handle Token
handletoken = HandleToken.HandleToken(ui.token_handler)
handletoken.handle_token()


#Show Token
handletoken = HandleToken.HandleToken(ui.token_handler)
handletoken.show_token()

#Refresh Dir Tree
ui.refresh_dir_tree()

sys.exit(app.exec_())

