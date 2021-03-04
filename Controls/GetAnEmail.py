import os
import shutil
import email
import re
import email.parser
import email.header
import email.utils
import traceback


############################
# Get Data of an email
############################


from PyQt5.QtWidgets import QMessageBox, QFileDialog


class GetAnEmail:

    tokenhandler = None
    account = None
    folder_path = ''
    folder = None
    id = ''
    key = ''
    item = None
    eml_temp_path = '../temp/mime.eml'
    temp_dir = '../temp'
    attachment_temp_dir = '../temp/attachments'
    inline_temp_dir = '../temp/inlines'

    msg = None
    subject = ''
    fromwho = ''
    date = ''
    to = ''
    cc = ''
    att = None

    def __init__(self, token_handler, path, id, key):
        try:
            if(os.path.exists(self.temp_dir) == False):
                os.mkdir(self.temp_dir)
            if(os.path.exists(self.eml_temp_path)):
                os.remove(self.eml_temp_path)
            self.id = id
            self.key = key
            self.folder_path = path
            self.tokenhandler = token_handler
            self.account = self.tokenhandler.get_account()
            self.folder = self.account.root
            i = 1
            for s in self.folder_path.split('/////'):
                if (i == 1):
                    i += 1
                    continue
                self.folder = self.folder / s
                i += 1
            self.item = self.folder.get(id=self.id, changekey=self.key)
        except Exception as e:
            messagebox = QMessageBox(QMessageBox.Critical, '获取邮件失败', '获取邮件初始化工作发生异常!\n' + traceback.format_exc())
            messagebox.exec()

    def clear_dir(self, dir):
        list = os.listdir(dir)
        for l in list:
            path = os.path.join(dir,l)
            if(os.path.isdir(path)):
                self.clear_dir(path)
                os.rmdir(path)
            else:
                os.remove(path)

    def write_mime_content_temp_file(self):
        try:
            f = open(self.eml_temp_path, 'wb')
            f.write(self.item.mime_content)
            f.close()
        except Exception as e:
            messagebox = QMessageBox(QMessageBox.Critical, '获取邮件失败', '获取邮件数据缓存文件发生异常!\n' + traceback.format_exc())
            messagebox.exec()


    def read_mime_content_temp_file_to_string(self):
        if(os.path.exits(self.eml_temp_path) == False):
            messagebox = QMessageBox(QMessageBox.Critical, '获取邮件失败', '请先点击一封要操作的邮件！')
            messagebox.exec()
            return ''
        f = open(self.eml_temp_path, 'r')
        temp = f.read()
        f.close()
        return temp

    def decode_eml_header(self, s): # decode content in eml such as ?=gb2312=?B?....?
        res = ''
        if(s == ''):
            return res
        temp = email.header.decode_header(s)
        for t in temp:
            if(t[1] != None):
                try:
                    res = res + t[0].decode(t[1])
                except UnicodeDecodeError as e:
                    if(str(e).index('\'gb2312\' codec can\'t decode') >= 0):
                        res = res + t[0].decode('gb18030')
                continue
            if(isinstance(t[0], str)):
                res = res + t[0]
                continue
            res = res + t[0].decode('ascii')
        return res

    def prase_eml_address_list(self, add_list):
        res = []
        for l in add_list:
            temp = []
            for ll in email.utils.parseaddr(l.strip()):
                temp.append(self.decode_eml_header(ll))
            res.append(temp)
        return res


    def prase_eml_datetime(self, d):
        return email.utils.parsedate_to_datetime(d)

    def get_email_header(self):
        self.subject = self.decode_eml_header(self.msg.get("Subject"))
        if(self.msg.get("From") == None):
            self.fromwho = []
        else:
            self.fromwho = self.prase_eml_address_list(self.decode_eml_header(self.msg.get("From")).split(","))
        if(self.msg.get("To") == None):
            self.to = []
        else:
            self.to = self.prase_eml_address_list(self.decode_eml_header(self.msg.get("To")).split(","))
        if(self.msg.get("Cc") == None):
            self.cc = []
        else:
            self.cc = self.prase_eml_address_list(self.decode_eml_header(self.msg.get("Cc")).split(","))
        if(self.msg.get("Date") == None):
            self.date = ''
        else:
            self.date = self.prase_eml_datetime(self.msg.get("Date"))

    def get_attachments(self):
        if(os.path.exists(self.attachment_temp_dir) == False):
            os.mkdir(self.attachment_temp_dir)
        if(os.path.exists(self.inline_temp_dir) == False):
            os.mkdir(self.inline_temp_dir)
        res_attachments = []
        res_inlines = []
        res = []
        for i in self.msg.walk():
            if(i.get_content_maintype() == 'multipart'):
                continue
            if(i.get_content_disposition() == 'attachment'):
                filename = ''
                filename = i.get_filename()
                if(filename == None):
                    continue
                filename = self.decode_eml_header(filename)
                f = open(self.attachment_temp_dir + '/' + filename, 'wb')
                f.write(i.get_payload(decode=True))
                f.close()
                res_attachments.append('|*独立附件*| ' + filename)
            if(i.get_content_disposition() == 'inline'):
                content_id = ''
                for a in i._headers:
                    if(a[0] == 'Content-ID'):
                        content_id = a[1]
                        content_id = content_id.replace('<', '')
                        content_id = content_id.replace('>', '')
                        break
                content_id = self.decode_eml_header(content_id)
                f = open(self.inline_temp_dir + '/' + content_id, 'wb')
                f.write(i.get_payload(decode=True))
                f.close()
                res_inlines.append('|*内嵌附件*| ' + content_id)
                continue
            for a in i._headers:
                content_id = ''
                if(a[0] == 'Content-ID'):
                    content_id = a[1]
                    content_id = content_id.replace('<', '')
                    content_id = content_id.replace('>', '')
                    content_id = self.decode_eml_header(content_id)
                    f = open(self.inline_temp_dir + '/' + content_id, 'wb')
                    f.write(i.get_payload(decode=True))
                    f.close()
                    res_inlines.append('|*内嵌附件*| ' + content_id)
        res.append(res_attachments)
        res.append(res_inlines)
        self.att = res

    def get_content(self):
        result = ''
        for i in self.msg.walk():
            if(i.get_content_subtype() == 'html'):
                try:
                    result += i.get_payload(decode=True).decode(i.get_content_charset())
                except UnicodeDecodeError as e:
                    if(str(e).index('\'gb2312\' codec can\'t decode') >= 0):
                        result += i.get_payload(decode=True).decode('gb18030')
        return result

    def rend_inlines(self, html):
        pattern = re.compile("src=[\"'](.*?)[\"']")
        str2 = pattern.findall(html)
        dir = os.path.join(os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)).split('ExchangeLite')[0],'ExchangeLite'),'temp'),'inlines')
        for s in str2:
            html = html.replace(s,os.path.join(dir,s.replace("cid:",'')))
        return html

    def get_an_email(self):
        self.write_mime_content_temp_file()
        self.msg = email.message_from_file(open(self.eml_temp_path))
        self.get_email_header()
        self.get_attachments()
        self.item.is_read = True
        self.item.save(update_fields=['is_read'])
        res = []
        res.append(self.subject)
        res.append(self.fromwho)
        try:
            res.append(self.date.strftime('%Y-%m-%d_%H:%M:%S'))
        except Exception as e:
            res.append('时间未知')
        res.append(self.to)
        res.append(self.cc)
        res.append(self.att)
        return res


    def save_eml_file(self):
        if(os.path.exists(self.eml_temp_path) == False):
            QMessageBox(QMessageBox.Critical, '获取邮件失败', '请先点击一封要操作的邮件！').exec()
            return
        s = self.subject
        if(s == ''):
            s = '无标题邮件'
        temp = str(self.date.strftime('%Y-%m-%d_%H:%M:%S')) + s
        reg = r"[\/\\\:\*\?\"\<\>\|]"
        temp = re.sub(reg, "_", temp)
        file_name, filetype = QFileDialog.getSaveFileName(None, '请指定EML邮件归档文件保存路径', '../EMLArchives/' + temp + '.eml', "EML File (*.eml)")
        if(file_name != ''):
            shutil.copyfile(self.eml_temp_path, file_name)