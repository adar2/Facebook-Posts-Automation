from PyQt5 import QtWidgets, QtCore


class Post_Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.post_content_label = QtWidgets.QLabel(Dialog)
        self.post_content_label.setObjectName("post_content_label")
        self.verticalLayout.addWidget(self.post_content_label)
        self.post_content_text_edit = QtWidgets.QTextEdit(Dialog)
        self.post_content_text_edit.setObjectName("post_content_text_edit")
        self.verticalLayout.addWidget(self.post_content_text_edit)
        self.media_label = QtWidgets.QLabel(Dialog)
        self.media_label.setObjectName("media_label")
        self.verticalLayout.addWidget(self.media_label)
        self.browse_media_button = QtWidgets.QPushButton(Dialog)
        self.browse_media_button.setObjectName("browse_media_button")
        self.verticalLayout.addWidget(self.browse_media_button)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Posts Dialog"))
        self.post_content_label.setText(_translate("Dialog", "Post content:"))
        self.media_label.setText(_translate("Dialog", "Media:"))
        self.browse_media_button.setText(_translate("Dialog", "Browse.."))