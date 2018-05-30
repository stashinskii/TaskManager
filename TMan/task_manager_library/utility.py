import os
import uuid
from datetime import datetime


def str_to_uuid(str_id):
    return uuid.UUID(str_id)


def uuid_to_datetime(uuid_id):
    return datetime.fromtimestamp((uuid_id.time - 0x01b21dd213814000)*100/1e9)


def tid_gen():
    """
    Task id generator
    :return: id in str
    """
    return str(uuid.uuid1())


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


def date_to_str(date):
    """
    Converting datetime objects (Date) to str to serialize them into json
    :param date: datetime object
    :return: str object
    """
    str_date = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return str_date


def time_to_str(time):
    """
    Converting datetime objects (Time) to str to serialize them into json
    :param time: datetime object
    :return: str object
    """
    str_time = str(time.hour) + ":" + str(time.minute)
    return str_time


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
    for x in users:
        if user.uid == x.uid:
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


def open_nano(data, num):
    os.system("echo \"{}\" >> {}".format(data[num], "/tmp/tman_tempdata.tmp"))
    os.system("nano {}".format("/tmp/tman_tempdata.tmp"))
    file = open("/tmp/tman_tempdata.tmp")
    data[num] = file.read()[0:-1]
    os.system("rm /tmp/tman_tempdata.tmp")
    return data





