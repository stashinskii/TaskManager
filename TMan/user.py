import enum

from utility import logging_utils
from utility import serialization_utils
from utility import utils


class Task:

    def __init__(self, title, desc, start, end, tag, author, observers, executor,
                 reminder, priority, changed, planned, parent=None, tid=None, subtasks=None,
                 is_completed=None, connection = None):
        self.title = title
        if tid is None:
            self.tid = serialization_utils.tid_gen()
        else:
            self.tid = tid
        self.description = desc
        self.priority = priority
        self.start = start
        self.end = end
        self.author = author
        self.tag = tag
        self.observers = observers
        self.executor = executor
        if is_completed is None:
            self.is_completed = Status.undone
        else:
            self.is_completed = is_completed
        self.reminder = reminder
        if parent is None:
            self.parent = None
        else:
            self.parent = parent
        self.parent = parent
        if subtasks is None:
            self.subtasks = list()
        else:
            self.subtasks = subtasks
        self.planned = planned
        self.changed = changed
        if connection is not None:
            self.connection = connection
        else:
            self.connection = None

    def undone(self):
        self.is_completed = Status.undone

    def complete(self):
        self.is_completed = Status.done

    def begin(self):
        self.is_completed = Status.process

    def get_time(self):

        from .actions import uuid_to_datetime, str_to_uuid
        return uuid_to_datetime(str_to_uuid(self.tid))


class Priority(enum.Enum):

    high = 3
    medium = 2
    low = 1

    @classmethod
    def get_priority_from_name(cls, name):
        for priority, priority_name in Priority.items():
            if priority_name == name:
                return priority
        raise ValueError('{} is not priority type'.format(name))

    def to_name(self):
        return Priority[self.value]

    @staticmethod
    def convert_priority_to_str(priority):
        return str(Priority[priority].value)




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

class Scheduler():
    def __init__(self, date, task, sid=None):
        self.date = date
        # param: task Task's object
        self.task = task
        if sid is None:
            self.sid = serialization_utils.tid_gen()
        else:
            self.sid = sid





