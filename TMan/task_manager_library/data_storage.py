import json
import os

from .task_info import *

from utility import utils
from utility import serialization_utils
from utility import logging_utils

from datetime import datetime



class DataStorage:
    PATH = None
    @staticmethod
    def load_tasks_from_json():
        """
        Loading (deserializing) tasks's data from json files
        :param current: User object - current user (authorized)
        :return: tuple of collections(lists)
        """

        users = DataStorage.load_users_from_json()
        current = utils.get_active_user(users)

        with open(DataStorage.PATH + '/trackedtasks.json', 'r') as task_file:
            task_data = json.load(task_file)
        tasks = list()
        all_tasks = list()
        all_users_tasks = list()
        for task_dict in task_data:
            title = task_dict['title']
            start = utils.check_date(None, None, task_dict['start'])
            end = utils.check_date(None, None, task_dict['end'])
            desc = task_dict['description']
            tag = task_dict['tag']
            observers = task_dict['observers']
            executor = task_dict['executor']
            priority = Priority[Priority(int(task_dict['priority'])).name]
            author = task_dict['author']
            reminder = utils.check_time(None, None, task_dict['reminder'])
            is_completed = task_dict['is_completed']
            parent = task_dict['parent']
            tid = task_dict['tid']
            subtasks = task_dict['subtasks']
            planned = task_dict['planned']
            changed = task_dict['changed']

            new_task = TrackedTask(
                title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent, tid, subtasks, is_completed
            )
            if task_dict['parent'] is None:
                if task_dict['tid'] in current.tasks:
                    tasks.append(new_task)
                    all_tasks.append(new_task)
                all_users_tasks.append(new_task)
            else:
                all_tasks.append(new_task)
                all_users_tasks.append(new_task)
        return tasks, all_tasks, all_users_tasks


    @staticmethod
    def resave_all_tasks_to_json(all_tasks, task=None):
        data = list()
        if task is not None:
            users = DataStorage.load_users_from_json()
            current = utils.get_active_user(users)
            DataStorage.add_user_task(current, task.tid)
        for task in all_tasks:
            if isinstance(task.start, datetime):
                task.start = serialization_utils.date_to_str(task.start)
            if isinstance(task.end, datetime):
                task.end = serialization_utils.date_to_str(task.end)
            if isinstance(task.reminder, datetime):
                task.reminder = serialization_utils.time_to_str(task.reminder)
            if isinstance(task.priority, Priority):
                task.priority = str(task.priority.value)
            data.append(task.__dict__)
        with open(DataStorage.PATH + '/trackedtasks.json', 'w') as taskfile:
            json.dump(data, taskfile, indent=2, ensure_ascii=False)

    @staticmethod
    def load_users_from_json():
        """
        Loading(deserializing) users's data from json file
        :return: list of User's objects
        """
        with open(DataStorage.PATH + '/users.json', 'r') as file:
            data = json.load(file)
        users = list()
        for data_dict in data:
            name = data_dict['name']
            surname = data_dict['surname']
            login = data_dict['login']
            uid = data_dict['uid']
            tasks = data_dict['tasks']
            current = data_dict['current']
            user = User(name, surname, uid, login, current, tasks)
            users.append(user)
        return users

    @staticmethod
    def save_tasks_to_json(task_object):
        """
        Save data to json - Serialization
        :param task_object: Task's object
        """
        try:
            with open(data_dir + '/trackedtasks.json', 'r') as objfile:
                collection = json.load(objfile)

        except FileNotFoundError:
            collection = []
            logging.warning("Can't load json file")
        collection.append(task_object)

        with open(DataStorage.PATH + '/trackedtasks.json', 'w') as objfile:
            json.dump(collection, objfile, indent=2, ensure_ascii=False)

    @staticmethod
    def save_users_to_json(user_object):
        """
        Save new user to json file
        :param user_object: User's object
        :return:
        """
        try:
            with open(data_dir + '/users.json', 'r') as objfile:
                collection = json.load(objfile)

        except FileNotFoundError:
            collection = []
            logging.warning("Can't load json file")
        collection.append(user_object)

        with open(DataStorage.PATH + '/users.json', 'w') as objfile:
            json.dump(collection, objfile, indent=2, ensure_ascii=False)

    @staticmethod
    def add_user_task(user, tid):
        """
        Add task tid to user at users json file
        :param user: User's object
        :param tid: str object
        :return:
        """
        users = DataStorage.load_users_from_json()
        users.__delitem__(utils.get_user_index(user, users))
        user.tasks.append(tid)
        users.append(user)

        data = []
        for user in users:
            data.append(user.__dict__)

        with open(DataStorage.PATH + '/users.json', 'w') as userfile:
            json.dump(data, userfile, indent=2, ensure_ascii=False)

    @staticmethod
    def resave_users_json(users):
        data = []
        for user in users:
            data.append(user.__dict__)

        with open(DataStorage.PATH + '/users.json', 'w') as usersfile:
            json.dump(data, usersfile, indent=2, ensure_ascii=False)

    @staticmethod
    def give_task_permission(observers, tid):
        """
        Give permission to observers
        :param observers: list on User's objects
        :param tid: str object
        :return:
        """
        users = DataStorage.load_users_from_json()
        current = get_active_user(users)
        for us in observers:
            if us != current.login:
                user = get_user(us, users)
                DataStorage.add_user_task(user, tid)

    @staticmethod
    def load_schedulers_from_json():
        schedulers = DataStorage.load_schedulers_dict_from_json()
        schedulers_list = list()

        for scheduler in schedulers:
            date = utils.check_date(None, None, scheduler['date'])
            title = scheduler['task']['title']
            start = utils.check_date(None, None, scheduler['task']['start'])
            end = utils.check_date(None, None, scheduler['task']['end'])
            desc = scheduler['task']['description']
            tag = scheduler['task']['tag']
            observers = scheduler['task']['observers']
            executor = scheduler['task']['executor']
            priority = Priority[Priority(int(scheduler['task']['priority'])).name]
            author = scheduler['task']['author']
            reminder = utils.check_time(None, None, scheduler['task']['reminder'])
            is_completed = scheduler['task']['is_completed']
            parent = scheduler['task']['parent']
            tid = scheduler['task']['tid']
            subtasks = scheduler['task']['subtasks']
            planned = scheduler['task']['planned']
            changed = scheduler['task']['changed']
            sid = scheduler['sid']
            new_task = TrackedTask(
                title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent, tid, subtasks, is_completed
            )
            new_scheduler = Scheduler(date, new_task, sid)
            schedulers_list.append(new_scheduler)
        return schedulers_list




        return schedulers

    @staticmethod
    def load_schedulers_dict_from_json():
        with open(DataStorage.PATH + '/schedulers.json', 'r') as task_file:
            schedulers = json.load(task_file)

        return schedulers


    @staticmethod
    def save_scheduler_to_json(scheduler):
        schedulers = DataStorage.load_schedulers_dict_from_json()
        scheduler.task.start = serialization_utils.date_to_str(scheduler.task.start)
        scheduler.task.end = serialization_utils.date_to_str(scheduler.task.end)
        scheduler.task.reminder = serialization_utils.time_to_str(scheduler.task.reminder)
        scheduler.date = serialization_utils.date_to_str(scheduler.date)

        scheduler.task = scheduler.task.__dict__
        scheduler = scheduler.__dict__
        schedulers.append(scheduler)

        with open(DataStorage.PATH + '/schedulers.json', 'w') as file:
            json.dump(schedulers, file, indent=2, ensure_ascii=True)


    @staticmethod
    def delete_scheduler_from_json(scheduler):
        schedulers = DataStorage.load_schedulers_from_json()
        counter = 0
        for element in schedulers:
            if element.sid == scheduler.sid:
                break
            counter+=1
        del schedulers[counter]

        changed_schedulers = list()
        for element in schedulers:
            element.date = serialization_utils.date_to_str(element.date)
            element.task.start = serialization_utils.date_to_str(element.task.start)
            element.task.end = serialization_utils.date_to_str(element.task.end)
            element.task.priority = str(element.task.priority.value)
            element.task.reminder = serialization_utils.time_to_str( element.task.reminder)

            element.task = element.task.__dict__
            element = element.__dict__
            changed_schedulers.append(element)


        with open(DataStorage.PATH + '/schedulers.json', 'w') as file:
            json.dump(changed_schedulers, file, indent=2, ensure_ascii=True)



