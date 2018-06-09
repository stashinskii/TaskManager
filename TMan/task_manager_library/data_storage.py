"""
This module represents DataStorage class which is contains methods to manage tasks, schedulers,
users and store them in their json files.

To use DataStorage, primarily user need to set up PATH and CURRENT_USER for current work of application.

All methods in DataStorage are static

All methods describes logic of resaving and loading files from JSON
"""
import json
import os
from datetime import datetime

from task_manager_library.models.scheduler_model import Scheduler
from task_manager_library.models.task_model import Status, Task, Priority, Tag
from task_manager_library.models.notifications_model import Notifications
from task_manager_library.utility import logging_utils, utils, serialization_utils
from console.user import User



class DataStorage:
    """Database class.Requires to initialize PATH and CURRENT_USER for correct usage of library """
    PATH = None
    CURRENT_USER = None

    # region DB methods

    @staticmethod
    def begin_task(tid):
        """Change status of task to PROCESS/ Begin task"""

        tracked_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        index = utils.get_task_index(tid, all_users_tasks)
        all_users_tasks[index].begin()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def done_task(tid):
        """Change status of task to DONE/ Complete task"""
        tracked_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        index = utils.get_task_index(tid, all_users_tasks)

        for subtask in all_tasks:
            if subtask.parent == all_users_tasks[index].tid and subtask.is_completed == Status.undone:
                raise Exception("You have undone subtasks! Done them all before you finish this one!")

        all_users_tasks[index].complete()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def undone_task(tid):
        """Change status of task to UNDONE/ Uncomplete task"""
        tracked_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        index = utils.get_task_index(tid, all_users_tasks)
        all_users_tasks[index].undone()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def show_ordered_tasks_priority(priority):
        """Order task by priority and return list of them"""
        all_tasks = DataStorage.load_tasks_from_json()[1]
        ordered_tasks = list()

        for task in all_tasks:
            if task.priority == priority:
                ordered_tasks.append(task)
        if len(ordered_tasks) == 0:
            raise IndexError("There is no such tasks with this {}".format(priority))
        return ordered_tasks

    @staticmethod
    def show_ordered_tasks_tag(tag):
        """Order task by tag and return list of them"""
        all_tasks = DataStorage.load_tasks_from_json()[1]
        ordered_tasks = list()

        for task in all_tasks:
            if task.tag.tag_name == tag.tag_name:
                ordered_tasks.append(task)
        if len(ordered_tasks) == 0:
            raise IndexError("There is no such tasks with this tag {}".format(tag.tag_name))
        return ordered_tasks

    @staticmethod
    def add_task_to_json(task):
        """Add new task to json file using serialization"""
        all_user_tasks = DataStorage.load_tasks_from_json()[2]
        users = DataStorage.load_users_from_json()
        all_user_tasks.append(task)
        current = DataStorage.CURRENT_USER
        DataStorage.add_user_task(current, task.tid)
        for observer in task.observers:
            observer_object = utils.get_user(observer, users)
            DataStorage.add_user_task(observer_object, task.tid)
        DataStorage.resave_all_tasks_to_json(all_user_tasks)

    @staticmethod
    def make_link(task1, task2):
        """Make link/connection between two tasks(including subtasks) by their TID"""
        all_tasks = DataStorage.load_tasks_from_json()[2]
        first_index = utils.get_task_index(task1, all_tasks)
        second_index = utils.get_task_index(task2, all_tasks)

        all_tasks[first_index].connection.append(task2)
        all_tasks[second_index].connection.append(task1)

        DataStorage.resave_all_tasks_to_json(all_tasks)

    @staticmethod
    def edit_task(tid, task_field):
        """Editing task by its index and field name to be edit"""
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        current = DataStorage.CURRENT_USER

        task_index = utils.get_task_index(tid, all_users_tasks)

        author_name = all_users_tasks[task_index].author
        if author_name != current.uid:
            raise ValueError("Access denied")

        edit = all_users_tasks[task_index]

        data = list()
        data.extend((edit.title, edit.start.date(), edit.end.date(), edit.description))

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
        """Loading (deserializing) tasks's data from json files"""
        utils.check_json_files('/trackedtasks.json')
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
            tag = Tag(task_dict['tag']['tag_name'], task_dict['tag']['description'])
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
    def resave_all_tasks_to_json(all_tasks):

        """Resaving all_tasks (including tasks of other users) to json"""

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
            if isinstance(task.tag, Tag):
                task.tag = task.tag.__dict__

            data.append(task.__dict__)

        with open(DataStorage.PATH + '/trackedtasks.json', 'w') as taskfile:
            json.dump(data, taskfile, indent=2, ensure_ascii=False)

    @staticmethod
    def load_users_from_json():

        """Loading(deserializing) users's data from json file"""

        utils.check_json_files('/users.json')
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

        """Save new user to json file"""
        try:
            with open(DataStorage.PATH + '/users.json', 'r') as objfile:
                collection = json.load(objfile)

        except FileNotFoundError:
            collection = []
        collection.append(user_object)

        with open(DataStorage.PATH + '/users.json', 'w') as objfile:
            json.dump(collection, objfile, indent=2, ensure_ascii=False)

    @staticmethod
    def add_user_task(user, tid):
        """Add task tid to user at users json file"""
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
        """Resave users list aster changing"""
        data = []
        for user in users:
            data.append(user.__dict__)

        with open(DataStorage.PATH + '/users.json', 'w') as usersfile:
            json.dump(data, usersfile, indent=2, ensure_ascii=False)

    @staticmethod
    def give_task_permission(observers, tid):
        """Give permission of task (tid to observers (list of logins)"""
        users = DataStorage.load_users_from_json()

        current = DataStorage.CURRENT_USER

        for us in observers:
            if us != current.login:
                user = utils.get_user(us, users)
                DataStorage.add_user_task(user, tid)

    @staticmethod
    def load_schedulers_from_json():
        """Load scheduler from from json by converting dict of schedulers to objects"""
        schedulers = DataStorage.load_schedulers_dict_from_json()
        schedulers_list = list()

        for scheduler in schedulers:
            last = utils.check_date(None, None, scheduler['last'])
            title = scheduler['task']['title']
            start = utils.check_date(None, None, scheduler['task']['start'])
            end = utils.check_date(None, None, scheduler['task']['end'])
            desc = scheduler['task']['description']
            tag = scheduler['task']['tag']['tag_name']
            tag = Tag(tag)
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
            interval = scheduler['interval']
            new_task = Task(
                title, desc, start, end, tag, author, observers, executor,
                reminder, priority, changed, planned, parent, tid, subtasks, is_completed
            )

            new_scheduler = Scheduler(last, new_task, interval, sid)
            schedulers_list.append(new_scheduler)
        return schedulers_list

    @staticmethod
    def load_schedulers_dict_from_json():
        """Load schedulers from json without converting to needed types"""
        utils.check_json_files('/schedulers.json')
        with open(DataStorage.PATH + '/schedulers.json', 'r') as task_file:
            schedulers = json.load(task_file)

        return schedulers

    @staticmethod
    def save_scheduler_to_json(scheduler):
        """Save scheduler object to json"""
        schedulers = DataStorage.load_schedulers_dict_from_json()
        scheduler.task.start = serialization_utils.date_to_str(scheduler.task.start)
        scheduler.task.end = serialization_utils.date_to_str(scheduler.task.end)
        scheduler.task.reminder = serialization_utils.time_to_str(scheduler.task.reminder)
        scheduler.last = serialization_utils.date_to_str(scheduler.last)
        scheduler.task.is_completed = str(scheduler.task.is_completed.value)
        if isinstance(scheduler.task.priority, Priority):
            scheduler.task.priority = str(scheduler.task.priority.value)
        scheduler.task.tag = scheduler.task.tag.__dict__
        scheduler.task = scheduler.task.__dict__
        scheduler = scheduler.__dict__
        schedulers.append(scheduler)
        with open(DataStorage.PATH + '/schedulers.json', 'w') as file:
            json.dump(schedulers, file, indent=2, ensure_ascii=True)

    @staticmethod
    def delete_task(tid):
        """Delete task by its tid"""
        all_tasks = DataStorage.load_tasks_from_json()[2]
        global_index = utils.get_task_index(tid, all_tasks)
        del all_tasks[global_index]
        DataStorage.resave_all_tasks_to_json(all_tasks)

    @staticmethod
    def delete_scheduler_from_json(scheduler):
        """Deleting sceduler for resaving"""
        schedulers = DataStorage.load_schedulers_from_json()
        counter = 0
        for element in schedulers:
            if element.sid == scheduler.sid:
                break
            counter += 1
        del schedulers[counter]

        changed_schedulers = list()
        for element in schedulers:
            element.last = serialization_utils.date_to_str(element.last)
            element.task.start = serialization_utils.date_to_str(element.task.start)
            element.task.end = serialization_utils.date_to_str(element.task.end)
            element.task.priority = str(element.task.priority.value)
            element.task.reminder = serialization_utils.time_to_str(element.task.reminder)
            element.task.tag = element.task.tag.__dict__
            element.task.is_completed = str(element.task.is_completed.value)
            element.task = element.task.__dict__
            element = element.__dict__
            changed_schedulers.append(element)

        with open(DataStorage.PATH + '/schedulers.json', 'w') as file:
            json.dump(changed_schedulers, file, indent=2, ensure_ascii=True)

    @staticmethod
    def get_subtasks(index):
        """Get subtasks by index"""
        user_tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        len_of_tasks = len(user_tasks)
        if index > len_of_tasks:
            raise IndexError("You dont have subtasks with such index {}!".format(index))

        tid = user_tasks[index - 1].tid
        result_collection = list()
        for tasks in all_tasks:
            if tasks.parent == tid:
                result_collection.append(tasks)
        return result_collection

    @staticmethod
    def get_subtasks_parent(tid):
        """Get parent of subtask"""
        all_user_tasks = DataStorage.load_tasks_from_json()[2]
        index = utils.get_task_index(tid, all_user_tasks)
        parent_tid = all_user_tasks[index]
        return DataStorage.get_task_from_id(parent_tid).title

    @staticmethod
    def get_subtasks_of_parent(tid):
        """Get subtasks of parent"""
        all_user_tasks = DataStorage.load_tasks_from_json()[2]

        subtasks = list()

        for task in all_user_tasks:
            if task.parent == tid:
                subtasks.append(task)

        return subtasks

    @staticmethod
    def get_task_from_id(tid):
        """Get task from task's tid"""
        tasks = DataStorage.load_tasks_from_json()[2]
        for task in tasks:
            if task.tid == tid:
                return task
        raise ValueError("Trouble while getting task by tid")

    @staticmethod
    def open_nano(data, num):
        """Open nano editor"""
        os.system("echo \"{}\" >> {}".format(data[num], "/tmp/tman_tempdata.tmp"))
        os.system("nano {}".format("/tmp/tman_tempdata.tmp"))
        file = open("/tmp/tman_tempdata.tmp")
        data[num] = file.read()[0:-1]
        os.system("rm /tmp/tman_tempdata.tmp")
        return data

    # endregion

    # region Notifications

    @staticmethod
    def add_notification(notification):
        """Create new notification"""
        all_notifications = DataStorage.load_notifications_from_json()
        result_notifications = list()
        for notify in all_notifications:
            notify.date = serialization_utils.date_to_str(notify.date)
            notify.reminder = serialization_utils.time_to_str(notify.reminder)
            notify = notify.__dict__
            result_notifications.append(notify)

        notification.date = serialization_utils.date_to_str(notification.date)
        notification.reminder = serialization_utils.time_to_str(notification.reminder)
        notification = notification.__dict__
        result_notifications.append(notification)

        with open(DataStorage.PATH + '/notifications.json', 'w') as file:
            json.dump(result_notifications, file, indent=2, ensure_ascii=True)

    @staticmethod
    def load_notifications_from_json():
        """Load/Deserialize notifications from json file"""
        utils.check_json_files('/notifications.json')
        with open(DataStorage.PATH + '/notifications.json', 'r') as task_file:
            notifications = json.load(task_file)

        notifications_list = list()
        for notificaion in notifications:
            notifications_list.append(
                Notifications(
                    notificaion['task_id'],
                    utils.check_time(None, None, notificaion['reminder']),
                    utils.check_date(None, None, notificaion['date']),
                    notificaion['title'],
                    notificaion['rid']))
        return notifications_list

    @staticmethod
    def delete_notification(rid):
        """Delete notification from its Reminder ID"""
        notifications = DataStorage.load_notifications_from_json()

        prepared_notifications = list()

        for notification in notifications:
            if notification.rid == rid:
                continue
            notification.date = serialization_utils.date_to_str(notification.date)
            notification.reminder = serialization_utils.time_to_str(notification.reminder)
            notification = notification.__dict__
            prepared_notifications.append(notification)

        with open(DataStorage.PATH + '/notifications.json', 'w') as file:
            json.dump(prepared_notifications, file, indent=2, ensure_ascii=True)

    # endregion


"""
@staticmethod
    def done_subtask(task_index, subtask_index):
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tasks[task_index - 1].tid:
                tid_subtasks.append(subtask)

        global_index = utils.get_task_index(tid_subtasks[subtask_index - 1].tid, all_users_tasks)
        all_users_tasks[global_index].complete()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def begin_subtask(task_index, subtask_index):
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tasks[task_index - 1].tid:
                tid_subtasks.append(subtask)

        global_index = utils.get_task_index(tid_subtasks[subtask_index - 1].tid, all_users_tasks)
        all_users_tasks[global_index].begin()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)

    @staticmethod
    def undone_subtask(task_index, subtask_index):
        tasks, all_tasks, all_users_tasks = DataStorage.load_tasks_from_json()
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tasks[task_index - 1].tid:
                tid_subtasks.append(subtask)

        global_index = utils.get_task_index(tid_subtasks[subtask_index - 1].tid, all_users_tasks)
        all_users_tasks[global_index].undone()
        DataStorage.resave_all_tasks_to_json(all_users_tasks)
"""
