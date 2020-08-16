from PyQt5 import QtWidgets, QtCore


class Users_Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.username_label = QtWidgets.QLabel(Dialog)
        self.username_label.setObjectName("username_label")
        self.gridLayout.addWidget(self.username_label, 0, 0, 1, 1)
        self.username_line_edit = QtWidgets.QLineEdit(Dialog)
        self.username_line_edit.setObjectName("username_line_edit")
        self.gridLayout.addWidget(self.username_line_edit, 1, 0, 1, 1)
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 2, 0, 1, 1)
        self.password_line_edit = QtWidgets.QLineEdit(Dialog)
        self.password_line_edit.setObjectName("password_line_edit")
        self.gridLayout.addWidget(self.password_line_edit, 3, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Users Dialog"))
        self.username_label.setText(_translate("Dialog", "Username:"))
        self.password_label.setText(_translate("Dialog", "Password:"))