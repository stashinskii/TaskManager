"""
This module represents model of notifications
"""
from task_manager_library.utility import serialization_utils
from datetime import datetime


class Notifications:
    """Notifications class represents full information of notification"""
    def __init__(self, task_id=None, reminder=None, date=None, title=None, rid=None):
        if date is not None:
            self.date = date
        else:
            self.date = datetime.now()
        if title is not None:
            self.title = title
        else:
            self.title = "Unknown Reminder"
        if task_id is not None:
            self.task_id = task_id
        else:
            raise ValueError("Empty task while creating new notification!")
        if reminder is not None:
            self.reminder = reminder
        else:
            self.reminder = "12:00"  # Default value
        if rid is not None:
            self.rid = rid
        else:
            self.rid = serialization_utils.tid_gen()
