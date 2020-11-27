from datetime import datetime as dt

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog

from Modules.Bot import Bot
from Modules.DatabaseWrapper import DatabaseWrapper
from Modules.TaskExecuteThread import Task, TaskExecuteThread
from UI.Post_Ui_Dialog import Post_Ui_Dialog
from UI.Targets_Ui_Dialog import Targets_Ui_Dialog
from UI.Task_Ui_Dialog import Tasks_Ui_Dialog
from UI.Users_Ui_Dialog import Users_Ui_Dialog


def now_str():
    return dt.now().strftime("%d/%m/%Y %H:%M:%S")


class Ui_MainWindow(object):
    def __init__(self):
        self.bot = None
        self.db_wrap = DatabaseWrapper()
        self.task_execute = TaskExecuteThread()
        self.media_path = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.existing_users_label = QtWidgets.QLabel(self.centralwidget)
        self.existing_users_label.setObjectName("existing_users_label")
        self.horizontalLayout_2.addWidget(self.existing_users_label)
        self.users_combobox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.users_combobox.sizePolicy().hasHeightForWidth())
        self.users_combobox.setSizePolicy(sizePolicy)
        self.users_combobox.setObjectName("users_combobox")
        self.horizontalLayout_2.addWidget(self.users_combobox)
        self.edit_user_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_user_btn.setObjectName("edit_user_btn")
        self.horizontalLayout_2.addWidget(self.edit_user_btn)
        self.delete_user_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_user_btn.setCheckable(False)
        self.delete_user_btn.setObjectName("delete_user_btn")
        self.horizontalLayout_2.addWidget(self.delete_user_btn)
        self.add_user_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_user_btn.setCheckable(False)
        self.add_user_btn.setObjectName("add_user_btn")
        self.horizontalLayout_2.addWidget(self.add_user_btn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.posts_label = QtWidgets.QLabel(self.centralwidget)
        self.posts_label.setObjectName("posts_label")
        self.verticalLayout_4.addWidget(self.posts_label)
        self.posts_listwidget = QtWidgets.QListWidget(self.centralwidget)
        self.posts_listwidget.setObjectName("posts_listwidget")
        self.verticalLayout_4.addWidget(self.posts_listwidget)
        self.edit_post_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_post_btn.setObjectName("edit_post_btn")
        self.verticalLayout_4.addWidget(self.edit_post_btn)
        self.delete_post_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_post_btn.setObjectName("delete_post_btn")
        self.verticalLayout_4.addWidget(self.delete_post_btn)
        self.add_new_post_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_new_post_btn.setObjectName("add_new_post_btn")
        self.verticalLayout_4.addWidget(self.add_new_post_btn)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.targets_label = QtWidgets.QLabel(self.centralwidget)
        self.targets_label.setObjectName("targets_label")
        self.verticalLayout_3.addWidget(self.targets_label)
        self.targets_listwidget = QtWidgets.QListWidget(self.centralwidget)
        self.targets_listwidget.setObjectName("targets_listwidget")
        self.targets_listwidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.verticalLayout_3.addWidget(self.targets_listwidget)
        self.edit_target_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_target_btn.setObjectName("edit_target_btn")
        self.verticalLayout_3.addWidget(self.edit_target_btn)
        self.delete_target_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_target_btn.setObjectName("delete_target_btn")
        self.verticalLayout_3.addWidget(self.delete_target_btn)
        self.add_target_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_target_btn.setObjectName("add_target_btn")
        self.verticalLayout_3.addWidget(self.add_target_btn)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tasks_label = QtWidgets.QLabel(self.centralwidget)
        self.tasks_label.setObjectName("tasks_label")
        self.verticalLayout_6.addWidget(self.tasks_label)
        self.tasks_listwidget = QtWidgets.QListWidget(self.centralwidget)
        self.tasks_listwidget.setObjectName("tasks_listwidget")
        self.tasks_listwidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.verticalLayout_6.addWidget(self.tasks_listwidget)
        self.edit_task_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_task_btn.setObjectName("edit_task_btn")
        self.verticalLayout_6.addWidget(self.edit_task_btn)
        self.delete_task_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_task_btn.setObjectName("delete_task_btn")
        self.verticalLayout_6.addWidget(self.delete_task_btn)
        self.add_task_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_task_btn.setObjectName("add_task_btn")
        self.verticalLayout_6.addWidget(self.add_task_btn)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.headless_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.headless_checkBox.setObjectName("headless_checkBox")
        self.horizontalLayout_3.addWidget(self.headless_checkBox)
        self.load_file_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_file_btn.setObjectName("load_file_btn")
        self.horizontalLayout_3.addWidget(self.load_file_btn)
        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setObjectName("login_btn")
        self.horizontalLayout_3.addWidget(self.login_btn)
        self.logout_btn = QtWidgets.QPushButton(self.centralwidget)
        self.logout_btn.setObjectName("logout_btn")
        self.horizontalLayout_3.addWidget(self.logout_btn)
        self.post_btn = QtWidgets.QPushButton(self.centralwidget)
        self.post_btn.setObjectName("post_btn")
        self.horizontalLayout_3.addWidget(self.post_btn)
        self.scrape_btn = QtWidgets.QPushButton(self.centralwidget)
        self.scrape_btn.setObjectName("scrape_btn")
        self.horizontalLayout_3.addWidget(self.scrape_btn)
        self.run_tasks_btn = QtWidgets.QPushButton(self.centralwidget)
        self.run_tasks_btn.setObjectName("run_tasks_btn")
        self.horizontalLayout_3.addWidget(self.run_tasks_btn)
        self.stop_tasks_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_tasks_btn.setObjectName("stop_tasks_btn")
        self.horizontalLayout_3.addWidget(self.stop_tasks_btn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.output_label = QtWidgets.QLabel(self.centralwidget)
        self.output_label.setObjectName("output_label")
        self.verticalLayout_5.addWidget(self.output_label)
        self.output_textedit = QtWidgets.QTextEdit(self.centralwidget)
        self.output_textedit.setMinimumSize(QtCore.QSize(256, 0))
        self.output_textedit.setReadOnly(True)
        self.output_textedit.setObjectName("output_textedit")
        self.verticalLayout_5.addWidget(self.output_textedit)
        self.gridLayout.addLayout(self.verticalLayout_5, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.init_users_combobox()
        self.get_user_data()
        self.users_combobox.currentTextChanged.connect(self.get_user_data)
        self.add_user_btn.clicked.connect(self.add_user)
        self.edit_user_btn.clicked.connect(self.edit_user)
        self.delete_user_btn.clicked.connect(self.delete_user)
        self.add_new_post_btn.clicked.connect(self.add_post)
        self.edit_post_btn.clicked.connect(self.edit_post)
        self.delete_post_btn.clicked.connect(self.delete_post)
        self.add_target_btn.clicked.connect(self.add_target)
        self.edit_target_btn.clicked.connect(self.edit_target)
        self.delete_target_btn.clicked.connect(self.delete_target)
        self.login_btn.clicked.connect(self.on_login)
        self.scrape_btn.clicked.connect(self.on_scrape)
        self.post_btn.clicked.connect(self.on_post)
        self.add_task_btn.clicked.connect(self.add_task)
        self.edit_task_btn.clicked.connect(self.edit_task)
        self.delete_task_btn.clicked.connect(self.delete_task)
        self.logout_btn.clicked.connect(self.on_logout)
        self.run_tasks_btn.clicked.connect(self.run_task)
        self.stop_tasks_btn.clicked.connect(self.stop_task)
        self.task_execute.task_added_signal.connect(self.task_added)
        self.task_execute.task_removed_signal.connect(self.task_removed)
        self.task_execute.stopped_signal.connect(self.task_execute_stopped)
        self.task_execute.task_not_found_signal.connect(self.task_not_found)
        self.task_execute.task_timeout_signal.connect(self.task_timeout)
        self.task_execute.task_completed_signal.connect(self.task_completed)
        self.task_execute.started_signal.connect(self.task_execute_started)
        self.load_file_btn.clicked.connect(self.load_data_from_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Facebook-Bot"))
        self.existing_users_label.setText(_translate("MainWindow", "Existing Users:"))
        self.edit_user_btn.setText(_translate("MainWindow", "Edit User"))
        self.delete_user_btn.setText(_translate("MainWindow", "Delete User"))
        self.add_user_btn.setText(_translate("MainWindow", "Add User"))
        self.posts_label.setText(_translate("MainWindow", "Posts:"))
        self.edit_post_btn.setText(_translate("MainWindow", "Edit Post"))
        self.delete_post_btn.setText(_translate("MainWindow", "Delete Post"))
        self.add_new_post_btn.setText(_translate("MainWindow", "Add post"))
        self.targets_label.setText(_translate("MainWindow", "Targets:"))
        self.edit_target_btn.setText(_translate("MainWindow", "Edit Target"))
        self.delete_target_btn.setText(_translate("MainWindow", "Delete Target"))
        self.add_target_btn.setText(_translate("MainWindow", "Add target"))
        self.tasks_label.setText(_translate("MainWindow", "Tasks:"))
        self.edit_task_btn.setText(_translate("MainWindow", "Edit Task"))
        self.delete_task_btn.setText(_translate("MainWindow", "Delete Task"))
        self.add_task_btn.setText(_translate("MainWindow", "Add Task"))
        self.headless_checkBox.setText(_translate("MainWindow", "Hide Browser"))
        self.load_file_btn.setText(_translate("MainWindow", "Load File"))
        self.login_btn.setText(_translate("MainWindow", "Login"))
        self.logout_btn.setText(_translate("MainWindow", "Logout"))
        self.post_btn.setText(_translate("MainWindow", "Post"))
        self.scrape_btn.setText(_translate("MainWindow", "Scrape"))
        self.run_tasks_btn.setText(_translate("MainWindow", "Run Task"))
        self.stop_tasks_btn.setText(_translate("MainWindow", "Stop Task"))
        self.output_label.setText(_translate("MainWindow", "Output:"))

    def init_users_combobox(self):
        self.users_combobox.clear()
        self.users_combobox.addItems({"{}:{}".format(user[0], user[1]) for user in self.db_wrap.get_users()})

    def get_user_data(self):
        user_id = self.get_current_user_id()
        if user_id is None:
            return
        self.targets_listwidget.clear()
        self.targets_listwidget.addItems(
            {'{}'.format(target[1]) for target in self.db_wrap.get_targets_by_user_id(user_id)})
        self.posts_listwidget.clear()
        self.posts_listwidget.addItems({'{} | {}'.format(post[1], post[2]) for post in
                                        self.db_wrap.get_posts_by_user_id(user_id)})
        self.tasks_listwidget.clear()
        self.tasks_listwidget.addItems({task[1] for task in self.db_wrap.get_tasks_by_user_id(user_id)})

    def get_current_user_id(self):
        user_id = self.users_combobox.currentText().split(':')[0]
        return user_id if user_id != '' else None

    def delete_user(self):
        user_id = self.get_current_user_id()
        if user_id is None:
            return
        if self.db_wrap.delete_user(user_id) == 'SUCCESS':
            self.output_textedit.insertPlainText(f"[{now_str()}] User was deleted successfully.\n")
            self.init_users_combobox()
        else:
            self.output_textedit.insertPlainText(f"[{now_str()}] Failed to delete user.\n")

    def edit_user(self):
        def accepted():
            new_username = dialog.ui.username_line_edit.text()
            new_password = dialog.ui.password_line_edit.text()
            if self.db_wrap.edit_user(user[1], user[2], new_username, new_password) == 'SUCCESS':
                self.output_textedit.insertPlainText(f"[{now_str()}] User was edited successfully.\n")
            else:
                self.output_textedit.insertPlainText(f"[{now_str()}] Failed to edit user.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] User editing was canceled.\n")

        user_id = self.get_current_user_id()
        if user_id is None:
            return
        user = self.db_wrap.get_user_by_id(user_id)
        dialog = QDialog()
        dialog.ui = Users_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.ui.username_line_edit.setText(user[1])
        dialog.ui.password_line_edit.setText(user[2])
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.exec_()

    def add_user(self):
        def accepted():
            username = dialog.ui.username_line_edit.text()
            password = dialog.ui.password_line_edit.text()
            if not username or not password:
                self.output_textedit.insertPlainText(f"[{now_str()}] Invalid user values,aborting...\n")
                return
            if self.db_wrap.add_user(username, password) == 'SUCCESS':
                self.output_textedit.insertPlainText(f"[{now_str()}] User was added successfully.\n")
                self.init_users_combobox()
            else:
                self.output_textedit.insertPlainText(f"[{now_str()}] Failed to add user.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] User addition was canceled.\n")

        dialog = QDialog()
        dialog.ui = Users_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.exec_()

    def delete_post(self):
        post = self.posts_listwidget.currentItem()
        if post is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] Select post to delete, aborting...\n")
            return
        user_id = self.get_current_user_id()
        msg = post.text().split(' | ')[0]
        media_path = post.text().split(' | ')[1]
        if media_path == "None":
            media_path = None
        if self.db_wrap.delete_post(msg, media_path, user_id) == 'SUCCESS':
            self.output_textedit.insertPlainText(f"[{now_str()}] Post was deleted successfully.\n")
            self.get_user_data()
        else:
            self.output_textedit.insertPlainText(f"[{now_str()}] Failed to delete post.\n")

    def edit_post(self):
        post = self.posts_listwidget.currentItem()
        if post is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] Select post to edit, aborting...\n")
            return

        def accepted():
            msg = dialog.ui.post_content_text_edit.toPlainText()
            media = self.media_path
            if not msg and not media:
                self.output_textedit.insertPlainText(f"[{now_str()}] Invalid post values, aborting...\n")
                return
            user_id = self.get_current_user_id()
            if self.db_wrap.edit_post(old_msg, old_media_path, user_id, msg, media) == 'SUCCESS':
                self.output_textedit.insertPlainText(f"[{now_str()}] Post was edited successfully.\n")
            else:
                self.output_textedit.insertPlainText(f"[{now_str()}] Failed to edit post.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] Post editing was canceled.\n")

        dialog = QDialog()
        dialog.ui = Post_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        old_msg = post.text().split(' | ')[0]
        old_media_path = post.text().split(' | ')[1]
        if old_media_path == "None":
            old_media_path = None
        dialog.ui.post_content_text_edit.setText(old_msg)
        dialog.ui.browse_media_button.clicked.connect(self.openImageDialog)
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.exec_()
        self.media_path = None
        self.get_user_data()

    def add_post(self):
        def accepted():
            msg = dialog.ui.post_content_text_edit.toPlainText()
            media = self.media_path
            if not msg and not media:
                self.output_textedit.insertPlainText(f"[{now_str()}] invalid post values, aborting...\n")
                return
            if self.db_wrap.add_post(msg, media, user_id) == 'SUCCESS':
                self.output_textedit.insertPlainText(f"[{now_str()}] post was added successfully.\n")
            else:
                self.output_textedit.insertPlainText(f"[{now_str()}] Failed to add new post.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] post addition was canceled.\n")

        user_id = self.get_current_user_id()
        if user_id is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] Create user first, aborting...\n")
            return
        dialog = QDialog()
        dialog.ui = Post_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.ui.browse_media_button.clicked.connect(self.openImageDialog)
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.exec_()
        self.media_path = None
        self.get_user_data()

    def delete_target(self):
        target = self.targets_listwidget.currentItem()
        if target is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] you must select target for editing, aborting...\n")
            return
        user_id = self.get_current_user_id()
        if self.db_wrap.delete_target(target.text(), user_id) == 'SUCCESS':
            self.output_textedit.insertPlainText(f"[{now_str()}] Target was deleted successfully.\n")
            self.get_user_data()
        else:
            self.output_textedit.insertPlainText(f"[{now_str()}] Failed to delete target.\n")

    def edit_target(self):
        target = self.targets_listwidget.currentItem()
        if target is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] you must select target for editing, aborting...\n")
            return

        def accepted():
            user_id = self.get_current_user_id()
            new_target_url = dialog.ui.target_url_line_edit.text()
            if 'facebook.com' not in new_target_url:
                self.output_textedit.insertPlainText(f'[{now_str()}] not a valid facebook url, aborting..\n')
                return
            if self.db_wrap.edit_target(target.text(), user_id, new_target_url) == 'SUCCESS':
                self.output_textedit.insertPlainText(f"[{now_str()}] Target was edited successfully.\n")
                self.get_user_data()
            else:
                self.output_textedit.insertPlainText(f"[{now_str()}] Failed to edit target.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] target editing was canceled.\n")

        dialog = QDialog()
        dialog.ui = Targets_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.ui.target_url_line_edit.setText(target.text())
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.exec_()

    def add_target(self):
        def accepted():

            target = dialog.ui.target_url_line_edit.text()
            if 'facebook.com' not in target:
                self.output_textedit.insertPlainText(f'[{now_str()}] Not a valid facebook url, aborting..\n')
                return
            if self.db_wrap.add_target(target, user_id) == 'SUCCESS':
                self.output_textedit.insertPlainText(f"[{now_str()}] Target added successfully.\n")
                self.get_user_data()
            else:
                self.output_textedit.insertPlainText(f"[{now_str()}] Failed to add new target.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] Target addition was canceled.\n")

        user_id = self.get_current_user_id()
        if user_id is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] Create user first, aborting...\n")
            return
        dialog = QDialog()
        dialog.ui = Targets_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.exec_()

    def add_task(self):
        def accepted():
            if self.task_dialog_data(dialog, user_id) is not None:
                task_name, post_id, targets, date = self.task_dialog_data(dialog, user_id)
                if self.db_wrap.add_task(task_name, user_id, post_id, targets, date) == 'SUCCESS':
                    self.output_textedit.insertPlainText(f"[{now_str()}] Task was added successfully.\n")
                else:
                    self.output_textedit.insertPlainText(f"[{now_str()}] Failed to add new task.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] Task addition was canceled.\n")

        user_id = self.get_current_user_id()
        if user_id is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] Create user first, aborting...\n")
            return
        dialog = QDialog()
        dialog.ui = Tasks_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.ui.posts_listWidget.addItems(
            {'{} | {}'.format(post[1], post[2]) for post in self.db_wrap.get_posts_by_user_id(user_id)})
        dialog.ui.targets_listWidget.addItems(
            {'{}'.format(target[1]) for target in self.db_wrap.get_targets_by_user_id(user_id)})
        dialog.exec_()
        self.get_user_data()

    def task_dialog_data(self, dialog, user_id):
        targets = {target.text() for target in dialog.ui.targets_listWidget.selectedItems()}
        post = dialog.ui.posts_listWidget.currentItem()
        date = dialog.ui.dateTimeEdit.dateTime().toString("dd/MM/yy hh:mm:ss")
        task_name = dialog.ui.task_name_line_edit.text()
        if len(targets) == 0 or post is None or task_name == '':
            self.output_textedit.insertPlainText(f"[{now_str()}] Task editing was canceled.\n")
            return None
        msg, media = (post.text().split(' | ')[0], post.text().split(' | ')[1])
        if media == 'None':
            media = None
        post_id = self.db_wrap.get_post(msg, media, user_id)[0]
        return task_name, post_id, targets, date

    def edit_task(self):
        def accepted():
            if self.task_dialog_data(dialog, user_id) is not None:
                task_name, post_id, targets, date = self.task_dialog_data(dialog, user_id)
                if self.db_wrap.edit_task(task.text(), user_id, task_name, post_id, targets, date) == 'SUCCESS':
                    self.output_textedit.insertPlainText(f"[{now_str()}] Task was edited successfully.\n")
                    self.get_user_data()
            else:
                self.output_textedit.insertPlainText(f"[{now_str()}] Failed to edit  task.\n")

        def rejected():
            self.output_textedit.insertPlainText(f"[{now_str()}] Task editing was canceled.\n")

        task = self.tasks_listwidget.currentItem()
        if task is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] you must select target for editing, aborting...\n")
            return
        user_id = self.get_current_user_id()
        dialog = QDialog()
        dialog.ui = Tasks_Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.ui.buttonBox.accepted.connect(accepted)
        dialog.ui.buttonBox.rejected.connect(rejected)
        dialog.ui.posts_listWidget.addItems(
            {'{} | {}'.format(post[1], post[2]) for post in self.db_wrap.get_posts_by_user_id(user_id)})
        dialog.ui.targets_listWidget.addItems(
            {'{}'.format(target[1]) for target in self.db_wrap.get_targets_by_user_id(user_id)})
        dialog.ui.task_name_line_edit.setText(task.text())
        dialog.exec_()

    def delete_task(self):
        task = self.tasks_listwidget.currentItem()
        if task is None:
            self.output_textedit.insertPlainText(f"[{now_str()}] You must select target for editing, aborting...\n")
            return
        if self.db_wrap.delete_task(task.text(), self.get_current_user_id()) == 'SUCCESS':
            self.output_textedit.insertPlainText(f"[{now_str()}] Task was deleted successfully.\n")
            self.get_user_data()
        else:
            self.output_textedit.insertPlainText(f"[{now_str()}] Failed to delete task.\n")

    def get_task_obj(self, task):
        if task is None:
            self.output_textedit.insertPlainText(f'[{now_str()}] You must select a task, aborting... ')
            return
        user_id = self.get_current_user_id()
        task = self.db_wrap.get_task(task.text(), user_id)
        user = self.db_wrap.get_user_by_id(user_id)
        targets = []
        for target_id in task[4].split(',', maxsplit=task[4].count(',')):
            target = self.db_wrap.get_target_by_id(target_id)
            if target is not None:
                targets.append(target)
        post = self.db_wrap.get_post_by_id(task[3])
        task_obj = Task(task[0], task[1], user[1], user[2], targets, post, task[5])
        return task_obj

    def run_task(self):
        tasks = self.tasks_listwidget.selectedItems()
        for task in tasks:
            task_obj = self.get_task_obj(task)
            task_name = task_obj.get_task_name()
            if task_obj is not None and self.task_execute.get_task_by_name(task_name) is None:
                self.task_execute.add_task(task_obj)

    def stop_task(self):
        task = self.tasks_listwidget.currentItem()
        if task is None:
            self.output_textedit.insertPlainText(f'[{now_str()}] You must select a task, aborting... ')
            return
        task_obj = self.task_execute.get_task_by_name(task.text())
        if task_obj is not None:
            self.task_execute.remove_task(task_obj)

    def task_added(self, task_name):
        self.output_textedit.insertPlainText(f'[{now_str()}] Task with task name: {task_name} has been added.\n')

    def task_removed(self, task_name):
        self.output_textedit.insertPlainText(f'[{now_str()}] Task with task name: {task_name} has been removed.\n')

    def task_execute_started(self):
        self.output_textedit.insertPlainText(f'[{now_str()}] Task executor started.\n')

    def task_execute_stopped(self):
        self.output_textedit.insertPlainText(f'[{now_str()}] Task executor stopped.\n')

    def task_not_found(self):
        self.output_textedit.insertPlainText(f'[{now_str()}] Task not found.\n')

    def task_timeout(self, task_name):
        self.output_textedit.insertPlainText(f'[{now_str()}] Task timeout with task name: {task_name}\n')

    def task_completed(self, task_name):
        self.output_textedit.insertPlainText(
            f'[{now_str()}] Task with task name: {task_name} completed successfully \n')

    def openImageDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose media file", "",
                                                  "Mobile Video(*.3g2);;Mobile Video(*.3gp);;Mobile Video(*.3gpp);;Windows Media Video(*.asf);;AVI(*.avi);;MPEG Video(*.dat);;DIVX Video(*.divx);;DV Video(*.dv);;Flash Video(*.f4v);;Flash Video(*.flv);;Graphics Interchange Format(*.gif);;M2TS Video(*.m2ts);;MPEG-4 Video(*.m4v);;Matroska Format(*.mkv);;MOD Video(*.mod);;QuickTime Movie(*.mov);;MPEG-4 Video(*.mp4);;MPEG Video(*.mpe);;MPEG Video(*.mpeg);;MPEG-4 Video(*.mpeg4);;MPEG Video(*.mpg);;AVCHD Video(*.mts);;Nullsoft Video(*.nsv);;Ogg Media Format(*.ogm);;Ogg Video Format(*.ogv);;QuickTime Movie(*.qt);;TOD Video(*.tod);;MPEG Transport Stream(*.ts);;DVD Video(*.vob);;Windows Media Video(*.wmv);;BMP(*.bmp);;DIB(*.dib);;HEIC(*.heic);;HEIF(*.heif);;IFF(*.iff);;JFIF(*.jfif);;JP2(*.jp2);;JPE(*.jpe);;JPEG(*.jpeg);;JPG(*.jpg);;PNG(*.png);;PSD(*.psd);;TIF(*.tif);;TIFF(*.tiff);;WBMP(*.wbmp);;WEBP(*.webp);;XBM(*.xbm)",
                                                  options=options)
        if fileName:
            self.media_path = fileName

    def on_logout(self):
        self.output_textedit.insertPlainText(f'[{now_str()}] {self.bot.logout()}\n')
        self.users_combobox.setEnabled(True)
        self.edit_user_btn.setEnabled(True)
        self.delete_user_btn.setEnabled(True)

    def on_login(self):
        user_id = self.get_current_user_id()
        if user_id is None:
            return
        current_user = self.db_wrap.get_user_by_id(user_id)
        user_val = current_user[1]
        pass_val = current_user[2]
        if not self.bot:
            self.bot = Bot(self.headless_checkBox.isChecked())
        else:
            self.bot.check_browser_state()
        self.output_textedit.insertPlainText(f'[{now_str()}] {self.bot.doLogin(user_val, pass_val)}\n')
        self.users_combobox.setEnabled(False)
        self.edit_user_btn.setEnabled(False)
        self.delete_user_btn.setEnabled(False)

    def on_scrape(self):
        if self.bot is None or not self.bot.logged_in:
            self.output_textedit.insertPlainText(f'[{now_str()}] You need to log in first.\n')
            return
        url_val = self.targets_listwidget.currentItem()
        if url_val is None or url_val.text() == '':
            self.output_textedit.insertPlainText(f'[{now_str()}] Invalid url value.\n')
            return
        self.output_textedit.insertPlainText(f'[{now_str()}] Scraping data for {url_val.text()} .\n')
        self.output_textedit.insertPlainText(f'{self.bot.groupScraper(url_val.text())}\n')

    def on_post(self):
        if self.bot is None or not self.bot.logged_in:
            self.output_textedit.insertPlainText(f'[{now_str()}] You need to log in first.\n')
            return
        post = self.posts_listwidget.currentItem()
        if post is None:
            self.output_textedit.insertPlainText(f'[{now_str()}] You need Image or Message to post.\n')
            return
        targets = self.targets_listwidget.selectedItems()
        if len(targets) == 0:
            self.output_textedit.insertPlainText(f'[{now_str()}] You need url to post.\n')
            return
        media = post.text().split(' | ')[1]
        msg = post.text().split(' | ')[0]
        if len(targets) == 1:
            target = targets.pop().text()
            self.output_textedit.insertPlainText(
                f'[{now_str()}] {self.bot.postToUrl(url=target, media_path=media, message=msg)}.\n')
        else:
            for target in targets:
                self.output_textedit.insertPlainText(
                    f'[{now_str()}] {self.bot.postToUrl(url=target.text(), media_path=media, message=msg)}.\n')

    def load_data_from_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file", options=options)
        if fileName:
            if self.db_wrap.load_data(file_path=fileName, owner_id=self.get_current_user_id()) == 'SUCCESS':
                self.output_textedit.insertPlainText(f'[{now_str()}] Successfully loaded the file.\n')
            else:
                self.output_textedit.insertPlainText(
                    f'[{now_str()}] Something went wrong while trying to load the file.\n')
            self.get_user_data()
