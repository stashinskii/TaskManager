from .TaskLib import *
import logging
import json
import uuid
from datetime import datetime


# TODO настроить автоматическое расположение файлов
data_dir = '/home/herman/Рабочий стол/TaskTracker/src/TMan/TaskData'


# задаем конфигурацию логгирования
logging.basicConfig(filename=data_dir+"/tasklog.log", level=logging.INFO,
                    format='%(levelname)s:%(message)s:(%(asctime)s)')

logging.basicConfig(filename="tasklog.log", level=logging.WARNING,
                    format='%(levelname)s:%(message)s:(%(asctime)s)')


def tid_gen():
    """Генерирует task id"""
    return str(uuid.uuid1())


def add_simple_task(users, current, simple_tasks, title, date, description, priority, tid, is_completed, tag):
    """Добавление задачи в список дел"""
    simple_tasks.append(SimpleListTask(
        title, str(date.year)+"-"+str(date.month)+"-"+str(date.day),
        description, priority, tid, is_completed, tag))

    data_to_json(simple_tasks, simple_tasks[-1])
    logging.info('TODO task added. TID: {}'.format(tid))
    add_user_task(users, current, tid, "TODO")
    return simple_tasks


def check_date(date):
    time_format_one = "%b %d, %Y"
    if (date is None):
        raise ValueError

    try:
        date = datetime.strptime(date, time_format_one)
    except ValueError:
        date = datetime.now()
    return date


def check_time(mytime):

    time_format = "%H:%M"
    mytime = datetime.strptime(mytime, time_format)
    return mytime


def data_from_json(type, current):
    """Загрузка задач из файла"""
    simple_tasks = []
    tracked_tasks = []
    users = []
    all_tasks = []
    try:
        if type == "TODO":
            with open(data_dir+'/simpletasks.json', 'r') as todo_task_file:
                simple_data = json.load(todo_task_file)

            for task_dict in simple_data:
                """
                Загрузка задач, которые принадлежат пользователю
                """
                if task_dict['tid'] in current.tasks['simple']:
                    title = task_dict['title']
                    tid = task_dict['tid']
                    date = task_dict['date']
                    description = task_dict['description']
                    priority = task_dict['priority']
                    tag = task_dict['tag']
                    is_completed = task_dict['is_completed']
                    new_task = SimpleListTask(
                        title,
                        date,
                        description,
                        priority,
                        tid,
                        is_completed,
                        tag
                    )
                    simple_tasks.append(new_task)
            return simple_tasks

        elif type=="Task":
            with open(data_dir+'/trackedtasks.json', 'r') as task_file:
                task_data = json.load(task_file)

            for task_dict in task_data:
                if task_dict['tid'] in current.tasks['task']:
                    title = task_dict['title']
                    start = check_date(task_dict['start'])
                    end = check_date(task_dict['end'])
                    description = task_dict['description']
                    dash = task_dict['dash']
                    tag = task_dict['tag']
                    observers = task_dict['observers']
                    executor = task_dict['executor']
                    priority = Priority[Priority(int(task_dict['priority'])).name]
                    author = task_dict['author']
                    reminder = check_time(task_dict['reminder'])
                    cancel_sync = task_dict['cancel_sync']
                    is_completed = task_dict['is_completed']
                    parent = task_dict['parent']
                    tid = task_dict['tid']
                    subtasks = task_dict['subtasks']

                    new_task = TrackedTask(
                        tid,
                        title,
                        description,
                        start,
                        end,
                        tag,
                        dash,
                        author,
                        observers,
                        executor,
                        cancel_sync,
                        is_completed,
                        reminder,
                        priority,
                        parent,
                        subtasks
                    )
                    if task_dict['parent'] is None:
                        tracked_tasks.append(new_task)
                        all_tasks.append(new_task)
                    else:
                        all_tasks.append(new_task)
            return tracked_tasks, all_tasks

        elif type == "User":
            with open(data_dir+'/users.json', 'r') as file:
                data = json.load(file)

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


    except FileNotFoundError:
        logging.warning("File not exist")
        return []


