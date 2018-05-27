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
