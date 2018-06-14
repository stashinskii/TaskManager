"""
Actions module represents connection between CLI and Controllers of Tasks, Schedulers, etc in Library.
Primarily it prepares data to be used as objects and sends to controllers classes.
Each call of method add new note to a log file. Each method use decorator to get logger config
"""

import os
from task_manager_library.storage.task_storage import Storage
from task_manager_library.storage.scheduler_storage import SchedulerStorage
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.controllers.scheduler_controller import SchedulerController
from task_manager_library.models.task_model import Task, Priority, Tag, Status
from task_manager_library.models.scheduler_model import Scheduler
from task_manager_library.utility import logger
from console.log_config import LOG_CONFIG
from datetime import datetime


class Actions:
    """"
    Actions class represents manager which connects CLI
    and task manager library
    """

    def __init__(self, log_config=None):
        # region Configuraion of logger

        log_config = log_config if log_config is not None else LOG_CONFIG
        log_path = (log_config['log_path'] if log_config.get('log_path', None) is not None else os.path.dirname(
            __file__) + '/actions.log')

        logger.init_logging(log_config['level'], log_path, log_config['format'])

        # endregion

        self.task_storage = Storage()
        self.scheduler_storage = SchedulerStorage()
        self.current_user = self.task_storage.load_user(self.task_storage.current_uid)
        self.task_controller = TaskController(self.task_storage)
        self.scheduler_controller = SchedulerController(self.scheduler_storage, self.task_storage)


    # region Users
    @logger.log_func(__name__)
    def add_new_user(self, login, name, surname):
        """Created new User's object and save it to storage"""
        user = User(login=login, name=name, surname=surname)
        self.task_storage.save_new_user_to_json(user)

    def change_user(self, login):
        """Change current user. Resave user ID to configuration file"""
        self.task_storage.change_user_config(login)

    # endregion

    # region Tasks
    @logger.log_func(__name__)
    def add_task(self, title, start, end, **kwargs):
        """
        Method for creating new task and save it to storage
        :param title: title of task
        :param start: datetime object describing start of task
        :param end: datetime object describing end of task
        :param kwargs: other parameters describing task
        :return:
        """
        parent =  kwargs['parent']
        if parent is None:
            height = 0
        else:
            height = self.get_subtask_height(parent) + 1

        task = Task(title=title,
                    author=self.current_user.uid,
                    start=start,
                    end=end,
                    height=height,
                    **kwargs)
        self.task_controller.add(task)

    @logger.log_func(__name__)
    def edit_task(self,tid, **kwargs):
        """
        Editing of task by its task ID (tid)
        :param tid: task ID of chosen task
        :param kwargs: parameters to be changed (title, end date, tag, priority, etc.)
        :return:
        """
        self.task_controller.edit(tid, **kwargs)

    @logger.log_func(__name__)
    def share_task(self, observer_uid, tid):
        """
        Share task with other user
        :param observer_uid: user ID (uid) of user to share with
        :param tid: task ID (tid) of task to be shared
        :return:
        """
        self.task_controller.share(observer_uid, tid)

    @logger.log_func(__name__)
    def delete_task(self, tid):
        """Delete task by its task ID (tid)"""
        self.task_controller.delete(tid)

    @logger.log_func(__name__)
    def get_task_by_tid(self, tid):
        """Get task by its task ID (tid)"""
        return self.task_controller.get_task(tid)

    @logger.log_func(__name__)
    def get_subtasks(self, tid):
        """Get subtasks of chosen task by its tid (task ID)"""
        return self.task_controller.get_subtasks(tid)

    @logger.log_func(__name__)
    def get_subtask_height(self, tid):
        """Get height of chosen task by its tid (task ID)"""
        return self.task_controller.get_subtask_height(tid)

    @logger.log_func(__name__)
    def get_tasks_list(self):
        """Get list of user's tasks"""
        return self.task_controller.get_list()

    @logger.log_func(__name__)
    def order_by_tag(self, tag_name):
        """
        Order tasks by their tag
        :param tag_name: string describing tag's title
        :return:
        """
        tag_name = Tag(tag_name)
        return self.task_controller.order_by_tag(tag_name)

    @logger.log_func(__name__)
    def order_by_priority(self, priority):
        """Order tasks by their priority"""
        return self.task_controller.order_by_priority(priority)

    @logger.log_func(__name__)
    def make_link(self, first_id, second_id):
        """
        Connects two tasks by creating link between them
        :param fisrt_id: describing task ID (tid) of first task
        :param second_id: describing task ID (tid) of second task
        """
        self.task_controller.make_link(first_id, second_id)

    @logger.log_func(__name__)
    def complete_task(self, tid):
        """Complete chosen task by its task ID (tid)"""
        self.task_controller.complete_task(tid)

    @logger.log_func(__name__)
    def begin_task(self, tid):
        """Begin (chance status to "process") chosen task by its task ID (tid)"""
        self.task_controller.begin_task(tid)

    @logger.log_func(__name__)
    def uncomplete_task(self, tid):
        """Change status of task to "undone" chosen task by its task ID (tid)"""
        self.task_controller.uncomplete_task(tid)

    @logger.log_func(__name__)
    def get_archieve(self):
        """Get tasks with "done" status"""
        all_tasks = self.task_controller.get_list()
        return [task for task in all_tasks if task.is_completed == Status.done]

    # endregion

    # region Schedulers
    @logger.log_func(__name__)
    def add_scheduler(self, title, start, end, interval, **kwargs):
        """
        Adding new planned task
        Created pattern of task and then creates Scheduler's object
        :param title: title of planned task
        :param start: datetime object describing start of task
        :param end: datetime object describing end of task
        :param interval: interval between creation of task
        :param kwargs: other parameters describing task pattern
        :return:
        """
        task = Task(title=title,
                    author=self.current_user.uid,
                    start=start,
                    end=end,
                    height=0,
                    **kwargs)
        last = datetime.now()
        scheduler = Scheduler(task=task,
                              last=last,
                              interval=interval,
                              uid=self.current_user.uid)
        self.scheduler_controller.add(scheduler)

    @logger.log_func(__name__)
    def get_schedulers(self):
        """
        Get schedulers and creates new task if it needed
        :return:
        """
        schedulers = self.scheduler_controller.get()
        for scheduler in schedulers:
            self.scheduler_controller.generate_task(scheduler)

    # endregion







