import configparser
import json
import logging
import os
import uuid

from utility import logging_utils
from utility import serialization_utils
from utility import utils
from .data_storage import DataStorage
from .task_info import User


class UserTools():
    PATH = None
    """
    UserTools class is used to manage users
    """

    @staticmethod
    def validate_login(login):
        """

        :param login:
        :return: if False then login was used before
        """

        users = DataStorage.load_users_from_json()
        for user in users:
            if user.login == login:
                return False
        return True

    @staticmethod
    def set_current():
        users = DataStorage.load_users_from_json()
        for user in users:
            if user.current:
                return user
        raise Exception("There is no current user")
    """
    @staticmethod
    def change_user(login):
        users = DataStorage.load_users_from_json()
        is_changed = None
        for user in users:
            user.current = False
            if user.login == login:
                is_changed = True
                user.set_current()
        if is_changed is True:
            DataStorage.resave_users_json(users)
            return users
        else:
            raise Exception("User not found")
    """

    @staticmethod
    def add_user(login, name, surname, tasks=None):
        UserTools.validate_login(login)
        uid = serialization_utils.tid_gen()
        new_user = User(name, surname, uid, login, False, tasks)
        users = DataStorage.save_users_to_json(new_user.__dict__)
        return users
    """
    @staticmethod
    def get_current_user():
        
        Get current user (authorized)
        :return: User's object
        
        users = DataStorage.load_users_from_json()
        for user in users:
            if user.current:
                return user
        raise Exception("There is no current user")
        """

    @staticmethod
    def get_current_user():
        config = configparser.ConfigParser()
        if UserTools.PATH is None:
            raise TypeError("You didn't set UserTools PATH's value")
        config.read(UserTools.PATH)
        section = "USER"
        login = config.get(section, "current")
        users = DataStorage.load_users_from_json()
        return utils.get_user(login, users)

    @staticmethod
    def set_current_user(login):
        if UserTools.validate_login(login):
            raise Exception("Check login. User doesn't exist")

        config = configparser.ConfigParser()
        config.read(UserTools.PATH)
        section = "USER"
        exist = config.has_section(section)
        if not exist:
            config.add_section(section)
        config.set(section, 'current', login)

        with open(UserTools.PATH, 'w+') as f:
            config.write(f)








