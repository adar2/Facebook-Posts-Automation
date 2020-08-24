import logging
import sqlite3
from Modules.Encryption import DatabaseEncrypt

logging.basicConfig(format=' %(asctime)s - %(message)s', level=logging.WARNING)


# noinspection SqlResolve
class DatabaseWrapper(object):

    def __init__(self):
        self.db_encrypt = DatabaseEncrypt()
        self.db_conn = sqlite3.connect('FB.db')
        self.cursor = self.db_conn.cursor()
        self.cursor.execute('create table if not exists users(ID integer primary key,USER_NAME text ,PASSWORD blob);')
        self.cursor.execute(
            'create table if not exists posts(ID integer primary key,MSG text ,MEDIA text,OWNER_ID integer);')
        self.cursor.execute(
            'create table if not exists targets(ID integer primary key,TARGET_URL text ,OWNER_ID integer);')
        self.cursor.execute(
            'create table if not exists tasks(ID integer primary key,TASK_NAME text not null ,OWNER_ID integer,POST_ID integer,TARGETS text not null ,DATE text not null);')

    def __del__(self):
        self.cursor.close()
        self.db_conn.commit()
        self.db_conn.close()

    def add_user(self, username, password):
        user = self.get_user(username, password)
        if user is not None:
            logging.info("User already exists, aborting..")
            return 'ERROR'
        self.cursor.execute('insert into users (USER_NAME,PASSWORD) values (?,?);',
                            (username, self.db_encrypt.encrypt(password)))
        self.db_conn.commit()
        return 'SUCCESS'

    def edit_user(self, username, password, new_username, new_password):
        user = self.get_user(username, password)
        if user is None:
            logging.info("Can't find the requested user, aborting..")
            return 'ERROR'
        self.cursor.execute("update users set USER_NAME=?,PASSWORD=? where ID is ?;",
                            (new_username, self.db_encrypt.encrypt(new_password), user[0]))
        self.db_conn.commit()
        return 'SUCCESS'

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user is None:
            logging.info("Can't find the requested user, aborting..")
            return 'ERROR'
        self.cursor.execute('delete from users where ID is ?;', (user_id,))
        self.cursor.execute('delete from posts where OWNER_ID is ?;', (user_id,))
        self.cursor.execute('delete from targets where OWNER_ID is ?;', (user_id,))
        self.cursor.execute('delete from tasks where OWNER_ID is ?;', (user_id,))
        self.db_conn.commit()
        return 'SUCCESS'

    def get_user(self, username, password):
        users = self.get_users()
        for user in users:
            if user[1] == username and self.db_encrypt.decrypt(user[2]) == password:
                return user
        return None

    def get_user_by_id(self, user_id):
        self.cursor.execute('select * from users where ID is ?;', (user_id,))
        user = self.cursor.fetchone()
        return user[0], user[1], self.db_encrypt.decrypt(user[2])

    def get_users(self):
        self.cursor.execute('select * from users;')
        users = self.cursor.fetchall()
        return users

    def add_post(self, msg, media, owner_id):
        post = self.get_post(msg, media, owner_id)
        if post is not None:
            logging.warning("Duplicate post , aborting..")
            return 'ERROR'
        self.cursor.execute('insert into posts (MSG,MEDIA,OWNER_ID) values ( ?,?,? );', (msg, media, owner_id))
        self.db_conn.commit()
        return 'SUCCESS'

    def edit_post(self, msg, media, owner_id, new_msg, new_media):
        post = self.get_post(msg, media, owner_id)
        if post is None:
            logging.warning("Can't find the requested post, aborting..")
            return 'ERROR'
        self.cursor.execute('update posts set MSG=?, MEDIA=? where ID is ?;', (new_msg, new_media, post[0]))
        self.db_conn.commit()
        return 'SUCCESS'

    def delete_post(self, msg, media, owner_id):
        post = self.get_post(msg, media, owner_id)
        if post is None:
            logging.warning("Can't find the requested post, aborting..")
            return 'ERROR'
        self.cursor.execute('delete from posts where ID is ?;', (post[0],))
        self.db_conn.commit()
        return 'SUCCESS'

    def get_post(self, msg, media, owner_id):
        self.cursor.execute('select * from posts where MSG is ? and MEDIA is ? and OWNER_ID is ?;',
                            (msg, media, owner_id))
        post = self.cursor.fetchone()
        return post

    def get_post_by_id(self, post_id):
        self.cursor.execute('select * from posts where ID is ?;', (post_id,))
        post = self.cursor.fetchone()
        return post

    def get_posts_by_user_id(self, owner_id):
        self.cursor.execute('select * from posts where OWNER_ID is ?;', (owner_id,))
        posts = self.cursor.fetchall()
        return posts

    def add_target(self, target_url, owner_id):
        target = self.get_target(target_url, owner_id)
        if target is not None:
            logging.warning("Duplicate target , aborting..")
            return 'ERROR'
        self.cursor.execute('insert into targets (TARGET_URL,OWNER_ID) values ( ?,? );', (target_url, owner_id))
        self.db_conn.commit()
        return 'SUCCESS'

    def edit_target(self, target_url, owner_id, new_target_url):
        target = self.get_target(target_url, owner_id)
        if target is None:
            logging.warning("Can't find the requested target, aborting..")
            return 'ERROR'
        self.cursor.execute('update targets set TARGET_URL=? where ID is ?;', (new_target_url, target[0]))
        self.db_conn.commit()
        return 'SUCCESS'

    def delete_target(self, target_url, owner_id):
        target = self.get_target(target_url, owner_id)
        if target is None:
            logging.warning("Can't find the requested target, aborting..")
            return 'ERROR'
        self.cursor.execute('delete from targets where ID=?;', (target[0],))
        self.db_conn.commit()
        return 'SUCCESS'

    def get_target(self, target_url, owner_id):
        self.cursor.execute('select * from targets where TARGET_URL is ? and OWNER_ID is ?;', (target_url, owner_id))
        target = self.cursor.fetchone()
        return target

    def get_target_by_id(self, target_id):
        self.cursor.execute('select * from targets where ID is ?;', (target_id,))
        target = self.cursor.fetchone()
        return target

    def get_targets_by_user_id(self, owner_id):
        self.cursor.execute('select * from targets where OWNER_ID is ?;', (owner_id,))
        targets = self.cursor.fetchall()
        return targets

    def add_task(self, task_name, owner_id, post_id, targets, date):
        task = self.get_task(task_name, owner_id)
        if task is not None:
            logging.warning("Duplicate , aborting..")
            return 'ERROR'
        targets_str = ''
        for target in targets:
            target = self.get_target(target, owner_id)
            if target is not None:
                targets_str += str(target[0]) + ','
        self.cursor.execute('insert into tasks(TASK_NAME,OWNER_ID,POST_ID,TARGETS,DATE) values (?,?,?,?,?);',
                            (task_name, owner_id, post_id, targets_str, date))
        self.db_conn.commit()
        return 'SUCCESS'

    def edit_task(self, task_name, owner_id, new_task_name, new_post_id, new_targets, new_date):
        task = self.get_task(task_name, owner_id)
        if task is None:
            logging.warning("Can't find the requested task, aborting..")
            return 'ERROR'
        targets_str = ''
        for target in new_targets:
            target = self.get_target(target, owner_id)
            if target is not None:
                targets_str += str(target[0]) + ','
        self.cursor.execute('update tasks set TASK_NAME=? , POST_ID=? , TARGETS=? , DATE=? where ID is ?;',
                            (new_task_name, new_post_id, targets_str, new_date, task[0]))
        self.db_conn.commit()
        return 'SUCCESS'

    def delete_task(self, task_name, owner_id):
        task = self.get_task(task_name, owner_id)
        if task is None:
            logging.warning("Can't find the requested task, aborting..")
            return 'ERROR'
        self.cursor.execute('delete from tasks where ID is ?;', (task[0],))
        self.db_conn.commit()
        return 'SUCCESS'

    def get_tasks_by_user_id(self, owner_id):
        self.cursor.execute('select * from tasks where OWNER_ID is ?;', (owner_id,))
        tasks = self.cursor.fetchall()
        return tasks

    def get_task(self, task_name, owner_id):
        self.cursor.execute('select * from tasks where TASK_NAME is ? and OWNER_ID is ?;', (task_name, owner_id))
        task = self.cursor.fetchone()
        return task
