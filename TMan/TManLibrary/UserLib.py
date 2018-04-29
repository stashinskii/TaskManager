from .DataLib import *
import uuid
import logging
import json

data_dir = '/home/herman/Рабочий стол/TaskTracker/taskmanager/TMan/TaskData'


def set_current(users):
    """
    Установка текущего пользователя для данного сеанса
    """
    #TODO сохранить изменения
    for user in users:
        if user.current:
            return user
    raise Exception("There is no current user")


def change_user(users, login):
    """
    Смена текущего пользователя
    """
    #TODO Сохранить изменения
    #TODO ошибка, если такого пользователя нет
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
    """Пересохранение данных после изменения"""
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
    from .TaskLib import User
    from .DataLib import data_to_json
    uid = str(uuid.uuid1())
    print(users)
    new_user = User(name, surname, uid, tasks, login, False)
    users = data_to_json(users, new_user)
    print(users)
    logging.info('User added. UID: {}'.format(uid))
    return users


def delete_user(users, user):
    pass


def add_user_task(users, user, tid):
    print(users.index(user))
    users.__delitem__(users.index(user))
    user.tasks['simple'].append(tid)
    users.append(user)

    data = []
    for user in users:
        data.append(user.__dict__)

    with open(data_dir+'/users.json', 'w') as userfile:
        json.dump(data, userfile, indent=2, ensure_ascii=False)



