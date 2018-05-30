import json
import logging
import os
import uuid

from .data_storage import DataStorage
from .task_info import User
from .utility import tid_gen


class UserTools():
    """
    UserTools class is used to manage users
    """

    @staticmethod
    def validate_login(login):
        users = DataStorage.load_users_from_json()
        for user in users:
            if user.login == login:
                raise Exception("Login was used before")
        return True

    @staticmethod
    def set_current():
        users = DataStorage.load_users_from_json()
        for user in users:
            if user.current:
                return user
        raise Exception("There is no current user")

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

    @staticmethod
    def add_user(login, name, surname, tasks=None):
        uid = tid_gen()
        new_user = User(name, surname, uid, login, False, tasks)
        users = DataStorage.save_users_to_json(new_user.__dict__)
        return users

    @staticmethod
    def get_current_user():
        """
        Get current user (authorized)
        :return: User's object
        """
        users = DataStorage.load_users_from_json()
        for user in users:
            if user.current:
                return user
        raise Exception("There is no current user")








