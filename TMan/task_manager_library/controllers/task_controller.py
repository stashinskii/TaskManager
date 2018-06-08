"""
This module represents controller of tasks which is managing actions of them and give full access to
user and his CLI for adding, editing, deleting, sharing, viewing, etc.
"""

from task_manager_library.data_storage import DataStorage
from task_manager_library.models.task_model import Status


class TaskController:
    """Manager/controller of tasks. Requests sends from actions"""
    @staticmethod
    def add(task):
        return DataStorage.add_task_to_json(task)

    @staticmethod
    def get_connected_tasks(tid):
        """Get connected task of chosen task"""
        return DataStorage.get_task_from_id(tid)

    @staticmethod
    def edit(task_num, task_field):
        """Editing task by its index and fieldname(title, start date, etc.)"""
        DataStorage.edit_task(task_num, task_field)

    @staticmethod
    def delete(tid):
        """Deleting task by its task ID"""
        DataStorage.delete_task(tid)

    @staticmethod
    def archieve():
        """Get done tasks"""
        tasks = DataStorage.load_tasks_from_json()[1]
        archieved_tasks = list()
        for task in tasks:
            if task.is_completed == Status.done:
                archieved_tasks.append(task)

        return archieved_tasks

    @staticmethod
    def get_by_index(task_index):
        """Get task by its index"""
        tasks = DataStorage.load_tasks_from_json()[0]
        task = tasks[task_index - 1]
        return task

    @staticmethod
    def make_link(task1, task2):
        """Make connection between 2 tasks. Parameters are tid (str object)"""
        return DataStorage.make_link(task1, task2)

    @staticmethod
    def order_by(tag):
        """Order tasks (tasks+subtasks) by its tag"""
        return DataStorage.show_ordered_tasks(tag)

    @staticmethod
    def complete_task(task):
        """Complete chosen task"""
        DataStorage.done_task(task)

    @staticmethod
    def uncomplete_task(task):
        """Uncomplete chosen task"""
        DataStorage.undone_task(task)

    @staticmethod
    def begin_task(task):
        """Begin chosen task"""
        DataStorage.begin_task(task)

    @staticmethod
    def complete_subtask(task_index, subtask_index):
        DataStorage.done_subtask(task_index, subtask_index)

    @staticmethod
    def uncomplete_subtask(task_index, subtask_index):
        DataStorage.undone_subtask(task_index, subtask_index)

    @staticmethod
    def edit_subtask(task_num, subtask_num, task_field):
        DataStorage.edit_subtask(task_num, subtask_num, task_field)

    @staticmethod
    def begin_subtask(task_index, subtask_index):
        DataStorage.begin_subtask(task_index, subtask_index)

    @staticmethod
    def get_users_tasks():
        """Get list of tasks of current user with other information (Amount of subtasks, index, etc.)"""
        tracked_tasks = DataStorage.load_tasks_from_json()[0]
        all_tasks = DataStorage.load_tasks_from_json()[1]
        if tracked_tasks is None:
            raise TypeError("Task collection is not list")
        for task in tracked_tasks:
            subtasks = []
            for subtask in all_tasks:
                if subtask.parent == task.tid:
                    subtasks.append(subtask.tid)

            yield task.is_completed, tracked_tasks.index(task) + 1, len(subtasks), task.title

    @staticmethod
    def get_users_subtasks(index):
        """Get list of subtasks of chosen task"""
        subtasks = DataStorage.get_subtasks(index)
        if subtasks is None:
            raise TypeError("Task collection is not list")
        for task in subtasks:
            yield task.is_completed, subtasks.index(task) + 1, task.title

    @staticmethod
    def get_subtask(task_index, subtask_index):
        """Get subtask of chosen task"""
        subtasks = DataStorage.get_subtasks(task_index)
        return subtasks[subtask_index-1]

