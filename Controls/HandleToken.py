import sys

from PyQt5.QtWidgets import QMessageBox

#############################################
# Check if local token conf file exists,
# Check if local token is valid,
# Ask user to input token when local token is not valid,
# Save valid token to local conf file
#############################################


class HandleToken:

    token_handler = ''

    def __init__(self,tokenhandler):
        self.token_handler = tokenhandler

    def handle_token(self):
        if (self.token_handler.if_token_conf_file_exists() == False):
            self.token_handler.create_empty_token_conf_file()
            self.token_handler.input_token()
        self.token_handler.parse_token_conf_file()
        i = 0
        while (self.token_handler.if_token_ok() == False):
            msg_box = QMessageBox(QMessageBox.Critical, '错误', '身份认证失败，请输入身份认证信息！')
            msg_box.exec()
            self.token_handler.input_token()
            i += 1
            if (i == 3):
                msg_box = QMessageBox(QMessageBox.Critical, '错误', '连续三次失败，程序将退出！')
                msg_box.exec()
                sys.exit()
        self.token_handler.write_token_conf_file()
        self.token_handler.parse_token_conf_file()
        self.token_handler.generate_account()

    def show_token(self):
        self.token_handler.show_token()
