from task_manager_library.utility import utils
from task_manager_library.models.task_model import Tag, Priority, Status, Task
from task_manager_library.models.user_model import User
from task_manager_library.models.scheduler_model import Scheduler

from datetime import datetime


def dict_to_task(task_dict):
    """Converting dict object to current Task object"""

    title = task_dict['title']
    start = utils.str_to_date(task_dict['start'])
    end = utils.str_to_date(task_dict['end'])
    desc = task_dict['description']
    tag = Tag(task_dict['tag']['tag_name'], task_dict['tag']['description'])
    observers = task_dict['observers']
    priority = Priority[Priority(int(task_dict['priority'])).name]
    author = task_dict['author']
    reminder = utils.str_to_time(task_dict['reminder'])
    is_completed = Status(int(task_dict['is_completed']))
    parent = task_dict['parent']
    tid = task_dict['tid']
    subtasks = task_dict['subtasks']
    changed = task_dict['changed']
    connection = task_dict['connection']
    height = task_dict['height']

    task = Task(
                title=title, description=desc,
                start=start, end=end,
                tag=tag, author=author,
                observers=observers,
                reminder=reminder, priority=priority,
                height=height, changed=changed,
                parent=parent, tid=tid, subtasks=subtasks,
                is_completed=is_completed, connection=connection
                )
    return task


def dict_to_user(data_dict):
    """Converting dict to user's object"""
    name = data_dict['name']
    surname = data_dict['surname']
    login = data_dict['login']
    uid = data_dict['uid']
    tasks = data_dict['tasks']

    user = User(name=name, surname=surname, uid=uid, login=login, tasks=tasks)
    return user


def task_to_dict(task):
    """Converting Task object to dict"""
    if isinstance(task.start, datetime):
        task.start = date_to_str(task.start)
    if isinstance(task.end, datetime):
        task.end = date_to_str(task.end)
    if isinstance(task.reminder, datetime):
        task.reminder = time_to_str(task.reminder)
    if isinstance(task.priority, Priority):
        task.priority = str(task.priority.value)
    if isinstance(task.is_completed, Status):
        task.is_completed = str(task.is_completed.value)
    if isinstance(task.tag, Tag):
        task.tag = task.tag.__dict__
    return task


def scheduler_to_dict(scheduler):
    """Converting Scheduler object to dict"""
    scheduler.task = task_to_dict(scheduler.task)
    scheduler.task = scheduler.task.__dict__

    if isinstance(scheduler.last, datetime):
        scheduler.last = date_to_str(scheduler.last)
    return scheduler


def dict_to_scheduler(scheduler):
    """Converting dict object to Scheduler object"""
    task = dict_to_task(scheduler['task'])
    last = utils.str_to_date(scheduler['last'])
    uid = scheduler['uid']
    sid = scheduler['sid']
    interval = scheduler['interval']

    return Scheduler(task=task, last=last, uid=uid, sid=sid, interval=interval)


def date_to_str(date):
    """
    Converting datetime objects (Date) to str to serialize them into json
    :param date: datetime object
    :return: str object
    """
    str_date = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return str_date


def time_to_str(time):
    """
    Converting datetime objects (Time) to str to serialize them into json
    :param time: datetime object
    :return: str object
    """
    str_time = str(time.hour) + ":" + str(time.minute)
    return str_time

