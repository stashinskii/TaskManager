import json
import uuid
import TaskLib
import logging
import DataLib

data_dir = '/home/herman/Рабочий стол/TMan/TaskData'


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


def add_user(users, name, surname, login):
    uid = str(uuid.uuid1())
    new_user = TaskLib.User(name, surname, uid, [], login, False)
    users = DataLib.data_to_json(users, new_user)
    users.append(TaskLib.User)
    logging.info('User added. UID: {}'.format(uid))
    return users