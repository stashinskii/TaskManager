import enum

from utility import logging_utils
from utility import serialization_utils
from utility import utils


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






