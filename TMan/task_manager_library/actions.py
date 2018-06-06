import json
import logging
import os
import uuid
from datetime import datetime

import config
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
                     reminder=None, priority=None,
                     changed=None, planned=None, executor=None):
    """Adding new task"""
    current = DataStorage.CURRENT_USER
    observers = serialization_utils.split_str_to_list(observers, current)
    priority = Priority[priority].value
    author = current.uid
    task = Task(title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned)
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
def edit_task(task_num, task_field):
    TaskController.edit(task_num, task_field)

# endregion

# region Show tasks

@logging_utils.logger
def show_tasks_list():
    return TaskController.get_users_tasks()



@logging_utils.logger
def show_subtasks_list(index):
    return TaskController.get_users_subtasks(index)

@logging_utils.logger
def order_tasks(tag):
    return TaskController.order_by(tag)

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
def begin_task(task):
    TaskController.begin_task(task)


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

#endregion
