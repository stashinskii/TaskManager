"""
Actions module represents connection between CLI and Controllers of Tasks, Schedulers, etc.

Primarily it prepares data to be used as objects and sends to controllers classes.

It was divided to logical regions for more comfort.

Each call of method add new note to a log file. Each method use decorator to get logger config
"""

from task_manager_library.data_storage import Storage
from task_manager_library.scheduler_storage import SchedulerStorage
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.controllers.scheduler_controller import SchedulerController
from task_manager_library.models.task_model import Task, Priority, Tag, Status
from task_manager_library.models.scheduler_model import Scheduler
from console.user_actions import User
from datetime import datetime


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

        self.task_storage = Storage()
        self.scheduler_storage = SchedulerStorage()
        self.current_user = self.task_storage.load_user(self.task_storage.current_uid)
        self.task_controller = TaskController(self.task_storage)
        self.scheduler_controller = SchedulerController(self.scheduler_storage, self.task_storage)


    # region Users
    def add_new_user(self, login, name, surname):
        """Sign Up in app"""
        user = User(login=login, name=name, surname=surname)
        self.task_storage.save_new_user_to_json(user)

    def change_user(self, uid):
        self.task_storage.change_user_config(uid)

    # endregion

    # region Tasks

    def add_task(self, title, start, end, **kwargs):
        """Adding new task"""
        parent =  kwargs['parent']
        if parent is None:
            height = 0
        else:
            height = self.get_subtask_height(parent) + 1

        task = Task(title=title,
                    author=self.current_user.uid,
                    start=start,
                    end=end,
                    height=height,
                    **kwargs)
        self.task_controller.add(task)

    def edit_task(self,tid, **kwargs):
        """Editing task by its tid"""

        self.task_controller.edit(tid, **kwargs)

    def share_task(self, observer_uid, tid):
        self.task_controller.share(observer_uid, tid)

    def delete_task(self, tid):
        self.task_controller.delete(tid)

    def clear_all(self):
        self.task_controller.clear()

    def get_task_by_tid(self, tid):
        return self.task_controller.get_task(tid)

    def get_subtasks(self, tid):
        return self.task_controller.get_subtasks(tid)

    def get_subtask_height(self, tid):
        return self.task_controller.get_subtask_height(tid)

    def get_tasks_list(self):
        return self.task_controller.get_list()

    def order_by_tag(self, tag_name):
        tag_name = Tag(tag_name)
        return self.task_controller.order_by_tag(tag_name)

    def order_by_priority(self, priority):
        return self.task_controller.order_by_priority(priority)

    def make_link(self, first_id, second_id):
        self.task_controller.make_link(first_id, second_id)

    def complete_task(self, tid):
        self.task_controller.complete_task(tid)

    def begin_task(self, tid):
        self.task_controller.begin_task(tid)

    def uncomplete_task(self, tid):
        self.task_controller.uncomplete_task(tid)

    def get_archieve(self):
        all_tasks = self.task_controller.get_list()
        return [task for task in all_tasks if task.is_completed == Status.done]

    # endregion

    # region Schedulers

    def add_scheduler(self, title, start, end, interval, **kwargs):
        """Adding new planned task by its interval, start"""
        task = Task(title=title,
                    author=self.current_user.uid,
                    start=start,
                    end=end,
                    height=0,
                    **kwargs)
        last = datetime.now()
        scheduler = Scheduler(task=task,
                              last=last,
                              interval=interval,
                              uid=self.current_user.uid)
        self.scheduler_controller.add(scheduler)

    def get_schedulers(self):
        schedulers = self.scheduler_controller.get()
        for scheduler in schedulers:
            self.scheduler_controller.generate_task(scheduler)




    # endregion







