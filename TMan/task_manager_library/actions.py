"""
Actions module represents connection between CLI and Controllers of Tasks, Schedulers, etc.

Primarily it prepares data to be used as objects and sends to controllers classes.

It was divided to logical regions for more comfort.
"""


import json
import logging
import os
import uuid
from datetime import datetime

import config
from task_manager_library.models.notifications_model import Notifications
from task_manager_library.controllers.notification_controller import NotificationController
from task_manager_library.controllers.scheduler_controller import SchedulerController
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.models.scheduler_model import Scheduler
from task_manager_library.models.task_model import Task
from utility import console_utils as console
from utility import logging_utils
from utility import serialization_utils
from utility import utils
from utility.utils import *
from .data_storage import *


# region Adding and editing tasks

@logging_utils.logger
def add_tracked_task(title=None, desc=None, start=None, end=None,
                     tag=None, observers=None,
                     reminder=None, priority=None,parent=None,
                     changed=None, planned=None,  executor=None):
    """Adding new task"""
    current = DataStorage.CURRENT_USER
    observers = serialization_utils.split_str_to_list(observers, current)
    if priority is not None:
        priority = Priority[priority].value
    else:
        priority = Priority.low
    if tag is not None:
        tag = Tag(tag)
    else:
        tag = Tag("default")

    author = current.uid
    task = Task(title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent)
    check_date_range(start, end)
    TaskController.add(task)
    return task


@logging_utils.logger
def add_subtask(index, title=None, desc=None, start=None, end=None,
                tag=None, observers=None,
                reminder=None, priority=None,
                changed=None, planned=None, executor=None):

    """Adding new subtask task"""
    current = DataStorage.CURRENT_USER
    observers = serialization_utils.split_str_to_list(observers, current)
    priority = Priority.convert_priority_to_str(priority)
    author = current.uid

    tasks, all, all_users_tasks = DataStorage.load_tasks_from_json()
    parent_id = tasks[index - 1].tid

    task = Task(title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent_id)
    all_users_tasks.append(task)
    global_index = get_task_index(parent_id, all_users_tasks)
    all_users_tasks[global_index].subtasks.append(task.tid)
    check_date_range(start, end)
    TaskController.add(task)


@logging_utils.logger
def edit_task(tid, task_field):
    TaskController.edit(tid, task_field)


@logging_utils.logger
def edit_subtask(task_num, subtask_num, task_field):
    TaskController.edit_subtask(task_num, subtask_num, task_field)


@logging_utils.logger
def delete_task(tid):
    return TaskController.delete(tid)

# endregion

# region Show tasks

@logging_utils.logger
def get_subtasks(tid):
    return TaskController.get_subtasks(tid)


@logging_utils.logger
def show_tasks_list():
    return TaskController.get_users_tasks()

@logging_utils.logger
def get_task_from_id(tid):
    return TaskController.get_task_from_id(tid)


@logging_utils.logger
def show_subtasks_list(index):
    return TaskController.get_users_subtasks(index)

@logging_utils.logger
def order_tasks(tag):
    return TaskController.order_by(tag)

@logging_utils.logger
def order_by_priority(priority):
    return TaskController.order_by_priority(priority)

@logging_utils.logger
def get_task(task_index):
    """
    Get task by index
    :param task_index: int object
    :return:
    """
    task = TaskController.get_by_index(task_index)
    return task

@logging_utils.logger
def get_subtask(task_index, subtask_index):
    """
    Get task by index
    :param task_index: int object
    :return:
    """
    task = TaskController.get_subtask(task_index, subtask_index)
    return task

# endregion

# region Change status of task

@logging_utils.logger
def begin_task(tid):
    TaskController.begin_task(tid)


@logging_utils.logger
def done_task(task):
    TaskController.complete_task(task)


@logging_utils.logger
def undone_task(task):
    TaskController.uncomplete_task(task)

# endregion

# region Change status of subtask

@logging_utils.logger
def done_subtask(task_index, subtask_index):
    TaskController.complete_subtask(task_index, subtask_index)


@logging_utils.logger
def begin_subtask(task_index, subtask_index):
    TaskController.begin_subtask(task_index, subtask_index)


@logging_utils.logger
def undone_subtask(task_index, subtask_index):
    TaskController.uncomplete_subtask(task_index, subtask_index)

# endregion

# region Tools region


@logging_utils.logger
def add_scheduler(title=None, description=None, date=None, enddate=None,
                  tag=None, observers=None,
                  reminder=None, priority=None, interval=None,
                  changed=None, planned=None, executor=None):
    current = DataStorage.CURRENT_USER
    observers = serialization_utils.split_str_to_list(observers, current)
    priority = Priority.convert_priority_to_str(priority)
    author = current.uid
    tag = Tag(tag)
    task = Task(title, description, date, enddate, tag, author, observers, executor,
                reminder, priority, changed, planned)
    check_date_range(date, enddate)
    scheduler = Scheduler(datetime.now(), task, interval)

    SchedulerController.add(scheduler)


@logging_utils.logger
def get_schedulers():
    return SchedulerController.get()


@logging_utils.logger
def get_connected_tasks(tid):
    return TaskController.get_connected_tasks(tid)


@logging_utils.logger
def make_link(task1, task2):
    return TaskController.make_link(task1, task2)

@logging_utils.logger
def show_archieve():
    return TaskController.archieve()

@logging_utils.logger
def add_notification(date, tid, title=None):
    return NotificationController.add(date, tid, title)

@logging_utils.logger
def get_notification():
    return NotificationController.get()

#endregion
