from .UserLib import *
import enum


class Task:
    """Базовый класс для задачи списка дел и события календаря"""
    def __init__(self, title, date, description, priority, tid):
        self.title = title
        self.date = date
        self.description = description
        self.priority = priority
        self.tid = tid


class EventCalendar(Task):
    """Сущность события календаря"""
    def __init__(self, title, date, description, priority, tid, planned):
        Task.__init__(self, title, date, description, priority, tid)
        self.planned = planned

    def __str__(self):
        return self.title


class TrackedTask:
    """Базовый класс для сущности задачи и подзадачи трекинговой системы"""
    def __init__(self, tid, title, description, start, end, tag, author, observers,
                 executor, is_completed, reminder, priority, parent, subtasks, changed, planned):
        self.title = title
        self.tid = tid
        self.description = description
        self.priority = priority
        self.start = start
        self.end = end
        self.author = author
        self.tag = tag
        self.observers = observers
        self.executor = executor
        self.is_completed = is_completed
        self.reminder = reminder
        self.parent = parent
        self.subtasks = subtasks
        self.planned = planned
        self.changed = changed


    def complete(self):
        if self.is_completed:
            self.is_completed = False
        else:
            self.is_completed = True

    def get_time(self):
        """Получить дату и время создания в виде datetime объекта"""
        from .DataLib import uuid_to_datetime, str_to_uuid
        return uuid_to_datetime(str_to_uuid(self.tid))


class Priority(enum.Enum):
    """Перечеслитель важности/приоритета задачи: от 1 к 3 (3 - наивысший)"""
    high = 3
    medium = 2
    low = 1

    @classmethod
    def from_name(cls, name):
        for priority, priority_name in Priority.items():
            if priority_name == name:
                return priority
        raise ValueError('{} is not priority type'.format(name))

    def to_name(self):
        return Priority[self.value]


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
        """Сделать данного пользователя текущим"""
        self.current = True

    def add_simpletasks(self, tid):
        self.tasks['simple'].append(tid)

    def add_task(self, tid):
        self.tasks['task'].append(tid)


class Scheduler():
    def __init__(self, weekday, title, basic_description, sid, last_added):
        self.weekday = weekday
        self.title = title
        self.basic_description = basic_description
        self.sid = sid
        self.last_added = last_added




