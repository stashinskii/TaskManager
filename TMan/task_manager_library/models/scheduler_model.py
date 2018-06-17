"""
This module represents model of Scheduler which is describes full information of
"""

import uuid
from task_manager_library.models.task_model import Task


class Scheduler():
    """Description of scheduler"""
    def __init__(self, last=None, task=None, interval=None, uid=None, sid=None):
        self.last = last
        if task is None:
            self.task = Task()
        else:
            self.task = task
        if interval is None:
            self.interval = 0
        else:
            self.interval = interval
        self.uid = uid
        if sid is None:
            self.sid = str(uuid.uuid1())
        else:
            self.sid = sid

