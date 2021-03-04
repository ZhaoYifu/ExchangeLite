from PyQt5.QtWidgets import QMessageBox, QFileDialog
from exchangelib import Message
from exchangelib.errors import ErrorAccessDenied
from exchangelib.attachments import  FileAttachment
import os
import re
import time


class BatchArchive():
    path = ''
    tokenhandler = ''
    dir = ''

    def __init__(self, path, tokenhandler):
        self.path = path
        self.tokenhandler = tokenhandler


    def batch_archive_eml(self):
        self.dir = QFileDialog.getExistingDirectory(None, '请指定批量归档保存路径', '../BATArchives')
        if(self.dir == ''):
            return '没有指定保存路径！'
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
            mails = folder.all().only('subject', 'datetime_received', 'mime_content')
        except ValueError as e:
            pass
        if (mails.count == 0):
            return '目标目录中没有合法邮件！'
        # Some folder can't be handled by normal user, skip then and just focus on those you can!
        try:
            result = ''
            opetime = str(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()))
            reg = r"[\/\\\:\*\?\"\<\>\|]"
            opetime = re.sub(reg, "_", opetime)
            savepath = os.path.abspath(self.dir + '\\EML_BAT_' + opetime)
            if (os.path.exists(savepath) == False):
                os.mkdir(savepath)
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
                    mime_content = m.mime_content
                except Exception as e:
                    mime_content = b'No Mime Content Available!'
                savefilename = savepath + '\\' + re.sub(reg, "_", subject + "_" + reveive_time) + '.eml'
                try:
                    f = open(savefilename, 'wb')
                    f.write(mime_content)
                    f.close()
                    result += '*成功* '+savefilename+ '\n'
                except Exception as e:
                    result += '*失败* '+savefilename+ '\n'
            return result
        except ErrorAccessDenied as e:
            prom = QMessageBox(QMessageBox.Critical, '权限不足', '您无权进入此文件夹！')
            prom.exec()
            return '试图访问无权限文件夹，没有EML被导出！'

    def batch_archive_attachments(self):
        self.dir = QFileDialog.getExistingDirectory(None, '请指定批量附件保存路径', '../BATArchives')
        if (self.dir == ''):
            return '没有指定保存路径！'
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
            mails = folder.all().only('subject', 'datetime_received', 'attachments')
        except ValueError as e:
            pass
        if (mails.count == 0):
            return '目标目录中没有合法邮件！'
        # Some folder can't be handled by normal user, skip then and just focus on those you can!
        try:
            result = ''
            opetime = str(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()))
            reg = r"[\/\\\:\*\?\"\<\>\|]"
            opetime = re.sub(reg, "_", opetime)
            savepath = os.path.abspath(self.dir + '\\ATTACH_BAT_' + opetime)
            if (os.path.exists(savepath) == False):
                os.mkdir(savepath)
            for m in mails:
                rootpath = ''
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

                attachments = []
                try:
                    attachments = m.attachments
                except Exception as a:
                    result += '*失败* ' + subject + '_' + reveive_time + '_ALL' + '\n'

                rootpath = savepath + '\\' + re.sub(reg, "_", subject + "_" + reveive_time)
                if(os.path.exists(rootpath) == False):
                    os.mkdir(rootpath)
                for a in attachments:
                    if(isinstance(a, FileAttachment)):
                        if(a.is_inline):
                            try:
                                targetpath = rootpath + '\\inline'
                                if(os.path.exists(targetpath) == False):
                                    os.mkdir(targetpath)
                                filename = targetpath + '\\' + a.content_id
                                f = open(filename, 'wb')
                                f.write(a.content)
                                f.close()
                            except Exception as e:
                                result += '*失败* ' + subject + '_' + reveive_time + '_INLINE_:' + a.content_id + '\n'
                                print(e)
                                continue
                            result += '*成功* ' + subject + '_' + reveive_time + '_INLINE_:' + a.content_id + '\n'
                        else:
                            try:
                                targetpath = rootpath + '\\stand_alone'
                                if(os.path.exists(targetpath) == False):
                                    os.mkdir(targetpath)
                                filename = targetpath + '\\' + a.name
                                f = open(filename, 'wb')
                                f.write(a.content)
                                f.close()
                            except Exception as e:
                                result += '*失败* ' + subject + '_' + reveive_time + '_ATT_:' + a.name + '\n'
                                print(e)
                                continue
                            result += '*成功* ' + subject + '_' + reveive_time + '_ATT_:' + a.name + '\n'
            if(result == ''):
                result = '没有检测到任何附件！'
            return result
        except ErrorAccessDenied as e:
            prom = QMessageBox(QMessageBox.Critical, '权限不足', '您无权进入此文件夹！')
            prom.exec()
            return '试图访问无权限文件夹，没有附件被导出！'