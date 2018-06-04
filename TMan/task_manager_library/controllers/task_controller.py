from task_manager_library.data_storage import DataStorage


class TaskController:
    """Request send from actions"""
    @staticmethod
    def add(task):
        DataStorage.add_task_to_json(task)

    @staticmethod
    def edit():
        DataStorage.edit_task(task_num, field)

    @staticmethod
    def get_by_index(index):
        tasks = DataStorage.load_tasks_from_json()[0]
        task = tasks[task_index - 1]
        return task

    @staticmethod
    def complete_task(task):
        DataStorage.done_task(task)

    @staticmethod
    def uncomplete_task(task):
        DataStorage.undone_task(task)

    @staticmethod
    def begin_task(task):
        DataStorage.begin_task(task)

    @staticmethod
    def complete_subtask(task):
        DataStorage.done_subtask(task)

    @staticmethod
    def uncomplete_subtask(task):
        DataStorage.undone_subtask(task)

    @staticmethod
    def begin_subtask(task):
        DataStorage.begin_subtask(task)

    @staticmethod
    def get_users_tasks():
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
        subtasks = DataStorage.get_subtasks(index)
        if subtasks is None:
            raise TypeError("Task collection is not list")
        for task in subtasks:
            yield task.is_completed, subtasks.index(task) + 1, task.title

