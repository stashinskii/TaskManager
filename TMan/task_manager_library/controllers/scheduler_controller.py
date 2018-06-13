"""
This module represents controller of scheduler which were created for managing planned tasks by
given interval and give full access to schedulers to Command Line Interface

"""

import copy
from datetime import datetime, timedelta

from task_manager_library.scheduler_storage import SchedulerStorage


class SchedulerController():
    """Scheduler for creating planned tasks"""
    def __init__(self, scheduler_storage, task_storage):
        #TODO передать taskstorage
        self.storage = scheduler_storage
        self.task_storage = task_storage

    def add(self, scheduler):
        """Adding new scheduler"""
        self.storage.add_scheduler(scheduler)

    def get(self):
        self.storage.load_user_schedulers()
        return self.storage.user_schedulers

    def generate_task(self, scheduler):

        if (scheduler.last + timedelta(scheduler.interval)) < datetime.now():
            self.task_storage.add_task(scheduler.task)
            scheduler.last = datetime.now()
            self.storage.update(scheduler.sid)



