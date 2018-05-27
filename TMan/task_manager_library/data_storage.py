import json
import os

from .task_info import *
from .user_actions import *
from .utility import *

data_dir = os.environ['HOME']+'/tmandata'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def load_tasks_from_json(o):
    """
    Loading (deserializing) tasks's data from json files
    :param current: User object - current user (authorized)
    :return: tuple of collections(lists)
    """
    current = get_current_user()

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
            if task_dict['tid'] in current.tasks['task']:
                tasks.append(new_task)
                all_tasks.append(new_task)
            all_users_tasks.append(new_task)
        else:
            all_tasks.append(new_task)
            all_users_tasks.append(new_task)
    return tasks, all_tasks, all_users_tasks


def resave_task_to_json(new_task):
    """
    Resave Task's collection to json file
    :param new_task: Tasks's object
    :return:
    """
    current = get_current_user()
    add_user_task(current, new_task.tid)
    give_task_permission(new_task.observers, new_task.tid)

    tasks = load_tasks_from_json(current)[2]
    tasks.append(new_task)
    data = []
    for task in tasks:
        #TODO create method DATE-TO-STR AND USE IN HERE
        if isinstance(task.start, datetime):
            task.start = str(task.start.year)+"-"+str(task.start.month)+"-"+str(task.start.day)
        if isinstance(task.end, datetime):
            task.end = str(task.end.year) + "-" + str(task.end.month) + "-" + str(task.end.day)
        if isinstance(task.reminder, datetime):
            task.reminder = str(task.reminder.hour) +":"+str(task.reminder.minute)
        if isinstance(task.priority, Priority):
            task.priority = str(task.priority.value)
        data.append(task.__dict__)
    with open(data_dir+'/trackedtasks.json', 'w') as taskfile:
        json.dump(data, taskfile, indent=2, ensure_ascii=False)


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
        user = User(name, surname, uid, tasks, login, current)
        users.append(user)
    return users


def save_tasks_to_json(task_object):
    """
    Save data to json - Serialization
    :param task_object: Task's object
    """
    try:
        with open(data_dir+'/trackedtasks.json', 'r') as objfile:
            collection = json.load(objfile)

    except FileNotFoundError:
        collection = []
        logging.warning("Can't load json file")
    collection.append(task_object)

    with open(data_dir+'/trackedtasks.json', 'w') as objfile:
        json.dump(collection, objfile, indent=2, ensure_ascii=False)


def save_users_to_json(user_object):
    """
    Save new user to json file
    :param user_object: User's object
    :return:
    """
    try:
        with open(data_dir+'/users.json', 'r') as objfile:
            collection = json.load(objfile)

    except FileNotFoundError:
        collection = []
        logging.warning("Can't load json file")
    collection.append(user_object)

    with open(data_dir+'/users.json', 'w') as objfile:
        json.dump(collection, objfile, indent=2, ensure_ascii=False)


def get_current_user():
    """
    Get current user (authorized)
    :return: User's object
    """
    users = load_users_from_json()
    for user in users:
        if user.current:
            return user
    raise Exception("There is no current user")


def give_task_permission(observers, tid):
    """
    Give permission to observers
    :param observers: list on User's objects
    :param tid: str object
    :return:
    """
    current = get_current_user()
    for us in observers:
        if us != current.login:
            user = get_user(us)
            add_user_task(user, tid)


def add_user_task(user, tid):
    """
    Add task tid to user at users json file
    :param user: User's object
    :param tid: str object
    :return:
    """
    users = load_users_from_json()
    users.__delitem__(get_user_index(user))
    user.tasks['task'].append(tid)
    users.append(user)

    data = []
    for user in users:
        data.append(user.__dict__)

    with open(data_dir+'/users.json', 'w') as userfile:
        json.dump(data, userfile, indent=2, ensure_ascii=False)


def get_user_index(user):
    """
    Get user's index at json file
    :param user: User's object
    :return: int object
    """
    users = load_users_from_json()
    counter = 0
    for x in users:
        if user.uid == x.uid:
            return counter
        counter += 1
    raise Exception("Trouble while adding task to user")


def get_user(login):
    """
    Get Users's object by his login (str object)
    :param login: str object - login
    :return: User's object
    """
    users = load_users_from_json()
    for user in users:
        if user.login == login:
            return user
    raise Exception("There is no such user")
