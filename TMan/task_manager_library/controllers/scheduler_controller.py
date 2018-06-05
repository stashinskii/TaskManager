from task_manager_library.data_storage import DataStorage
from datetime import datetime


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
            if datetime.now().date() >= scheduler.date.date():
                DataStorage.add_task_to_json(scheduler.task)
                DataStorage.delete_scheduler_from_json(scheduler)