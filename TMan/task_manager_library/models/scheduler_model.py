"""
This module represents model of Scheduler which is describes full information of
"""

from task_manager_library import date_delta
import uuid


class Scheduler():
    """Description of scheduler of planned tasks"""
    def __init__(self, last, task, interval, uid, sid=None):
        self.last = last
        self.task = task
        self.interval = interval
        self.uid = uid
        if sid is None:
            self.sid = str(uuid.uuid1())
        else:
            self.sid = sid

