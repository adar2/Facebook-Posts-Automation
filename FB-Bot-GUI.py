import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, \
    QTextBrowser, QFileDialog,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from Bot import Bot


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.scrape = QPushButton('Scrape url', self)
        self.login = QPushButton('Login', self)
        self.img = QPushButton('Image File', self)
        self.urls = QPushButton('Urls File', self)
        self.post = QPushButton('Post', self)
        self.multi_post = QPushButton('Multi Post', self)
        self.data_box = QMessageBox(self)
        self.url_box = QLineEdit(self)
        self.pass_box = QLineEdit(self)
        self.pass_box.setEchoMode(QLineEdit.Password)
        self.outbox = QTextBrowser(self)
        self.user_box = QLineEdit(self)
        self.message_box = QLineEdit(self)
        self.title = 'FacebookBot'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800
        self.bot = None
        self.media_path = ''
        self.group_path = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.outbox.move(500, 20)
        self.outbox.resize(600, 300)

        # Create textbox
        self.user_box.move(95, 20)
        self.user_box.resize(280, 40)

        self.pass_box.move(95, 80)
        self.pass_box.resize(280, 40)

        self.url_box.move(95, 140)
        self.url_box.resize(280, 40)

        self.message_box.move(95, 200)
        self.message_box.resize(280, 40)

        self.data_box.move(400, 140)
        self.data_box.resize(280, 280)

        email_label = QLabel('Email:', self)
        email_label.move(20, 20)

        pass_label = QLabel('Password:', self)
        pass_label.move(20, 80)

        url_label = QLabel('Url:', self)
        url_label.move(20, 140)

        message_label = QLabel('Message:', self)
        message_label.move(20, 200)

        # Create a button in the window
        self.scrape.move(20, 260)

        self.login.move(140, 260)

        self.img.move(260, 260)

        self.urls.move(20, 320)

        self.post.move(140, 320)

        self.multi_post.move(260, 320)

        # connect button to function on_click
        self.login.clicked.connect(self.on_login)
        self.img.clicked.connect(self.openImageDialog)
        self.urls.clicked.connect(self.openGroupDialog)
        self.scrape.clicked.connect(self.on_scrape)
        self.post.clicked.connect(self.on_post)
        self.multi_post.clicked.connect(self.on_multi_post)

        self.show()

    @pyqtSlot()
    def on_login(self):
        user_val = self.user_box.text()
        pass_val = self.pass_box.text()
        if user_val != '' and pass_val != '':
            self.bot = Bot(user_val, pass_val)
        else:
            self.outbox.setText('Invalid credentials')

    def on_scrape(self):
        if self.bot is None or not self.bot.logged_in:
            self.outbox.setText('You need to log in first')
            return
        url_val = self.url_box.text()
        if url_val == '':
            self.outbox.setText('Invalid url value')
        self.outbox.setText(self.bot.groupScraper(url_val))

    def on_post(self):
        if self.bot is None or not self.bot.logged_in:
            self.outbox.setText('You need to log in first')
            return
        if self.media_path == '' and self.message_box.text() == '':
            self.outbox.setText('You need Image or Message to post')
            return
        if self.url_box.text() == '':
            self.outbox.setText('You need url to post')
            return
        self.bot.postToUrl(url=self.url_box.text(), media_path=self.media_path, message=self.message_box.text())

    def on_urls(self):
        if self.bot is None or not self.bot.logged_in:
            self.outbox.setText('You need to log in first')
            return
        self.outbox.setText('Keep in mind you need each line look like this: url,media_path,message_path,')

    def on_multi_post(self):
        if self.bot is None or not self.bot.logged_in:
            self.outbox.setText('You need to log in first')
            return
        if self.group_path == '':
            self.outbox.setText('You have to select text file first!')
            return
        self.bot.multiPost(self.group_path)

    def openImageDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.media_path = fileName

    def openGroupDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.group_path = fileName


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
