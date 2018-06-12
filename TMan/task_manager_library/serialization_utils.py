from console.user_actions import User
from task_manager_library import utils
from task_manager_library.models.task_model import Tag, Priority, Status, Task

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
    is_completed = Status[Status(int(task_dict['is_completed'])).name]
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
    name = data_dict['name']
    surname = data_dict['surname']
    login = data_dict['login']
    uid = data_dict['uid']
    tasks = data_dict['tasks']

    user = User(name=name, surname=surname, uid=uid, login=login, tasks=tasks)
    return user


def task_to_dict(task):
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

