from exchangelib.items import Message
from exchangelib.errors import ErrorAccessDenied
from PyQt5.QtWidgets import QMessageBox

######################################
# Get all e-mail list in a selected DIR
######################################


class GetEmailList:

    path = ''
    tokenhandler = ''

    def __init__(self, path, tokenhandler):
        self.path = path
        self.tokenhandler = tokenhandler

    def get_email_list(self):
        account = self.tokenhandler.get_account()
        folder = account.root
        i = 1
        for s in self.path.split('/////'):
            if(i == 1):
                i += 1
                continue
            folder = folder / s
            i += 1
        #print(folder.id)
        #print(folder.changekey)
        #print(folder.name)
        mails = []
        # If an itme is not a message, it may not have all attributes in only(), skip them and just focus on messages!
        try:
            mails = folder.all().order_by('-datetime_received').only('subject','sender','datetime_received','id','changekey','is_read')
        except ValueError as e:
            pass
        if (mails.count == 0):
            return []
        result = []
        # Some folder can't be handled by normal user, skip then and just focus on those you can!
        try:
            for m in mails:
                if(isinstance(m, Message) == False):
                    print(False)
                    continue
                temp = ''
                try:
                    temp = temp + '|**   标题   **| ' + str(m.subject) + '\n'
                except Exception as e:
                    temp += '|**   标题   **| ' + '无法获取邮件标题\n'
                try:
                    temp = temp + '|**  发件人 **| ' + str(m.sender.name) + ' '
                except Exception as e:
                    temp += '|**  发件人 **| ' + '无法获取发件人 '
                try:
                    temp = temp + str(m.sender.email_address) + '\n'
                except Exception as e:
                    temp += '无法获取发件人邮箱\n'
                try:
                    temp = temp + '|**收件时间**| ' + str(m.datetime_received.astimezone())[0:19] + '\n'
                except Exception as e:
                    temp += '|**收件时间**| ' + '无法获取收件时间\n'
                try:
                    temp = temp + '|**    ID     **| ' + str(m.id) + '\n'
                except Exception as e:
                    temp += '|**    ID     **| ' + '无法获取ID\n'
                try:
                    temp = temp + '|**   KEY    **| ' + str(m.changekey) + '\n'
                except Exception as e:
                    temp += '|**   KEY    **| ' + '无法获取KEY\n'
                try:
                    temp = temp + '|**是否已读**| ' + str(m.is_read)
                except Exception as e:
                    temp += '|**是否已读**| ' + '无法获取是否已读信息'
                result.append(temp)
        except ErrorAccessDenied as e:
            prom = QMessageBox(QMessageBox.Critical, '权限不足','您无权进入此文件夹！')
            prom.exec()
            return []
        return result
