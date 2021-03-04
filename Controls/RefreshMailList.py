
######################################
# Refresh or generate dir tree view
######################################
from PyQt5.QtGui import QStandardItem, QFont
from PyQt5 import QtCore

class RefreshMailList:

    model = ''
    tokenhandler = ''
    itemlist = []

    def __init__(self, model, tokenhandler, itemlist):
        self.model = model
        self.tokenhandler = tokenhandler
        self.itemlist = itemlist

    def refresh_mail_list(self):
        for l in self.itemlist:
            item = QStandardItem(l)
            fnt = QFont()
            fnt.setPointSize(9)
            fnt.setBold(True)
            if(l[(l.index('\n|**是否已读**| ') + 12):].strip() == 'False'):
                item.setBackground(QtCore.Qt.red)
            item.setFont(fnt)
            self.model.appendRow(item)


