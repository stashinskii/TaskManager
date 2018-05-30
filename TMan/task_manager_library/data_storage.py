import json
import os

from .task_info import *
from .utility import *


data_dir = os.environ['HOME']+'/tmandata'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


class DataStorage:

    @staticmethod
    def load_tasks_from_json():
        """
        Loading (deserializing) tasks's data from json files
        :param current: User object - current user (authorized)
        :return: tuple of collections(lists)
        """
        users = DataStorage.load_users_from_json()
        current = get_active_user(users)

        with open(data_dir + '/trackedtasks.json', 'r') as task_file:
            task_data = json.load(task_file)
        tasks = list()
        all_tasks = list()
        all_users_tasks = list()
        for task_dict in task_data:
            title = task_dict['title']
            start = check_date(None, None, task_dict['start'])
            end = check_date(None, None, task_dict['end'])
            desc = task_dict['description']
            tag = task_dict['tag']
            observers = task_dict['observers']
            executor = task_dict['executor']
            priority = Priority[Priority(int(task_dict['priority'])).name]
            author = task_dict['author']
            reminder = check_time(None, None, task_dict['reminder'])
            is_completed = task_dict['is_completed']
            parent = task_dict['parent']
            tid = task_dict['tid']
            subtasks = task_dict['subtasks']
            planned = task_dict['planned']
            changed = task_dict['changed']

            new_task = TrackedTask(
                title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, tid, subtasks, is_completed, parent
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
    def append_task_to_json(new_task):
        """
        Resave Task's collection to json file
        :param new_task: Tasks's object
        :return:
        """
        users = DataStorage.load_users_from_json()
        current = get_active_user(users)
        DataStorage.add_user_task(current, new_task.tid)
        DataStorage.give_task_permission(new_task.observers, new_task.tid)

        tasks = DataStorage.load_tasks_from_json()[2]
        tasks.append(new_task)
        data = []
        for task in tasks:
            if isinstance(task.start, datetime):
                task.start = date_to_str(task.start)
            if isinstance(task.end, datetime):
                task.end = date_to_str(task.end)
            if isinstance(task.reminder, datetime):
                task.reminder = time_to_str(task.reminder)
            if isinstance(task.priority, Priority):
                task.priority = str(task.priority.value)
            data.append(task.__dict__)
        with open(data_dir + '/trackedtasks.json', 'w') as taskfile:
            json.dump(data, taskfile, indent=2, ensure_ascii=False)


    @staticmethod
    def resave_all_tasks_to_json(all_tasks):
        data = list()
        for task in all_tasks:
            if isinstance(task.start, datetime):
                task.start = date_to_str(task.start)
            if isinstance(task.end, datetime):
                task.end = date_to_str(task.end)
            if isinstance(task.reminder, datetime):
                task.reminder = time_to_str(task.reminder)
            if isinstance(task.priority, Priority):
                task.priority = str(task.priority.value)
            data.append(task.__dict__)

        with open(data_dir + '/trackedtasks.json', 'w') as taskfile:
            json.dump(data, taskfile, indent=2, ensure_ascii=False)

    @staticmethod
    def load_users_from_json():
        """
        Loading(deserializing) users's data from json file
        :return: list of User's objects
        """
        with open(data_dir + '/users.json', 'r') as file:
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

        with open(data_dir + '/trackedtasks.json', 'w') as objfile:
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

        with open(data_dir + '/users.json', 'w') as objfile:
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
        users.__delitem__(get_user_index(user, users))
        user.tasks.append(tid)
        users.append(user)

        data = []
        for user in users:
            data.append(user.__dict__)

        with open(data_dir + '/users.json', 'w') as userfile:
            json.dump(data, userfile, indent=2, ensure_ascii=False)

    @staticmethod
    def resave_users_json(users):
        data = []
        for user in users:
            data.append(user.__dict__)

        with open(data_dir + '/users.json', 'w') as usersfile:
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





