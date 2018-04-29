from .TaskLib import *
import logging
import json
import uuid


# TODO настроить автоматическое расположение файлов
data_dir = '/home/herman/Рабочий стол/TaskTracker/taskmanager/TMan/TaskData'


# задаем конфигурацию логгирования
logging.basicConfig(filename=data_dir+"/tasklog.log", level=logging.INFO,
                    format='%(levelname)s:%(message)s:(%(asctime)s)')

logging.basicConfig(filename="tasklog.log", level=logging.WARNING,
                    format='%(levelname)s:%(message)s:(%(asctime)s)')


def tid_gen():
    """
    Генерирует task id
    """
    return str(uuid.uuid1())


def add_simple_task(users, current, simple_tasks, title, date, description, priority, tid, permission, is_completed, tag):
    """
    Добавление задачи в список дел
    """
    simple_tasks.append(SimpleListTask(
        title, date, description, priority, tid, permission, is_completed, tag))

    data_to_json(simple_tasks, simple_tasks[-1])
    logging.info('TODO task added. TID: {}'.format(tid))
    add_user_task(users, current, tid)
    return simple_tasks


def data_from_json(type, current):
    """
    Загрузка задач из файла
    """
    simple_tasks = []
    tracked_tasks = []
    event_tasks = []
    users = []
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
                    permission = task_dict['permission']
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
                        permission,
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
                    start = task_dict['start']
                    end = task_dict['end']
                    description = task_dict['description']
                    dash = task_dict['dash']
                    tag = task_dict['tag']
                    observers = task_dict['observers']
                    executor = task_dict['executor']
                    priority = task_dict['priority']
                    author = task_dict['author']
                    reminder = task_dict['reminder']
                    cancel_sync = task_dict['cancel_sync']
                    is_completed = task_dict['is_completed']
                    subtasks = task_dict['subtasks']
                    tid = task_dict['tid']
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
                        subtasks
                    )
                    tracked_tasks.append(new_task)
            return tracked_tasks

        # TODO пересмотреть опцию загрузки сех пользователей. Возможно при нахождении первого current == True стоит выйти и не загружать все.
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

        elif type == "Event":
            pass

    except FileNotFoundError:
        logging.warning("File not exist")
        return []


def data_to_json(collection, object):
    """
    Сохраняем состояние коллекции файле. В качестве аргумента передаем готовый слоаврь объекта
    В зависимости от типа передаваемого объекта, выбираем конкретные файлы для загрузки
    """
    files = [data_dir+'/trackedtasks.json', data_dir+'/subtasks.json',
             data_dir+'/simpletasks.json', data_dir+'/calendarevents.json',
             data_dir+'/users.json']
    if object.__class__.__name__ == 'TrackedTask':
        filename = files[0]
    elif object.__class__.__name__ == 'SubTask':
        filename = files[1]
    elif object.__class__.__name__ == 'SimpleListTask':
        filename = files[2]
    elif object.__class__.__name__ == 'EventCalendar':
        filename = files[3]
    elif object.__class__.__name__ == 'User':
        filename = files[4]
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
    """
    Вывод всех заданий из списка дел с отметкой о статусе выполения и номером
    """
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
    """
    Показать подробную информацию по номеру
    """
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


def delete_simple_task(simple_tasks, num):
    simple_tasks.__delitem__(num-1)
    resave_simple_json(simple_tasks)
    logging.info('TODO task was deleted. TID: {}'.format(simple_tasks[num - 1].tid))


# Далее работа с Трекером дел
def add_tracked_task(tracked_task, tid, title, description, start, end, tag, dash, author,
                   observers, executor, cancel_sync, is_completed, reminder, priority, subtasks):
    tracked_task.append(TrackedTask(
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
        subtasks
    ))
    data_to_json(tracked_task, tracked_task[-1])


def add_subtask(tid, tracked_task, num, title, description, start,
                end, tag, dash, author, observers, executor, cancel_sync, is_completed, reminder, priority):
    tracked_task[num-1].add_subtask(tid, title, description, start, end, tag, dash, author, observers, executor,
                          cancel_sync, is_completed, reminder, priority)

    resave_tracked_json(tracked_task)
    return tracked_task


def resave_tracked_json(tracked_tasks):
    """Пересохранение данных после изменения"""
    data = []
    for task in tracked_tasks:
        data.append(task.__dict__)

    with open(data_dir+'/trackedtasks.json', 'w') as taskfile:
        json.dump(data, taskfile, indent=2, ensure_ascii=False)


def show_tracked_task(tracked_tasks):
    """
    Вывод всех заданий с отметкой о статусе выполения и номером
    """
    try:
        if tracked_tasks is None:
            raise TypeError("Task collection is not list")
        for task in tracked_tasks:
            if task.is_completed:
                marker = "X"
            else:
                marker = " "
            # Возвращаем строку со списком задач и их состоянием
            yield (marker, str(tracked_tasks.index(task)+1),str(len(task.subtasks)), str(task.title))
    except TypeError as e:
        logging.warning('Unable to show tasks')

