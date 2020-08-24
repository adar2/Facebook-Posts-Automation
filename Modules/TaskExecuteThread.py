from datetime import datetime as dt

from PyQt5.QtCore import QThread, QMutex, pyqtSignal

from Modules.Bot import Bot


class Task(object):
    def __init__(self, task_id, task_name, user_name, password, targets, post, date):
        self.task_id = task_id
        self.task_name = task_name
        self.user_name = user_name
        self.password = password
        self.targets = targets
        self.post = post
        self.date = date
        self.status = 'Init'

    def get_task_id(self):
        return self.task_id

    def get_user_name(self):
        return self.user_name

    def get_password(self):
        return self.password

    def get_targets(self):
        return self.targets

    def get_post(self):
        return self.post

    def get_date(self):
        return self.date

    def get_status(self):
        return self.status

    def get_task_name(self):
        return self.task_name

    def set_status(self, status):
        self.status = status


def calculate_waiting_time(task):
    return (dt.strptime(task.get_date(), '%d/%m/%y %H:%M:%S') - dt.now()).total_seconds()


class TaskExecuteThread(QThread):
    stopped_signal = pyqtSignal()
    started_signal = pyqtSignal()
    task_added_signal = pyqtSignal(str)
    task_removed_signal = pyqtSignal(str)
    task_completed_signal = pyqtSignal(str)
    task_timeout_signal = pyqtSignal(str)
    task_not_found_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.tasks = []
        self.lock = QMutex()
        self.bot = None
        self.waiting_time = 0
        self.running = False

    def run(self):
        self.started_signal.emit()
        while self.running and len(self.tasks) > 0:
            self.lock.lock()
            task = self.tasks[0]
            self.lock.unlock()
            self.waiting_time = calculate_waiting_time(task)
            if self.waiting_time <= 0:
                if task in self.tasks:
                    self.lock.lock()
                    self.tasks.remove(task)
                    self.lock.unlock()
                post = task.get_post()
                if self.bot is None:
                    self.bot = Bot(True)
                if self.bot.doLogin(task.get_user_name(), task.get_password()) == 'Login Successful':
                    for target in task.get_targets():
                        print(self.bot.postToUrl(post[1], post[2], target[1]))
                    task.set_status('completed')
                    self.task_completed_signal.emit(task.get_task_name())
                    self.bot.logout()
                else:
                    print(f'Task executor failed to login to account with email: {task.get_user_name()}')
            if 15 > self.waiting_time > 0:
                self.sleep(int(self.waiting_time))
            else:
                self.sleep(15)
        self.stop()
        self.stopped_signal.emit()

    def stop(self):
        self.running = False

    def start(self, priority=None):
        if not self.isRunning() and not self.running:
            super().start()
            self.running = True

    def add_task(self, task):
        if calculate_waiting_time(task) > 0:
            task.set_status('Pending')
            self.lock.lock()
            self.tasks.append(task)
            self.tasks.sort(key=lambda t: t.get_date())
            self.lock.unlock()
            self.task_added_signal.emit(task.get_task_name())
            if not self.running:
                self.start()
        else:
            self.task_timeout_signal.emit(task.get_task_name())

    def remove_task(self, task):
        if task in self.tasks:
            self.lock.lock()
            self.tasks.remove(task)
            self.lock.unlock()
            self.task_removed_signal.emit(task.get_task_name())
        else:
            self.task_not_found_signal.emit()

    def get_task_by_name(self, task_name):
        for task in self.tasks:
            if task.get_task_name() == task_name:
                return task
        return None
