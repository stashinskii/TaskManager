"""
This module represents model of Scheduler which is describes full information of
"""

from task_manager_library.utility import serialization_utils


class Scheduler():
    """Description of scheduler of planned tasks"""
    def __init__(self, last, task, interval, sid=None):
        self.last = last
        self.task = task
        self.interval = interval
        if sid is None:
            self.sid = serialization_utils.tid_gen()
        else:
            self.sid = sid

