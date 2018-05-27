import json
import logging
import os
import uuid
from datetime import datetime

from .data_storage import *
from .logging_configuration import *
from .task_info import *
from .user_actions import *
from .utility import *

#при отсутствии такой директории - создаем её
data_dir = os.environ['HOME']+'/tmandata'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


# задаем конфигурацию логгирования
format_info, file_info = loggingConfig.get_logging_config(logging.INFO)
logging.basicConfig(filename=file_info, level=logging.INFO,
                    format=format_info)

format_warning, file_warning = loggingConfig.get_logging_config(logging.WARNING)
logging.basicConfig(filename=file_warning, level=logging.WARNING,
                    format=format_warning)




def add_tracked_task(title=None, desc=None, start=None, end=None,
                     tag=None, author=None, observers=None,executor=None,
                     reminder=None, priority=None,
                     changed=None, planned=None):
    """Adding new task"""
    if observers != "":
        observers = observers.split(",")
    else:
        observers = []
        
    task = TrackedTask(title, desc, start, end, tag, author, observers, executor,
                 reminder, priority, changed, planned)
    check_date_range(start, end)
    resave_task_to_json(task)




def show_tracked_task(tracked_tasks, all_tasks):
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













"""


def add_tracked_task(all_tasks, tid, title, description, start, end, tag,
                    author,observers, executor, is_completed,
                    reminder, priority, users, current, parent, subtasks, changed, planned):
    
    Создание новой задачи, добавление в коллекцию и сохранение в файл
    
    from task_manager_library import EventActions
    if observers != "":
        observers = observers.split(",")
    else:
        observers = []
    if start > end:
        raise ValueError("ERROR! Start date GT end date")
    all_tasks.append(TrackedTask(
        tid,
        title,
        description,
        str(start.year)+"-"+str(start.month)+"-"+str(start.day),
        str(end.year) + "-" + str(end.month) + "-" + str(end.day),
        tag,
        author,
        observers,
        executor,
        is_completed,
        str(reminder.hour) +":"+str(reminder.minute),
        priority,
        parent,
        subtasks,
        changed,
        planned
    ))
    resave_task_to_json(all_tasks)
    from task_manager_library import user_actions
    #data_to_json(all_tasks, all_tasks[-1])
    add_user_task(users, current, tid, "Task")
    for us in observers:
        if us!=current.login:
            user = user_actions.get_user(us, users)
            add_user_task(users, user, tid, "Task")


def resave_task_to_json(tracked_tasks):
 
    Пересохранение задач
    :param tracked_tasks: коллекция задач
    :return:
   
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


"""



