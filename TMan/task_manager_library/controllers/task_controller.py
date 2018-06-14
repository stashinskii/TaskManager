"""
This module represents controller of tasks which is managing actions of them and give full access to
user and his CLI for adding, editing, deleting, sharing, viewing, etc.
"""

from task_manager_library.storage.task_storage import Storage
from task_manager_library.models.task_model import Status, Priority, Tag
from task_manager_library.controllers.base_controller import BaseController


class TaskController(BaseController):
    """Manager/controller of tasks. Requests sends from actions"""
    def __init__(self, task_storage):
        super(TaskController, self).__init__(task_storage=task_storage)

    def add(self, task):
        self.task_storage.add_task(task)

    def edit(self, tid, **kwargs):
        self.task_storage.edit(tid, **kwargs)

    def delete(self, tid):
        self.task_storage.delete(tid)

    def clear(self):
        tasks = self.task_storage.load_tasks_from_json()
        for task in tasks:
            self.delete(task.tid)

    def share(self, observer_uid, tid):
        self.task_storage.give_task_permission(observer_uid, tid)

    def get_task(self, tid):
        self.task_storage.load_user_tasks()
        task = next((task for task in self.task_storage.user_tasks if task.tid == tid), None)
        if task is not None:
            return task
        raise Exception("There is no task with such tid {}".format(tid))

    def get_subtasks(self, tid):
        self.task_storage.load_user_tasks()

        return [task for task in self.task_storage.user_tasks if task.parent == tid]

    def get_subtask_height(self, tid):
        task = self.get_task(tid)
        counter=0
        while task and task.parent is not None:
            counter += 1
            task = self.get_task(task.parent)
            if task.parent is None:
                return counter
        return counter

    def get_list(self):
        self.task_storage.load_user_tasks()
        return self.task_storage.user_tasks

    def order_by_tag(self, tag):
        self.task_storage.load_user_tasks()
        return [task for task in self.task_storage.user_tasks if task.tag.tag_name == tag.tag_name]

    def order_by_priority(self, priority):
        self.task_storage.load_user_tasks()
        return [task for task in self.task_storage.user_tasks if task.priority == priority]

    def make_link(self, first_id, second_id):
        self.task_storage.link(first_id, second_id)

    def complete_task(self, tid):
        self.task_storage.complete_task(tid)

    def uncomplete_task(self, tid):
        self.task_storage.uncomplete_task(tid)

    def begin_task(self, tid):
        self.task_storage.begin_task(tid)




