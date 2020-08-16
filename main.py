import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from UI.Ui_MainWindow import Ui_MainWindow


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()