def data_to_json(collection, object):
    """
    Сохраняем состояние коллекции файле. В качестве аргумента передаем готовый слоаврь объекта
    В зависимости от типа передаваемого объекта, выбираем конкретные файлы для загрузки
    """
    files = [data_dir+'/trackedtasks.json',
             data_dir+'/simpletasks.json', data_dir+'/users.json']
    if object.__class__.__name__ == 'TrackedTask':
        filename = files[0]
    elif object.__class__.__name__ == 'SimpleListTask':
        filename = files[1]
    elif object.__class__.__name__ == 'User':
        filename = files[2]
    else:
        raise Exception("Unknown type of object")

    object = object.__dict__

    try:
        with open(filename, 'r') as objfile:
            collection = json.load(objfile)

    except FileNotFoundError:
        collection = []
        logging.warning("Can't load json file")
    collection.append(object)

    with open(filename, 'w') as objfile:
        json.dump(collection, objfile, indent=2, ensure_ascii=False)

    return collection


def show_simple_task(simple_tasks):
    """Вывод всех заданий из списка дел с отметкой о статусе выполения и номером"""
    try:
        if simple_tasks is None:
            raise TypeError("TODO collection is not list")
        for task in simple_tasks:
            if task.is_completed:
                marker = "X"
            else:
                marker = " "
            # Возвращаем строку со списком задач и их состоянием
            yield ("[" + marker + "]" + " - " + str(simple_tasks.index(task)+1)
                   + " - " + str(task.title))
    except TypeError as e:
        logging.warning('Unable to show todo tasks')


def show_simple_info(simple_tasks, num):
    """Показать подробную информацию по номеру"""
    return simple_tasks[num-1]


def resave_simple_json(simple_tasks):
    """Пересохранение данных после изменения"""
    data = []
    for task in simple_tasks:
        data.append(task.__dict__)

    with open(data_dir+'/simpletasks.json', 'w') as todotaskfile:
        json.dump(data, todotaskfile, indent=2, ensure_ascii=False)


def complete_simple_task(simple_tasks, num):
    """Пометить задачу как выполненную"""
    simple_tasks[num-1].complete()
    resave_simple_json(simple_tasks)
    logging.info('TODO task was done/undone. TID: {}'.format(simple_tasks[num-1].tid))
    return simple_tasks


def delete_simple_task(simple_tasks, num, tracked_tasks):
    for task in tracked_tasks:
        if task.tid == simple_tasks[num-1].tid:
            index = tracked_tasks.index(task)
            break
    if index is not None:
        tracked_tasks[index].cancel_sync = True
        resave_tracked_json(tracked_tasks)
    deleted_tid = simple_tasks[num - 1].tid
    simple_tasks.__delitem__(num-1)
    resave_simple_json(simple_tasks)
    logging.info('TODO task was deleted. TID: {}'.format(deleted_tid))


# Далее работа с Трекером дел
def add_tracked_task(all_tasks, simple_tasks, tid, title, description, start, end, tag, dash, author,
                   observers, executor, cancel_sync, is_completed, reminder, priority, users, current, parent, subtasks):
    from TManLibrary import Sync
    if start > end:
        raise ValueError("ERROR! Start date GT end date")
    all_tasks.append(TrackedTask(
        tid,
        title,
        description,
        str(start.year)+"-"+str(start.month)+"-"+str(start.day),
        str(end.year) + "-" + str(end.month) + "-" + str(end.day),
        tag,
        dash,
        author,
        observers,
        executor,
        cancel_sync,
        is_completed,
        str(reminder.hour) +":"+str(reminder.minute),
        priority,
        parent,
        subtasks
    ))
    resave_tracked_json(all_tasks)
    #data_to_json(all_tasks, all_tasks[-1])
    add_user_task(users, current, tid, "Task")
    if cancel_sync != True:
        Sync.to_todo(users, current, simple_tasks, title, tid, description, priority, is_completed, end, tag)


def resave_tracked_json(tracked_tasks):
    """Пересохранение данных после изменения"""
    data = []
    for task in tracked_tasks:
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


def show_tracked_task(tracked_tasks, all_tasks):
    """Вывод всех заданий с отметкой о статусе выполения и номером"""
    try:
        if tracked_tasks is None:
            raise TypeError("Task collection is not list")
        for task in tracked_tasks:
            subtasks = []
            for subtask in all_tasks:
                if subtask.parent == task.tid:
                    subtasks.append(subtask.tid)

            if task.is_completed:
                marker = "X"
            else:
                marker = " "
            # Возвращаем строку со списком задач и их состоянием
            yield (marker, str(tracked_tasks.index(task)+1),str(len(subtasks)), str(task.title))
    except TypeError as e:
        logging.warning('Unable to show tasks')


def str_to_uuid(str_id):
    """UUID строку в UUID"""
    return uuid.UUID(str_id)


def uuid_to_datetime(uuid_id):
    """UUID в объект datetime"""
    return datetime.fromtimestamp((uuid_id.time - 0x01b21dd213814000)*100/1e9)
