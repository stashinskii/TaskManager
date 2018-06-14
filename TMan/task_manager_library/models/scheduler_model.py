"""
This module represents model of Scheduler which is describes full information of
"""

import uuid


class Scheduler():
    """Description of scheduler"""
    def __init__(self, last, task, interval, uid, sid=None):
        self.last = last
        self.task = task
        self.interval = interval
        self.uid = uid
        if sid is None:
            self.sid = str(uuid.uuid1())
        else:
            self.sid = sid

