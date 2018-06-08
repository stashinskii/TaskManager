import click
import os
import uuid
import config
import json
from datetime import datetime


def str_to_uuid(str_id):
    """
    Convert str object of task id to UUID object
    :param str_id:
    :return:
    """
    return uuid.UUID(str_id)


def uuid_to_datetime(uuid_id):
    return datetime.fromtimestamp((uuid_id.time - 0x01b21dd213814000)*100/1e9)


def check_date_range(start, end):
    """
    Checking date range utility
    :param start: datetime object
    """
    if start > end:
        raise ValueError("Start date GT end date")


def check_date(ctx, param, date):
    """
    Date checking and converting to datetime utility
    :param ctx:
    :param date: str object - date to be checked
    :return: datetime bject
    """
    time_format_one = "%Y-%m-%d"
    if (date is None):
        raise ValueError

    try:
        date = datetime.strptime(date, time_format_one)
    except ValueError:
        date = datetime.now()
    return date


def check_time(ctx, param, my_time):
    """
    Time checking and converting str to datetime utility
    :param ctx:
    :param my_time: str object - time to be checked
    :return: datetime object
    """
    time_format = "%H:%M"
    my_time = datetime.strptime(my_time, time_format)
    return my_time


def get_active_user(users):
    """
    Get current user (authorized)
    :return: User's object
    """
    for user in users:
        if user.current:
            return user
    raise Exception("There is no current user")


def get_user_index(user, users):
    """
    Get user's index at json file
    :param user: User's object
    :return: int object
    """

    counter = 0
    #print(user.uid)
    #user_uid = user.uid
    for x in users:
        if user.uid == x.uid:
            return counter
        counter += 1
    raise Exception("Trouble while adding task to user")


def get_task_index(tid, all_tasks):
    """
    Get task's index at json file from tid
    :param tid: tid
    :param tasks: list of Task's objects
    :return: int object
    """

    counter = 0
    for x in all_tasks:
        if tid == x.tid:
            return counter
        counter += 1
    raise Exception("Trouble while adding task to user")


def get_user(login, users):
    """
    Get Users's object by his login (str object)
    :param login: str object - login
    :return: User's object
    """
    for user in users:
        if user.login == login:
            return user
    raise Exception("There is no such user")


def get_login(uid, users):
    for user in users:
        if user.uid == uid:
            return user.login
    raise Exception("There is no such user")


def check_json_files(file):

    check_dir()
    if not os.path.exists(config.DATA_PATH+file):
        with open(config.DATA_PATH + file, 'w') as objfile:
            json.dump([], objfile, indent=2, ensure_ascii=False)


def check_log_files(file):
    check_dir()
    if not os.path.exists(file):
        with open(file, 'a+') as f:
            f.write('Logfile created')


def check_dir():
    if not os.path.exists(config.DATA_PATH):
        os.makedirs(config.DATA_PATH)











