"""
Actions module represents connection between CLI and Controllers of Tasks, Schedulers, etc.

Primarily it prepares data to be used as objects and sends to controllers classes.

It was divided to logical regions for more comfort.

Each call of method add new note to a log file. Each method use decorator to get logger config
"""

from task_manager_library.data_storage import Storage
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.models.task_model import Task, Priority, Tag
from console.user_actions import User


class Actions:
    """"
    Actions class represents manager which connects CLI
    and data storage/database. It may work with any interfaces
    such as CLI, web, desktop GUI etc.
    It doesn't contain global state because of using instance methods instead of static
    """

    def __init__(self, logging_config=None):
        # region Configuraion of logger

        # TODO MAKE LOGGER CINFIGURATION HERE

        # endregion

        self.storage = Storage()
        self.current_user = self.storage.load_user(self.storage.current_uid)
        self.task_controller = TaskController(self.storage)
        #self.scheduler_controller = SchedulerController(self.storage)
        #self.notification_controller = NotificationController(self.storage)

    # region Users
    def add_new_user(self, login, name, surname):
        """Sign Up in app"""
        user = User(login=login, name=name, surname=surname)
        self.storage.save_new_user_to_json(user)

    def change_user(self, login):
        pass

    # endregion

    # region Tasks

    def add_task(self, title, start, end, **kwargs):
        """Adding new task"""

        task = Task(title=title, author=self.current_user.uid, start=start, end=end, **kwargs)
        self.task_controller.add(task)

    def edit_task(self,tid, **kwargs):
        """Editing task by its tid"""

        self.task_controller.edit(tid, **kwargs)

    def delete_task(self, tid):
        self.task_controller.delete(tid)

    def clear_all(self):
        self.task_controller.clear()

    def get_task_by_tid(self, tid):
        return self.task_controller.get_task(tid)

    def get_tasks_list(self):
        return self.task_controller.get_list()

    def order_by_tag(self, tag_name):
        tag_name = Tag(tag_name)
        return self.task_controller.order_by_tag(tag_name)

    def make_link(self, first_id, second_id):
        self.task_controller.make_link(first_id, second_id)

    def complete_task(self, tid):
        self.task_controller.complete_task(tid)

    def begin_task(self, tid):
        self.task_controller.begin_task(tid)

    def uncomplete_task(self, tid):
        self.task_controller.uncomplete_task(tid)

    # endregion

    # region Schedulers

    def add_scheduler(self, task, last, interval):
        """Adding new planned task by its interval, start"""
        scheduler = Scheduler(task=task, last=last, interval=interval)
        self.scheduler_controller.add(scheduler)

    def delete_scheduler(self, sid):
        self.scheduler_controller.delete(sid=sid)

    def get_schedulers_list(self):
        self.scheduler_controller.get_list()

    # endregion

    # region Notifications

    def add_notification(self, tid, date):
        notification = Notifications(tid=tid, date=date)
        self.notification_controller.add(notification)

    def get_notifications_list(self):
        self.notification_controller.get_list()

    # endregion








