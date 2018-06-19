import enum
import uuid


class Task:
    """
    Description of Task
    Contains methods to manage status of current task
    """
    def __init__(self,
                 title=None,
                 start=None,
                 end=None,
                 tag=None,
                 author=None,
                 observers=None,
                 reminder=None,
                 priority=None,
                 height=None,
                 changed=None,
                 description=None,
                 parent=None,
                 tid=None,
                 subtasks=None,
                 planned=None,
                 is_completed=None, connection=None):
        self.title = title
        self.planned = planned
        if tid is None:
            self.tid = str(uuid.uuid1())
        else:
            self.tid = tid
        self.description = description
        self.height = height
        if priority is not None:
            self.priority = priority
        else: self.priority = Priority.low
        self.start = start
        self.end = end
        self.author = author
        if tag is None:
            self.tag = Tag("deafult")
        else:
            self.tag = tag
        self.observers = observers
        if is_completed is None:
            self.is_completed = Status.UNDONE
        else:
            self.is_completed = is_completed
        self.reminder = reminder
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
        self.is_completed = Status.UNDONE

    def complete(self):
        self.is_completed = Status.DONE

    def begin(self):
        self.is_completed = Status.PROCESS


class Priority(enum.Enum):
    """Class represents enum of priority"""
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class Tag:
    """
    Class represents tag of task.
    Has optional field description to get more details about tag
    Used to order tasks by their tag
    """
    def __init__(self, name, description=None):
        self.tag_name = name
        self.description = description


class Status(enum.Enum):
    """Class represents enum of task's status"""
    DONE = 3
    PROCESS = 2
    UNDONE = 1