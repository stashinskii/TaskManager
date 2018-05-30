import os
import uuid
from datetime import datetime


def tid_gen():
    """
    Task id generator, using UUID
    :return: id in str
    """
    return str(uuid.uuid1())


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


#TODO TEST IT
def split_str_to_list(splitter, current_user):
    """
    Split string separated by ',' and convert it to list
    :param splitter:
    :return:
    """
    if splitter != "":
        splitter += ',{}'.format(current_user.login)
    else:
        splitter = current_user.login

    if splitter != "":
        splitter = splitter.split(",")
    else:
        splitter = []

    return splitter