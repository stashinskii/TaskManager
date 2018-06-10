def dict_to_task(task_dict):
    """Converting dict object to current Task object"""

    title = task_dict['title']
    start = utils.check_date(None, None, task_dict['start'])
    end = utils.check_date(None, None, task_dict['end'])
    desc = task_dict['description']
    tag = Tag(task_dict['tag']['tag_name'], task_dict['tag']['description'])
    observers = task_dict['observers']
    executor = task_dict['executor']
    priority = Priority[Priority(int(task_dict['priority'])).name]
    author = task_dict['author']
    reminder = utils.check_time(None, None, task_dict['reminder'])
    is_completed = Status[Status(int(task_dict['is_completed'])).name]
    parent = task_dict['parent']
    tid = task_dict['tid']
    subtasks = task_dict['subtasks']
    planned = task_dict['planned']
    changed = task_dict['changed']
    connection = task_dict['connection']

    task = Task(
                title, desc,
                start, end,
                tag, author,
                observers, executor,
                reminder, priority,
                changed, planned,
                parent, tid, subtasks,
                is_completed, connection
                )
    return task


def dict_to_user(data_dict):
    name = data_dict['name']
    surname = data_dict['surname']
    login = data_dict['login']
    uid = data_dict['uid']
    tasks = data_dict['tasks']
    current = data_dict['current']
    user = User(name, surname, uid, login, current, tasks)
    return user


def task_to_dict(task):
    if isinstance(task.start, datetime):
        task.start = serialization_utils.date_to_str(task.start)
    if isinstance(task.end, datetime):
        task.end = serialization_utils.date_to_str(task.end)
    if isinstance(task.reminder, datetime):
        task.reminder = serialization_utils.time_to_str(task.reminder)
    if isinstance(task.priority, Priority):
        task.priority = str(task.priority.value)
    if isinstance(task.is_completed, Status):
        task.is_completed = str(task.is_completed.value)
    if isinstance(task.tag, Tag):
        task.tag = task.tag.__dict__

    return task


