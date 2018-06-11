import enum
import uuid


class Task:
    """Description of Task"""
    def __init__(self, title, start, end, tag, author, observers,
                 reminder, priority, changed=None, description=None, parent=None, tid=None, subtasks=None,
                 is_completed=None, connection=None):
        self.title = title
        if tid is None:
            self.tid = str(uuid.uuid1())
        else:
            self.tid = tid
        self.description = description
        self.priority = priority
        self.start = start
        self.end = end
        self.author = author
        self.tag = tag
        self.observers = observers
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
        self.changed = changed
        if connection is not None:
            self.connection = connection
        else:
            self.connection = []

    def undone(self):
        self.is_completed = Status.undone

    def complete(self):
        self.is_completed = Status.done

    def begin(self):
        self.is_completed = Status.process

    def get_time(self):

        from .data_actions import uuid_to_datetime, str_to_uuid
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


class Tag:
    def __init__(self, name, description=None):
        self.tag_name = name
        self.description = description



class Status(enum.Enum):
    done = 3
    process = 2
    undone = 1

    @classmethod
    def get_status_from_name(cls, name):
        for status, status_name in Status.items():
            if status_name == name:
                return status
        raise ValueError('{} is not instance of Status'.format(name))

    def to_name(self):
        return Status[self.value]

    @staticmethod
    def convert_status_to_str(status):
        return str(Status[status].value)