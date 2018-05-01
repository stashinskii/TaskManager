class Sync:
    """
    Класс предназначен для синхронизации задач, подзадач, TO DO и календаря,
    а также обмена с другими пользователями
    Зависимости:
    Задача/подзадача  -> TO DO
    Задача/подзадача  -> Событие календаря
    TO DO             -> Событие календаря
    Событие календаря -> TO DO
    Любые изменения, происходящие с задачей должны быть также синхронизированны
    """
    @staticmethod
    def to_todo(users, current, simple_tasks, title, tid, description, priority, is_completed, date, tag):
        from .DataLib import add_simple_task

        add_simple_task(users, current, simple_tasks, title, date, description, priority, tid, is_completed, tag)

    @staticmethod
    def to_event():
        pass

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
