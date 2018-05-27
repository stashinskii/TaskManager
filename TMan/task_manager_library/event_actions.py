import uuid
from datetime import timedelta, date, datetime

from .task_info import *


class EventActions:
    """
    Класс предназначен для синхронизации задач, подзадач, TO DO и календаря,
    а также обмена с другими пользователями
    """
    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)



    @staticmethod
    def to_event(tracked_tasks):
        """
        Преобразование задач к календарю, для последующей работы с планировщиком
        """
        events = []
        for task in tracked_tasks:
            for single_date in EventActions.daterange(task.start, task.end + + timedelta(1)):
                events.append(
                    EventCalendar(task.title, single_date, task.description, task.priority, uuid.uuid1(), task.planned))
        return events


