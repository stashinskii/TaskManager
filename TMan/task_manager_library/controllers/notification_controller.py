"""
This module represents controller for manging notificatons
"""

from task_manager_library.data_storage import DataStorage
from task_manager_library.models.notifications_model import Notifications
from utility import utils
from datetime import datetime, time


class NotificationController:
    @staticmethod
    def add(date, tid, title):
        task = DataStorage.get_task_from_id(tid)

        notification = Notifications(task.tid, task.reminder, date, title)
        DataStorage.add_notification(notification)

    @staticmethod
    def get():
        notifications = DataStorage.load_notifications_from_json()
        notifications_list = list()
        for notification in notifications:
            if notification.date.date() == datetime.now().date() and datetime.now().time() >= notification.reminder.time():
                notifications_list.append(notification)
                DataStorage.delete_notification(notification.rid)
        if len(notifications_list) == 0:
            raise ValueError("There is no notifications!")
        return notifications_list