"""
This module represents controller of scheduler which were created for managing planned tasks by
given interval and give full access to schedulers to Command Line Interface

"""

import copy
from datetime import datetime, timedelta

from task_manager_library.storage.scheduler_storage import SchedulerStorage
from task_manager_library.controllers.base_controller import BaseController


class SchedulerController(BaseController):
    """Scheduler for creating planned tasks"""
    def __init__(self, scheduler_storage, task_storage):
        super(SchedulerController, self).__init__(task_storage=task_storage)
        self.scheduler_storage = scheduler_storage


    def add(self, scheduler):
        """Adding new scheduler"""
        self.scheduler_storage.add_scheduler(scheduler)

    def get(self):
        self.scheduler_storage.load_user_schedulers()
        return self.scheduler_storage.user_schedulers

    def generate_task(self, scheduler):

        if (scheduler.last + timedelta(scheduler.interval)) < datetime.now():
            self.task_storage.add_task(scheduler.task)
            scheduler.last = datetime.now()
            self.scheduler_storage.update(scheduler.sid)



