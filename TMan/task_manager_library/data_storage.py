import json
import os
from datetime import datetime

from utility import logging_utils
from utility import serialization_utils
from utility import utils


from .task_info import *


class DataStorage:
    PATH = None
    CURRENT_USER = None

    @staticmethod
    def begin_task(task):
        tracked_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        global_index = all_users_tasks.index(tracked_tasks[task - 1])
        all_users_tasks[global_index].begin()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def done_task(task):
        tracked_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        for subtask in all_tasks:
            if subtask.parent == tracked_tasks[task - 1].tid and subtask.is_completed == Status.undone:
                raise Exception("You have undone subtasks! Done them all before you finish this one!")
        global_index = all_users_tasks.index(tracked_tasks[task - 1])
        all_users_tasks[global_index].complete()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def undone_task(task):
        tracked_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        global_index = all_users_tasks.index(tracked_tasks[task - 1])
        all_users_tasks[global_index].undone()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def done_subtask(task_index, subtask_index):
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tasks[task_index - 1].tid:
                tid_subtasks.append(subtask)

        global_index = get_task_index(tid_subtasks[subtask_index - 1].tid, all_users_tasks)
        all_users_tasks[global_index].complete()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def begin_subtask(task_index, subtask_index):
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tasks[task_index - 1].tid:
                tid_subtasks.append(subtask)

        global_index = get_task_index(tid_subtasks[subtask_index - 1].tid, all_users_tasks)
        all_users_tasks[global_index].begin()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def undone_subtask(task_index, subtask_index):
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tasks[task_index - 1].tid:
                tid_subtasks.append(subtask)

        global_index = get_task_index(tid_subtasks[subtask_index - 1].tid, all_users_tasks)
        all_users_tasks[global_index].undone()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def add_task_to_json(task):
        all_user_tasks = DataStorage.load_tasks_from_json()[2]
        all_user_tasks.append(task)
        current = DataStorage.CURRENT_USER
        DataStorage.add_user_task(current, task.tid)
        DataStorage.resave_all_tasks_to_json(all_user_tasks)

    @staticmethod
    def edit_task(task_num, task_field):
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        current = DataStorage.CURRENT_USER
        author_name = tasks[task_num - 1].author
        if author_name != current.uid:
            raise ValueError("Access denied")

        if (task_num - 1) > len(tasks):
            raise IndexError("Out of range")
        edit = tasks[task_num - 1]
        task_index = all_users_tasks.index(edit)
        data = list()
        data.extend((edit.title, edit.start.date(), edit.end.date(), edit.description))

        #TODO перенесли open nano в UTILS
        if task_field == "title":
            data = DataStorage.open_nano(data, 0)
        elif task_field == "start":
            data = DataStorage.open_nano(data, 1)
        elif task_field == "end":
            data = DataStorage.open_nano(data, 2)
        elif task_field == "description":
            data = DataStorage.open_nano(data, 3)
        else:
            raise ValueError("ERROR! Unsupported field!")

        all_users_tasks[task_index].title = data[0]
        all_users_tasks[task_index].start = utils.check_date(None, None, str(data[1]))
        all_users_tasks[task_index].end = utils.check_date(None, None, str(data[2]))
        all_users_tasks[task_index].description = data[3]
        DataStorage.resave_all_tasks_to_json(all_users_tasks)


    @staticmethod
    def load_tasks_from_json():
        """
        Loading (deserializing) tasks's data from json files
        :param current: User object - current user (authorized)
        :return: tuple of collections(lists)
        """
        # TODO check if CURRENT doesn't exist and None
        current = DataStorage.CURRENT_USER

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
            is_completed = Status[Status(int(task_dict['is_completed'])).name]
            parent = task_dict['parent']
            tid = task_dict['tid']
            subtasks = task_dict['subtasks']
            planned = task_dict['planned']
            changed = task_dict['changed']
            connection = task_dict['connection']

            new_task = Task(
                title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent, tid, subtasks,
                is_completed, connection
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
        for task in all_tasks:
            if isinstance(task.start, datetime):
                task.start = serialization_utils.date_to_str(task.start)
            if isinstance(task.end, datetime):
                task.end = serialization_utils.date_to_str(task.end)
            if isinstance(task.reminder, datetime):
                task.reminder = serialization_utils.time_to_str(task.reminder)
            if isinstance(task.priority, Priority):
                task.priority = str(task.priority.value)
            if isinstance(task.is_completed, Status):
                task.is_completed = str(task.is_completed.value)
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
            with open(DataStorage.PATH + '/trackedtasks.json', 'r') as objfile:
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
            with open(DataStorage.PATH + '/users.json', 'r') as objfile:
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
        current = DataStorage.CURRENT_USER
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
            is_completed = Status[Status(int(scheduler['task']['is_completed'])).name]
            parent = scheduler['task']['parent']
            tid = scheduler['task']['tid']
            subtasks = scheduler['task']['subtasks']
            planned = scheduler['task']['planned']
            changed = scheduler['task']['changed']
            sid = scheduler['sid']
            new_task = Task(
                title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent, tid, subtasks, is_completed
            )
            new_scheduler = Scheduler(date, new_task, sid)
            schedulers_list.append(new_scheduler)
        return schedulers_list


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

    @staticmethod
    def get_subtasks(index):
        user_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        tid = user_tasks[index - 1].tid
        result_collection = list()
        for tasks in all_tasks:
            if tasks.parent == tid:
                result_collection.append(tasks)
        return result_collection

    @staticmethod
    def get_subtasks_parent(index):
        user_tasks = DataStorage.load_tasks_from_json()[0]
        title = user_tasks[index - 1].title
        return title


    @staticmethod
    def get_task_from_id(tid):
        tasks = DataStorage.load_tasks_from_json()[0]
        for task in tasks:
            if task.tid == tid:
                return task
        raise ValueError("Trouble while getting task by tid")

    @staticmethod
    def open_nano(data, num):
        """
        Open nano editor
        :param data: list of task's title, startdate, enddate and description
        :param num: position in list to be changed
        :return: changed data
        """
        os.system("echo \"{}\" >> {}".format(data[num], "/tmp/tman_tempdata.tmp"))
        os.system("nano {}".format("/tmp/tman_tempdata.tmp"))
        file = open("/tmp/tman_tempdata.tmp")
        data[num] = file.read()[0:-1]
        os.system("rm /tmp/tman_tempdata.tmp")
        return data