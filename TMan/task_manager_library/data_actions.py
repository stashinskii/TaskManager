import json
import logging
import os
import uuid
import config
from datetime import datetime

from utility import utils
from utility import serialization_utils
from utility import logging_utils

from .data_storage import *
from .task_info import *
from .user_actions import *
from utility.utils import *


data_dir = os.environ['HOME']+'/tmandata'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


@logging_utils.logger
def add_tracked_task(title=None, desc=None, start=None, end=None,
                     tag=None, observers=None,
                     reminder=None, priority=None,
                     changed=None, planned=None, executor=None):
    """Adding new task"""
    tasks, all, all_users_tasks = DataStorage.load_tasks_from_json()
    current = UserTools.get_current_user()
    observers = serialization_utils.split_str_to_list(observers, current)
    priority = Priority.convert_priority_to_str(priority)
    author = UserTools.get_current_user().uid
    task = TrackedTask(title, desc, start, end, tag, author, observers, executor,
                       reminder, priority, changed, planned)
    all_users_tasks.append(task)
    check_date_range(start, end)
    DataStorage.resave_all_tasks_to_json(all_users_tasks, task)


@logging_utils.logger
def add_subtask(index, title=None, desc=None, start=None, end=None,
                tag=None, observers=None,
                reminder=None, priority=None,
                changed=None, planned=None, executor=None):

    """Adding new subtask task"""
    current = UserTools.get_current_user()
    observers = serialization_utils.split_str_to_list(observers, current)
    priority = Priority.convert_priority_to_str(priority)
    author = UserTools.get_current_user().uid

    tasks, all, all_users_tasks = DataStorage.load_tasks_from_json()
    parent_id = tasks[index - 1].tid

    task = TrackedTask(title, desc, start, end, tag, author, observers, executor,
                       reminder, priority, changed, planned, parent_id)
    all_users_tasks.append(task)
    global_index = get_task_index(parent_id, all_users_tasks)
    all_users_tasks[global_index].subtasks.append(task.tid)
    check_date_range(start, end)
    DataStorage.resave_all_tasks_to_json(all_users_tasks, task)


@logging_utils.logger
def edit_task(task_num, task_field):
    tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
    current = UserTools.get_current_user()
    author_name = tasks[task_num - 1].author
    if author_name != current.uid:
        raise ValueError("Access denied")

    if (task_num - 1) > len(tasks):
        raise IndexError("Out of range")
    edit = tasks[task_num - 1]
    task_index = all_users_tasks.index(edit)
    data = list()
    data.extend((edit.title, edit.start.date(), edit.end.date(), edit.description))

    if task_field == "title":
        data = open_nano(data, 0)
    elif task_field == "start":
        data = open_nano(data, 1)
    elif task_field == "end":
        data = open_nano(data, 2)
    elif task_field == "description":
        data = open_nano(data, 3)
    else:
        raise ValueError("ERROR! Unsupported field!")

    all_users_tasks[task_index].title = data[0]
    all_users_tasks[task_index].start = check_date(None, None, str(data[1]))
    all_users_tasks[task_index].end = check_date(None, None, str(data[2]))
    all_users_tasks[task_index].description = data[3]
    DataStorage.resave_all_tasks_to_json(all_users_tasks)


@logging_utils.logger
def show_tracked_task():
    tracked_tasks = DataStorage.load_tasks_from_json()[0]
    all_tasks = DataStorage.load_tasks_from_json()[1]
    if tracked_tasks is None:
        raise TypeError("Task collection is not list")
    for task in tracked_tasks:
        subtasks = []
        for subtask in all_tasks:
            if subtask.parent == task.tid:
                subtasks.append(subtask.tid)

        if task.is_completed:
            marker = "X"
        else:
            marker = " "
        yield (marker, str(tracked_tasks.index(task)+1),str(len(subtasks)), str(task.title))


@logging_utils.logger
def done_task(task):
    tracked_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
    for subtask in all_tasks:
        if subtask.parent == tracked_tasks[task-1].tid and subtask.is_completed == False:
            raise Exception("You have undone subtasks! Done them all before you finish this one!")
    global_index = all_users_tasks.index(tracked_tasks[task-1])
    all_users_tasks[global_index].complete()
    DataStorage.resave_all_tasks_to_json(all_users_tasks)


@logging_utils.logger
def done_subtask(task_index, subtask_index):
    tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
    tid_subtasks = []

    for subtask in all_tasks:
        if subtask.parent == tasks[task_index - 1].tid:
            tid_subtasks.append(subtask)

    global_index = get_task_index(tid_subtasks[subtask_index - 1].tid, all_users_tasks)
    all_users_tasks[global_index].complete()
    DataStorage.resave_all_tasks_to_json(all_users_tasks)


@logging_utils.logger
def get_task(task_index):
    """
    Get task by index
    :param task_index: int object
    :return:
    """
    tasks = DataStorage.load_tasks_from_json()[0]
    task = tasks[task_index-1]
    return task


@logging_utils.logger
def add_sheduler(title=None, description=None, date=None, enddate=None,
                 tag=None, observers=None,
                 reminder=None, priority=None,
                 changed=None, planned=None, executor=None):
    current = UserTools.get_current_user()
    observers = serialization_utils.split_str_to_list(observers, current)
    priority = Priority.convert_priority_to_str(priority)
    author = UserTools.get_current_user().uid

    task = TrackedTask(title, description, date, enddate, tag, author, observers, executor,
                 reminder, priority, changed, planned)

    check_date_range(date, enddate)

    scheduler = Scheduler(date, task)

    DataStorage.save_scheduler_to_json(scheduler)


@logging_utils.logger
def get_schedulers():
    schedulers = DataStorage.load_schedulers_from_json()
    for scheduler in schedulers:
        print(scheduler.date.date())
        print(datetime.now().date())
        if datetime.now().date() >= scheduler.date.date():
            all_tasks = DataStorage.load_tasks_from_json()[2]
            all_tasks.append(scheduler.task)
            DataStorage.resave_all_tasks_to_json(all_tasks, scheduler.task)
            DataStorage.delete_scheduler_from_json(scheduler)





"""
 for subtask in tid_subtasks:
        if subtask.is_completed:
            marker = "X"
        else:
            marker = " "
        click.echo("[" + marker + "] - " + str(tid_subtasks.index(subtask) + 1)
                   + " - " + click.style(subtask.title, bg="red"))
            """



"""

# задаем конфигурацию логгирования
format_info, file_info = loggingConfig.get_logging_config(logging.INFO)
logging.basicConfig(filename=file_info, level=logging.INFO,
                    format=format_info)

format_warning, file_warning = loggingConfig.get_logging_config(logging.WARNING)
logging.basicConfig(filename=file_warning, level=logging.WARNING,
                    format=format_warning)
"""
