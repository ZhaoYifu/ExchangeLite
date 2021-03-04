import shutil

from PyQt5.QtWidgets import QFileDialog, QMessageBox


class ArchiveAttachment():
    model = None
    indexs = None
    def __init__(self,model,indexs):
        self.model = model
        self.indexs = indexs
    def archive_attachment(self):
        dir = QFileDialog.getExistingDirectory(None, '请指定附件保存路径', '../ATTArchives')
        for i in self.indexs:
            target = ''
            filename = self.model.itemFromIndex(i).text()[9:]
            type = self.model.itemFromIndex(i).text()[:9]
            if(dir):
                target = dir + '/' + filename
                if(type == '|*独立附件*| '):
                    shutil.copyfile('../temp/attachments/' + filename, target)
                if(type == '|*内嵌附件*| '):
                    shutil.copyfile('../temp/inlines/' + filename, target)
                continue
            return