"""
This module represents controller of scheduler which is managing planned tasks by
given interval and give full access of schedulers to View

"""

import copy
from datetime import datetime, timedelta

from task_manager_library.storage.scheduler_storage import SchedulerStorage
from task_manager_library.controllers.base_controller import BaseController


class SchedulerController(BaseController):
    """
    SchedulerController is used to control actions connected to scheduler.
    It contains methods for adding new scheduler, get list of schedulers,
    generating new task according to scheduler's pattern of task
    """
    def __init__(self, scheduler_storage, task_storage):
        super(SchedulerController, self).__init__(task_storage=task_storage)
        self.scheduler_storage = scheduler_storage

    def add(self, scheduler):
        """
        Creates new scheduler
        :param scheduler: Scheduler's object
        :return:
        """
        self.scheduler_storage.add_scheduler(scheduler)

    def get(self):
        """
        Get user's schedulers
        :return: list of Scheduler's objects
        """
        self.scheduler_storage.load_user_schedulers()
        return self.scheduler_storage.user_schedulers

    def generate_task(self, scheduler):
        """
        Generates the task if a specified condition is satisfied
        :param scheduler: Scheduler's object
        :return:
        """

        if (scheduler.last + timedelta(scheduler.interval)) < datetime.now():

            self.task_storage.add_task(scheduler.task)

            scheduler.last = datetime.now()
            self.scheduler_storage.update(scheduler.sid)



