import os
import base64

from exchangelib import Account, Credentials

from PyQt5.QtWidgets import QDialog, QMessageBox
from UserInterface import InputToken


##########################################
# Token Information and Account Connection
##########################################


class TokenHandler:

    token_conf_file_path = '../confs/token.conf'
    current_mail_address = ''
    current_username = ''
    current_password = ''
    account = ''  # Account representing a valid connection to MailBox

    def if_token_conf_file_exists(self):
        if (os.path.exists(self.token_conf_file_path)):
            return True
        return False

    def if_token_ok(self):
        try:
            c = Credentials(self.current_username, self.current_password)
            a = Account(self.current_mail_address, credentials=c, autodiscover=True)
            a.root.refresh()
        except Exception as e:
            return False
        return True

    def parse_token_conf_file(self):
        f = open(self.token_conf_file_path, mode='rb')
        token = f.read()
        token = base64.b64decode(token).decode('utf-8')
        i = 1
        for a in token.split('\n'):
            if (i == 1):
                self.current_mail_address = a
            if (i == 2):
                self.current_username = a
            if (i == 3):
                self.current_password = a
            i += 1
        f.close()

    def write_token_conf_file(self):
        token = self.current_mail_address + '\n' + self.current_username + '\n' + self.current_password
        token = token.encode('utf-8')
        token = base64.b64encode(token)
        f = open(self.token_conf_file_path, mode='wb')
        f.write(token)
        f.close()

    def create_empty_token_conf_file(self):
        f = open(self.token_conf_file_path, mode='wb')
        f.close()

    def delete_token_conf_file(self):
        os.remove(self.token_conf_file_path)

    def input_token(self):
        di = QDialog()
        token_input_window = InputToken.Ui_Dialog()
        token_input_window.setupUi(di, self)
        di.exec()

    def show_token(self):
        msg_box = QMessageBox(QMessageBox.Information, '您当前登录的账户为：', '用户域名：' + self.current_username + '\n' \
                              + '邮箱地址：' + self.current_mail_address)
        msg_box.exec()

    def generate_account(self):
        self.account = Account(self.current_mail_address,
                               credentials=Credentials(self.current_username, self.current_password), autodiscover=True)

    def get_account(self):
        return self.account
