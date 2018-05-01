from .DataLib import *

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
        add_simple_task(users, current, simple_tasks, title, date, description, priority, tid, is_completed, tag)

    @staticmethod
    def to_event():
        pass

