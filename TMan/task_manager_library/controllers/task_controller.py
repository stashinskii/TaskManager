"""
This module represents controller of tasks which is managing actions of them and give full access to
user and his CLI for adding, editing, deleting, sharing, viewing, etc.
"""

from task_manager_library.storage.task_storage import Storage
from task_manager_library.models.task_model import Status, Priority, Tag
from task_manager_library.controllers.base_controller import BaseController


class TaskController(BaseController):
    """
    Manager of tasks. Takes requests from CLI with parameters
    and returns exceptions, objects if needed
    """
    def __init__(self, task_storage):
        super(TaskController, self).__init__(task_storage=task_storage)

    def add(self, task):
        """
        Adding new task to storage
        :param task: Task's object
        :return:
        """
        self.task_storage.add_task(task)

    def edit(self, tid, **kwargs):
        """
        Editing task by its tid (task ID)
        :param tid: task ID of chosen task
        :param kwargs: parameters to be changed (title, end date, tag, priority, etc.)
        :return:
        """
        self.task_storage.edit(tid, **kwargs)

    def delete(self, tid):
        """Deletes task by its tid (task ID)"""
        self.task_storage.delete(tid)

    def share(self, observer_uid, tid):
        """
        Share task with other user
        :param observer_uid: user ID (uid) of user to share with
        :param tid: task ID (tid) of task to be shared
        :return:
        """
        self.task_storage.give_task_permission(observer_uid, tid)

    def get_task(self, tid):
        """Get task by its task ID (tid)"""
        self.task_storage.load_user_tasks()
        task = next((task for task in self.task_storage.user_tasks if task.tid == tid), None)
        if task is not None:
            return task
        raise Exception("There is no task with such tid {}".format(tid))

    def get_subtasks(self, tid):
        """Get subtasks of chosen task by its task ID (tid)"""
        self.task_storage.load_user_tasks()
        return [task for task in self.task_storage.user_tasks if task.parent == tid]

    def get_subtask_height(self, tid):
        """Get subtask's height of chosen task by its tid (task ID)"""
        task = self.get_task(tid)
        counter=0
        while task and task.parent is not None:
            counter += 1
            task = self.get_task(task.parent)
            if task.parent is None:
                return counter
        return counter

    def get_list(self):
        """Get full list user's tasks (including subtasks)"""
        self.task_storage.load_user_tasks()
        return self.task_storage.user_tasks

    def order_by_tag(self, tag):
        """Order tasks by tag"""
        self.task_storage.load_user_tasks()
        return [task for task in self.task_storage.user_tasks if task.tag.tag_name == tag.tag_name]

    def order_by_priority(self, priority):
        """Order tasks by priority"""
        self.task_storage.load_user_tasks()
        return [task for task in self.task_storage.user_tasks if task.priority == priority]

    def make_link(self, first_id, second_id):
        """
        Connects two tasks by creating link between them
        :param fisrt_id: describing task ID (tid) of first task
        :param second_id: describing task ID (tid) of second task
        """
        self.task_storage.link(first_id, second_id)

    def complete_task(self, tid):
        """Complete chosen task by its task ID (tid)"""
        self.task_storage.complete_task(tid)

    def uncomplete_task(self, tid):
        """Change status of task to "undone" chosen task by its task ID (tid)"""
        self.task_storage.uncomplete_task(tid)

    def begin_task(self, tid):
        """Begin (chance status to "process") chosen task by its task ID (tid)"""
        self.task_storage.begin_task(tid)




