import click
import os

import task_manager_library


@click.group(invoke_without_command=True)
def cli():
    """
    Entry point to CLI application
    """
    click.clear()

# region User actions


@cli.command()
def current():
    """
    Set current user
    """
    try:
        current = task_manager_library.UserTools.get_current_user()
        click.echo("Login: {}".format(current.login))
        click.echo("Full name: {} {}".format(current.name, current.surname))
        click.echo("UID: {}".format(current.uid))
    except Exception as e:
        print(e)


@cli.command()
@click.option('--login', type=str, default=None,
              help='Unique login of new user')
@click.option('--name', type=str, default='UserName',
              help='Name of new user')
@click.option('--surname', type=str, default='UserName',
              help='surname of new user')
def add_user(login, name, surname):
    """
    Adding new user
    """
    task_manager_library.UserTools.add_user(login, name, surname)


@cli.command()
@click.option('--login', type=str,
              help='Login to switch the users')
def change_user(login):
    """
    Set user as current
    """
    task_manager_library.UserTools.change_user(login)

# endregion

# region Task actions


@cli.command()
@click.option('--task/--subtask',
              help='Adding task or subtask to tracker manager')
@click.option('-sd', '--startdate', type=str, callback=task_manager_library.check_date,
              help='Start date')
@click.option('-ed', '--enddate', type=str, callback=task_manager_library.check_date,
              help='End date')
@click.option('-tg', '--tag', type=str,
              help='Tag')
@click.option('-de', '--description', type=str,
              help='Description')
@click.option('-ti', '--title', type=str,
              help='Title')
@click.option('-re', '--reminder', type=str, callback=task_manager_library.check_time,
              help='Reminder')
@click.option('-ob', '--observers',  type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=str,
              help='Priority')
@click.option('-i', '--index', type=int,
              help='Index of task to add subtask')
def add(task, startdate, enddate, tag, description,
        title, reminder, observers, priority, index):
    """Adding new task"""
    if task:
        task_manager_library.add_tracked_task(title, description, startdate, enddate,
                                              tag, observers, reminder, priority)
    else:
        task_manager_library.add_subtask(index, title, description, startdate, enddate,
                                              tag, observers, reminder, priority)



@cli.command()
@click.option('--task', is_flag=True,
              help='List of tasks')
def list(task):

    if task:
        import task_manager_library
        task_gen = task_manager_library.show_tracked_task()
        for task in task_gen:
            click.echo("[" + task[0] + "] - " + task[1] + " - " + click.style(
                "Subtasks: " + task[2], bold=True, fg='yellow')
                + " - " + click.style(task[3], bold=True, bg='green'))


@cli.command()
@click.option('--task', type=int,
              help='Option to done task. Input index of task')
@click.option('--subtask', type=int, nargs=2,
              help='Option to done subtask. Input index of task and then subtask')
def done(task, subtask):
    """
    Done subtask or task by inputing index of task
    """
    try:
        if task:
            task_manager_library.done_task(task)
        elif subtask:
            task_manager_library.done_subtask(subtask[0], subtask[1])
    except Exception as e:
        print(e)
        logging.warning("Troubles while trying to done task")


@cli.command()
@click.option('--task', type=(int, str),
              help='Опция для редактирования задач')
def edit(task):
    try:
        if task:
            task_num = task[0]
            task_field = task[1]
            task_manager_library.edit_task(task_num, task_field)
    except ValueError as e:
        print(e)


@cli.command()
@click.option('--level', type=str,
              help='Выбрать уровень логгирования')
@click.option('--file', type=str,
              help='Указать файл с логгированием')
@click.option('--format', type=str,
              help='Формат логгирования')
def logging(level, file, format):
    Console.set_logger(level, format, file)


# endregion


if __name__ == '__main__':
    cli()

