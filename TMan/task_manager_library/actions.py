"""
Actions module represents connection between CLI and Controllers of Tasks, Schedulers, etc.

Primarily it prepares data to be used as objects and sends to controllers classes.

It was divided to logical regions for more comfort.

Each call of method add new note to a log file. Each method use decorator to get logger config
"""

class Actions:
    """"
    Actions class represents manager which connects CLI
    and data storage/database. It may work with any interfaces
    such as CLI, web, desktop GUI etc.
    It doesn't contain global state because of using instance methods instead of static
    """

    def __init__(self, logging_config=None):
        # region config of logger

        # TODO MAKE LOGGER CINFIGURATION HERE

        # endregion

        self.storage = Storage()
        self.current_user = self.storage.get_current_user()
        self.task_controller = TaskController(storage)
        self.scheduler_controller = SchedulerController(storage)
        self.notification_controller = NotificationController(storage)

    # region Users
    def add_new_user(self, login, name, surname):
        """Sign Up in app"""
        user = User(login=login, name=name, surname=surname)
        self.storage.save_new_user_to_json(user)

    def change_user(self, login):
        pass

    # endregion

    # region Tasks

    def add_task(self, title, start, end, **kwargs):
        """Adding new task"""
        task = Task(title=title, author=self.current_user.uid, start=start, end=end, **kwargs)
        self.task_controller.add(task)

    def edit_task(self,tid,**kwargs):
        """
        Editing task by its tid
        :param: tid: str object, contains tid of task
        :param kwargs: kwargs contains field to be edit
        """

        self.task_controller.edit(tid=tid, **kwargs)

    def delete_task(self, tid):
        self.task_controller.delete(tid=tid)

    def clear_all(self):
        self.task_controller.clear()

    def get_task_by_tid(self, tid):
        return self.task_controller.get_task(tid)

    def get_tasks_list(self):
        return self.task_controller.get_list()

    def order_by_tag(self, tag_name):
        tag_name = Tag(tag_name)
        return self.task_controller.order_by_tag(tag_name)

    def make_link(self, first_id, second_id):
        self.task_controller.make_link(first_id, second_id)

    def complete_task(self, tid):
        self.task_controller.complete_task(tid)

    def begin_task(self, tid):
        self.task_controller.begin_task(tid)

    def uncomplete_task(self, tid):
        self.task_controller.uncomplete_task(tid)

    # endregion

    # region Schedulers

    def add_scheduler(self, task, last, interval):
        """Adding new planned task by its interval, start"""
        scheduler = Scheduler(task=task, last=last, interval=interval)
        self.scheduler_controller.add(scheduler)

    def delete_scheduler(self, sid):
        self.scheduler_controller.delete(sid=sid)

    def get_schedulers_list(self):
        self.scheduler_controller.get_list()

    # endregion

    # region Notifications

    def add_notification(self, tid, date):
        notification = Notifications(tid=tid, date=date)
        self.notification_controller.add(notification)

    def get_notifications_list(self):
        self.notification_controller.get_list()

    # endregion




# region DELETE REGION
import json
import logging
import os
import uuid
from datetime import datetime

import config
from task_manager_library.controllers.notification_controller import NotificationController
from task_manager_library.controllers.scheduler_controller import SchedulerController
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.models.notifications_model import Notifications
from task_manager_library.models.scheduler_model import Scheduler
from task_manager_library.models.task_model import Task
from console.user_actions import UserTools
from task_manager_library.utility import console_utils as console, utils, logging_utils, serialization_utils
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
    if desc is None:
        desc = ""

    author = current.uid
    task = Task(title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent)
    utils.check_date_range(start, end)
    TaskController.add(task)
    return task


@logging_utils.logger
def edit_task(tid, task_field):
    """Method for editing by field"""
    TaskController.edit(tid, task_field)


@logging_utils.logger
def share_task(observers, tid):
    """Method for sharing tasks between users"""
    current = UserTools.get_current_user()
    observers = serialization_utils.split_str_to_list(observers, current)
    TaskController.share(observers,tid)


@logging_utils.logger
def delete_task(tid):
    """Method for deleting tasks by its id"""
    return TaskController.delete(tid)

# endregion

# region Show tasks

@logging_utils.logger
def get_subtasks(tid):
    """Get subtasks by their tid"""
    return TaskController.get_subtasks(tid)


@logging_utils.logger
def show_tasks_list():
    """Get tasks of current user"""
    return TaskController.get_users_tasks()

@logging_utils.logger
def get_task_from_id(tid):
    """Get tasks from its id"""
    return TaskController.get_task_from_id(tid)


@logging_utils.logger
def show_subtasks_list(index):
    """Get subtask of task by its (tasks) index"""
    return TaskController.get_users_subtasks(index)

@logging_utils.logger
def order_tasks(tag):
    """Order tasks by tag"""
    return TaskController.order_by_tag(tag)

@logging_utils.logger
def order_by_priority(priority):
    """Order tasks by priority"""
    return TaskController.order_by_priority(priority)

@logging_utils.logger
def get_task(task_index):
    """Get task by index"""
    task = TaskController.get_by_index(task_index)
    return task

@logging_utils.logger
def get_subtask(task_index, subtask_index):
    """Get task by index"""
    task = TaskController.get_subtask(task_index, subtask_index)
    return task

# endregion

# region Change status of task

@logging_utils.logger
def begin_task(tid):
    """Begin task"""
    TaskController.begin_task(tid)


@logging_utils.logger
def done_task(task):
    """Done task"""
    TaskController.complete_task(task)


@logging_utils.logger
def undone_task(task):
    """Complete task"""
    TaskController.uncomplete_task(task)

# endregion


# region Tools region


@logging_utils.logger
def add_scheduler(title=None, description=None, date=None, enddate=None,
                  tag=None, observers=None,
                  reminder=None, priority=None, interval=None,
                  changed=None, planned=None, executor=None):
    """Add scheduler by its interval, task, etc."""
    current = DataStorage.CURRENT_USER
    observers = serialization_utils.split_str_to_list(observers, current)
    priority = Priority.convert_priority_to_str(priority)
    author = current.uid
    tag = Tag(tag)
    task = Task(title, description, date, enddate, tag, author, observers, executor,
                reminder, priority, changed, planned)
    utils.check_date_range(date, enddate)
    scheduler = Scheduler(datetime.now(), task, interval)

    SchedulerController.add(scheduler)


@logging_utils.logger
def get_schedulers():
    """Get schedulers"""
    return SchedulerController.get()


@logging_utils.logger
def get_connected_tasks(tid):
    """Get connected tasks"""
    return TaskController.get_connected_tasks(tid)


@logging_utils.logger
def make_link(task1, task2):
    """Link 2 tasks together"""
    return TaskController.make_link(task1, task2)

@logging_utils.logger
def show_archieve():
    """Get completed tasks"""
    return TaskController.archieve()

@logging_utils.logger
def add_notification(date, tid, title=None):
    """Adding new reminder"""
    return NotificationController.add(date, tid, title)

@logging_utils.logger
def get_notification():
    """Get all reminders"""
    return NotificationController.get()

#endregion

# endregion
