class Scheduler():
    def __init__(self, date, task, sid=None):
        self.date = date
        # param: task Task's object
        self.task = task
        if sid is None:
            self.sid = serialization_utils.tid_gen()
        else:
            self.sid = sid

