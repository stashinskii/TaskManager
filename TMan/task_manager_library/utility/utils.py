import os
import json
from datetime import datetime


def get_task_index(tid, storage):
    counter = 0
    for task in storage.tasks:
        if task.tid == tid:
            return counter
        counter+=1
    raise IndexError("Task was not found")


def get_scheduler_index(sid, storage):
    counter = 0
    for scheduler in storage.schedulers:
        if scheduler.sid == sid:
            return counter
        counter += 1
    raise IndexError("Scheduler was not found")


def get_user_index(uid, users):
    counter = 0
    for user in users:
        if user.uid == uid:
            return counter
        counter += 1
    raise IndexError("User was not found")


def check_json_files(path, file):
    check_dir(path)
    if not os.path.exists(path+file):
        print(path+file)
        with open(path+file, 'w') as outfile:
            json.dump([], outfile)


def check_cfg_files(path, file):
    check_dir(path)
    if not os.path.exists(path+file):
        print(path+file)
        with open(path+file, 'w'):
            pass


def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def str_to_date(date):
    """Date checking and converting to datetime utility"""
    time_format_one = "%Y-%m-%d"
    if date is None:
        return None
    try:
        date = datetime.strptime(date, time_format_one)
    except ValueError:
        date = datetime.now()
    return date


def str_to_time(my_time):
    """
    Time checking and converting str to datetime utility
    :param ctx:
    :param my_time: str object - time to be checked
    :return: datetime object
    """
    time_format = "%H:%M"
    try:
        my_time = datetime.strptime(my_time, time_format)
    except:
        my_time = datetime.now()

    return my_time