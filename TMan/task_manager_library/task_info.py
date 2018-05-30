import enum

#from .data_actions import *
#from .user_actions import *
from .utility import *


class Task:
    def __init__(self, title, date, description, priority, tid):
        self.title = title
        self.date = date
        self.description = description
        self.priority = priority
        self.tid = tid


class EventCalendar(Task):

    def __init__(self, title, date, description, priority, tid, planned):
        Task.__init__(self, title, date, description, priority, tid)
        self.planned = planned

    def __str__(self):
        return self.title


class TrackedTask:

    def __init__(self, title, desc, start, end, tag, author, observers, executor,
                 reminder, priority, changed, planned, parent=None, tid=None, subtasks=None, is_completed=None):
        self.title = title
        if tid is None:
            self.tid = tid_gen()
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
            self.is_completed = False
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


    def complete(self):
        if self.is_completed:
            self.is_completed = False
        else:
            self.is_completed = True

    def get_time(self):

        from .data_actions import uuid_to_datetime, str_to_uuid
        return uuid_to_datetime(str_to_uuid(self.tid))


class Priority(enum.Enum):

    high = 3
    medium = 2
    low = 1

    @classmethod
    def from_name(cls, name):
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


    def set_current(self):

        self.current = True

    def add_simpletasks(self, tid):
        self.tasks['simple'].append(tid)

    def add_task(self, tid):
        self.tasks['task'].append(tid)


class Scheduler():
    def __init__(self, date, task, sid=None):
        self.date = date
        # param: task Task's object
        self.task = task
        if sid is None:
            self.sid = tid_gen()
        else:
            self.sid = sid





