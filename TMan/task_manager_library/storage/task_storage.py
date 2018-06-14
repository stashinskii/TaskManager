"""
This module represents Storage class which is contains methods to manage tasks, schedulers,
users, serialize them and store in their JSON files.

All methods describes logic of resaving and loading files from JSON
"""
import json
import os
from datetime import datetime
import configparser

from task_manager_library.utility import utils
from task_manager_library.storage import serialization
from task_manager_library.models.task_model import Tag, Priority
from task_manager_library.models.user_model import User


class Storage:
    """
    Represents task's storage manager
    Used to serialize and store data of application in JSON format
    """
    def __init__(self, configuration=None, external_user=None):
        if configuration is not None and configuration.get('storage_path') is not None:
            self.path = configuration.get('storage_path')
        else:
            self.path = os.path.dirname(__file__) + "/tmandata/"
        if external_user is not None:
            self.current_uid = external_user
        else:
            try:
                utils.check_json_files(self.path, 'users.json')
                utils.check_cfg_files(self.path, 'current.ini')
                config = configparser.ConfigParser()
                config.read(self.path+'current.ini')
                section = "USER"
                uid = config.get(section, "uid")
                self.current_uid = uid
            except Exception as e:
                self.current_uid = None
        self.tasks = []
        self.user_tasks = []

    # region Loading data

    def load_users_from_json(self):
        """Load user's information from storage"""
        utils.check_json_files(self.path, '/users.json')
        with open(self.path + '/users.json', 'r') as file:
            data = json.load(file)
        users = list()

        for data_dict in data:
            user = serialization.dict_to_user(data_dict)
            users.append(user)
        return users

    def load_user(self, uid):
        """Get user object from its UID"""
        users = self.load_users_from_json()
        for user in users:
            if user.uid == uid:
                return user

    def get_uid_by_login(self, login):
        """Get user ID from login"""
        users = self.load_users_from_json()
        return next((user.uid for user in users if user.login == login), None)

    def change_user_config(self, login):
        """Change and save configuration .ini file of current user"""
        user_uid = self.get_uid_by_login(login)
        config = configparser.ConfigParser()
        section = "USER"
        config.read(self.path+'/current.ini')
        exist = config.has_section(section)
        if not exist:
            config.add_section(section)
        config.set(section, 'uid', user_uid)

        with open(self.path+'/current.ini', 'w+') as f:
            config.write(f)

    def load_tasks_from_json(self):
        """Load all tasks from json file"""
        utils.check_json_files(self.path, '/tasks.json')

        if self.tasks:
            return

        with open(self.path + 'tasks.json', 'r') as task_file:
            task_data = json.load(task_file)

        for task_dict in task_data:
            loaded_task = serialization.dict_to_task(task_dict)
            self.tasks.append(loaded_task)

    def load_user_tasks(self):
        """Load only user's files"""
        if not self.tasks:
            self.load_tasks_from_json()

        if self.user_tasks:
            return

        current_user = self.load_user(self.current_uid)
        for task in self.tasks:
            if task.tid in current_user.tasks:
                self.user_tasks.append(task)
    # endregion

    # region Tasks actions
    def add_task(self, task):
        """Adding new task and save it to json file"""
        self.load_tasks_from_json()
        self.tasks.append(task)
        self.write_tid_to_user(task.tid, self.current_uid)
        self.resave()

    def resave(self):
        """Resave tasks collection"""
        data = []
        for task in self.tasks:
            task = serialization.task_to_dict(task)
            data.append(task.__dict__)

        with open(self.path + '/tasks.json', 'w') as taskfile:
            json.dump(data, taskfile, indent=2, ensure_ascii=False)

    def delete(self, tid):
        self.load_tasks_from_json()
        if len(self.tasks) == 0:
            raise IndexError("Nothing to delete")
        index = utils.get_task_index(tid, self)
        del self.tasks[index]
        self.resave()

    def edit(self, tid, **kwargs):

        self.load_tasks_from_json()
        index = utils.get_task_index(tid, self)

        title = kwargs.get('title')
        if title is not None:
            self.tasks[index].title = title

        description = kwargs.get('description')
        if description is not None:
            self.tasks[index].description = description

        priority = kwargs.get('priority')
        if priority is not None:
            self.tasks[index].priority = Priority[priority]

        tag = kwargs.get('tag')
        if tag is not None:
            self.tasks[index].tag = Tag(tag)

        end = kwargs.get('end')
        if end is not None:
            self.tasks[index].end = utils.str_to_date(end)

        self.resave()

    def link(self, first_id, second_id):
        """Make link between two tasks by their task ID"""
        self.load_tasks_from_json()
        first_index = utils.get_task_index(first_id, self)
        second_index = utils.get_task_index(second_id, self)

        self.tasks[first_index].connection.append(second_id)
        self.tasks[second_index].connection.append(first_id)

        self.resave()

    def give_task_permission(self, observer, tid):
        """Give permission to task (tid) to other users/observers"""
        uid = self.get_uid_by_login(observer)
        self.write_tid_to_user(tid, uid)

    def write_tid_to_user(self, tid, uid):
        """Add info of task to user"""
        users = self.load_users_from_json()
        current_user = self.load_user(uid)

        index = utils.get_user_index(uid, users)
        del users[index]
        current_user.tasks.append(tid)
        users.append(current_user)

        users = [user.__dict__ for user in users]

        with open(self.path + '/users.json', 'w') as userfile:
            json.dump(users, userfile, indent=2, ensure_ascii=False)

    # endregion

    # region Changing status
    def complete_task(self, tid):
        self.load_tasks_from_json()
        index = utils.get_task_index(tid, self)
        self.tasks[index].complete()
        self.resave()

    def uncomplete_task(self, tid):
        self.load_tasks_from_json()
        index = utils.get_task_index(tid, self)
        self.tasks[index].undone()
        self.resave()

    def begin_task(self, tid):
        self.load_tasks_from_json()
        index = utils.get_task_index(tid, self)
        self.tasks[index].begin()
        self.resave()

    # endregion

    # region User actions

    def save_new_user_to_json(self, user):
        users = self.load_users_from_json()
        users.append(user)
        self.resave_users(users)

    def resave_users(self, users):
        users = [user.__dict__ for user in users]
        with open(self.path + '/users.json', 'w') as taskfile:
            json.dump(users, taskfile, indent=2, ensure_ascii=False)

    # enregion

