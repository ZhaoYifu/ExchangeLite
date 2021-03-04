from PyQt5.QtGui import QStandardItem, QFont

class RefreshAttachmentList():
    model = ''
    tokenhandler = ''
    itemlist = None

    def __init__(self,model, tokenhandler, itemlist):
        self.model = model
        self.tokenhandler = tokenhandler
        self.itemlist = itemlist

    def refresh_attachment_list(self):
        for l in self.itemlist:
            for a in l:
                item = QStandardItem(a)
                fnt = QFont()
                fnt.setPointSize(9)
                fnt.setBold(True)
                item.setFont(fnt)
                self.model.appendRow(item)