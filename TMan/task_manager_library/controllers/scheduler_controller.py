"""
This module represents controller of scheduler which were created for managing planned tasks by
given interval and give full access to schedulers to Command Line Interface
"""

import copy
from datetime import datetime, timedelta

from task_manager_library.data_storage import DataStorage


class SchedulerController():
    """Scheduler for creating planned tasks"""

    @staticmethod
    def add(scheduler):
        """Adding new scheduler"""
        DataStorage.save_scheduler_to_json(scheduler)

    @staticmethod
    def get():
        """Get list of schedulers"""
        schedulers = DataStorage.load_schedulers_from_json()
        for scheduler in schedulers:
            if datetime.now().date() > scheduler.last.date() + timedelta(days=scheduler.interval):
                new_task = copy.deepcopy(scheduler.task)
                DataStorage.add_task_to_json(new_task)

                DataStorage.delete_scheduler_from_json(scheduler)
                scheduler.last = datetime.now()
                DataStorage.save_scheduler_to_json(scheduler)
        return schedulers

    @staticmethod
    def delete_scheduler(scheduler):
        DataStorage.delete_scheduler_from_json(scheduler)
