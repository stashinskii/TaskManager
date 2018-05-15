from .TaskLib import *
from datetime import timedelta, date, datetime
import uuid

class Sync:
    """
    Класс предназначен для синхронизации задач, подзадач, TO DO и календаря,
    а также обмена с другими пользователями
    """
    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


    @staticmethod
    def to_todo(users, current, simple_tasks, title, tid, description, priority, is_completed, date, tag):
        from .DataLib import add_simple_task

        add_simple_task(users, current, simple_tasks, title, date, description, priority, tid, is_completed, tag)

    @staticmethod
    def to_event(tracked_tasks):
        events = []
        for task in tracked_tasks:
            for single_date in Sync.daterange(task.start, task.end + + timedelta(1)):
                events.append(
                    EventCalendar(task.title, single_date, task.description, task.priority, uuid.uuid1(), task.planned))
        return events

    @staticmethod
    def sync_changes_todo(task, simple_tasks):
        from .DataLib import resave_simple_json
        for todo in simple_tasks:
            if todo.tid == task.tid:
                index = simple_tasks.index(todo)
        if index is None:
            raise Exception("Trouble while sync w/ TODO")
        simple_tasks[index].title = task.title
        simple_tasks[index].date = task.end
        simple_tasks[index].description = task.description
        resave_simple_json(simple_tasks)

