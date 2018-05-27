import json
import logging
import os
import uuid

#from .data_storage import get_current

data_dir = os.environ['HOME']+'/tmandata/'




def set_current(users):
    """
    Установка текущего пользователя для данного сеанса
    """
    for user in users:
        if user.current:
            return user
    raise Exception("There is no current user")


def get_user(login, users):
    """
    Получить объект пользователя по логину
    :param login:
    :param users:
    :return:
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


def change_user(users, login):
    is_changed = None
    for user in users:
        user.current = False
        if user.login == login:
            is_changed = True
            user.set_current()
    if is_changed is True:
        resave_users_json(users)
        return users
    else:
        raise Exception("User not found")


def resave_users_json(users):
    data = []
    for user in users:
        data.append(user.__dict__)

    with open(data_dir+'/users.json', 'w') as usersfile:
        json.dump(data, usersfile, indent=2, ensure_ascii=False)


def validate_login(users, login):
    """
    Проверка существования такого же логина
    True - такой логин прошёл валидацию
    """
    for user in users:
        if user.login == login:
            raise Exception("Login was used before")
    return True


def add_user(users, name, surname, login, tasks):
    from .task_info import User
    from .data_actions import data_to_json
    uid = str(uuid.uuid1())
    new_user = User(name, surname, uid, tasks, login, False)
    users = data_to_json(users, new_user)
    logging.info('User added. UID: {}'.format(uid))
    return users


def logout(users):
    for user in users:
        user.current = False
    resave_users_json(users)


def add_user_task(users, user, tid):
    users.__delitem__(users.index(user))
    user.tasks['task'].append(tid)
    users.append(user)

    data = []
    for user in users:
        data.append(user.__dict__)

    with open(data_dir+'/users.json', 'w') as userfile:
        json.dump(data, userfile, indent=2, ensure_ascii=False)



