from PyQt5.QtWidgets import QMessageBox, QDialog
from exchangelib.errors import ErrorAccessDenied
from exchangelib import Message
import time
import re
from UserInterface import InputDestination

class BatchSend():
    path = ''
    tokenhandler = ''
    dir = ''

    def __init__(self, path, tokenhandler):
        self.tokenhandler = tokenhandler
        self.path = path

    def batch_forward(self):
        account = self.tokenhandler.get_account()
        folder = account.root
        i = 1
        for s in self.path.split('/////'):
            if (i == 1):
                i += 1
                continue
            folder = folder / s
            i += 1
        mails = []
        # If an itme is not a message, it may not have all attributes in only(), skip them and just focus on messages!
        try:
            mails = folder.all().order_by('-datetime_received').only('subject', 'datetime_received', 'body')
        except ValueError as e:
            pass
        if (mails.count == 0):
            return '目标目录中没有合法邮件！'

        di = QDialog()
        dests = []
        dest_input_win = InputDestination.Ui_Dialog()
        dest_input_win.setupUi(di, dests)
        di.exec()
        dests = dests[0].split(';')
        jj = 0
        for d in dests:
            dests[jj] = dests[jj].strip()
            jj += 1
        jj = 0
        temp = []
        for jj in range(0,len(dests)):
            if(dests[jj] == ''):
                continue
            temp.append(dests[jj])
        dests = temp
        if(dests == []):
            QMessageBox(QMessageBox.Information,'提示','没有执行转发操作')

        try:
            result = ''
            opetime = str(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()))
            reg = r"[\/\\\:\*\?\"\<\>\|]"
            opetime = re.sub(reg, "_", opetime)

            for m in mails:
                if (isinstance(m, Message) == False):
                    continue
                try:
                    subject = str(m.subject)
                    if(subject == 'None'):
                        subject = '无标题'
                except Exception as e:
                    sbuject = '无标题'
                try:
                    reveive_time = str(m.datetime_received.astimezone())[0:19]
                    if (reveive_time == 'None'):
                        reveive_time = '无收件时间'
                except Exception as e:
                    reveive_time = '无收件时间'
                try:
                    m.forward(subject=subject, body=m.body, to_recipients=dests)
                except Exception as e:
                    result += '*成功* ' + subject + '_' + opetime + '\n'
                    continue
                result += '*成功* ' + subject + '_' + opetime + '\n'
            return result
        except ErrorAccessDenied as e:
            prom = QMessageBox(QMessageBox.Critical, '权限不足', '您无权进入此文件夹！')
            prom.exec()
            return '试图访问无权限文件夹，没有邮件被转发！'