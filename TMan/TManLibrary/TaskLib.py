from .UserLib import *


class Task:
    """Базовый класс для задачи списка дел и события календаря"""
    def __init__(self, title, date, description, priority, tid):
        self.title = title
        self.date = date
        self.description = description
        self.priority = priority
        self.tid = tid


class SimpleListTask(Task):
    """Сущность задачи списка дел"""
    def __init__(self, title, date, description, priority, tid, permission, is_completed, tag):
        Task.__init__(self, title, date, description, priority, tid)
        self.is_completed = is_completed
        self.permission = permission
        self.tag = tag

    def __str__(self):
        return self.title

    def complete(self):
        """Функция завершения задачи и перевод в статус DONE"""
        if self.is_completed:
            self.is_completed = False
        else:
            self.is_completed = True


class EventCalendar(Task):
    """Сущность события календаря"""
    def __init__(self, title, date, description, priority, tid, permisson, location, reminder ):
        Task.__init__(self, title, date, description, priority, tid)
        self.permission = permisson
        self.location = location
        self.reminder = reminder

    def __str__(self):
        return self.title

    def set_reminder(self, reminder):
        """Функция установки пользовательского напоминания на событие календря"""
        self.reminder = reminder


class BaseTask:
    """Базовый класс для сущности задачи и подзадачи трекинговой системы"""
    def __init__(self, tid, title, description, start, end, tag, dash, author, observers, executor, cancel_sync, is_completed, reminder, priority):
        self.title = title
        self.tid = tid
        self.description = description
        self.priority = priority
        self.start = start
        self.end = end
        self.author = author
        self.tag = tag
        self.dash = dash
        self.observers = observers
        self.executor = executor
        self.is_completed = is_completed
        self.cancel_sync = cancel_sync
        self.reminder = reminder


class SubTask(BaseTask):
    """Сущность подзадачи"""
    def __init__(self, tid, parent_id, title, description, start, end, tag, dash, author, observers, executor,
                          cancel_sync, is_completed, reminder, priority):
        BaseTask.__init__(self, tid, title, description, start, end, tag, dash, author, observers, executor,
                          cancel_sync, is_completed, reminder, priority)
        self.parent_id = parent_id


class TrackedTask(BaseTask):
    """
    Сузность задачи, которая включает в себя мелкие подзадачи в виде списка
    """
    def __init__(self, tid, title, description, start, end, tag, dash, author, observers, executor, cancel_sync, is_completed, reminder, priority, subtasks):

        BaseTask.__init__(self, tid, title, description, start, end, tag, dash, author, observers, executor,
                          cancel_sync, is_completed, reminder, priority)
        self.subtasks = subtasks

    def add_subtask(self, tid):
        self.subtasks.append(tid)


class User:
    """
    Данный класс описывает сущность пользователя
    Главная цель - хранение информации о доступных пользователю задачах
    При загрузке файла users.json, ищем пользователя с current == True и список, доступных tid (task id)
    Далее выборочно загружаем данные из json файлов задач по tid
    tman user --chuser <login> - вход
    tman user --setuser <login> - создание пользователя
    """
    def __init__(self, name, surname, uid, tasks, login, current):
        self.name = name
        self.surname = surname
        self.uid = uid
        self.current = current
        self.login = login
        # tasks - это список, хранящий tid для task, списка, event, доступных пользователю
        self.tasks = tasks

    def set_current(self):
        """
        Сделать данного пользователя текущим
        """
        self.current = True
    def add_simpletasks(self, tid):
        self.tasks['simple'].append(tid)

    def add_task(self, tid):
        self.tasks['task'].append(tid)

