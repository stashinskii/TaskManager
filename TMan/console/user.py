"""
This module represents User class which is used for manage division of tasks between users in CLI app


"""

import enum

from task_manager_library.utility import logging_utils, utils, serialization_utils


class User:

    def __init__(self, name, surname, uid, login, current, tasks=None):
        self.name = name
        self.surname = surname
        self.uid = uid
        self.current = current
        self.login = login
        if tasks is None:
            self.tasks = list()
        else:
            self.tasks = tasks






