import click
import os

import config
import user_actions
from task_manager_library import actions
from task_manager_library import data_storage
from task_manager_library.models.task_model import Status, Priority, Task, Tag
from utility import console_utils
from utility import logging_utils
from utility import serialization_utils
from utility import utils


@click.group(invoke_without_command=True)
def cli():
    """Task Manager (tman) application for managing tasks and events"""
    try:
        data_storage.DataStorage.PATH = config.DATA_PATH
        user_actions.UserTools.PATH = config.CURRENT_USER_CONFIG
        data_storage.DataStorage.CURRENT_USER = user_actions.UserTools.get_current_user()
        actions.get_schedulers()
        logging_utils.get_logging_config("DEBUG")
    except Exception as e:
        print(e)
    click.clear()

# region User actions


@cli.group()
def user():
    """User actions and tools"""
    pass


@user.command()
@click.option('--login', type=str,
              help='Login to switch the users')
def change_user(login):
    """
    Set user as current
    """
    try:
        user_actions.UserTools.set_current_user(login)
    except Exception as e:
        click.secho(e, fg="red")


@user.command()
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
    user_actions.UserTools.add_user(login, name, surname)


@user.command()
def current():
    """
    Set current user
    """
    try:
        current = user_actions.UserTools.get_current_user()
        click.echo("Login: {}".format(current.login))
        click.echo("Full name: {} {}".format(current.name, current.surname))
        click.echo("UID: {}".format(current.uid))
    except Exception as e:
        print(e)

# endregion

# region Task actions

@cli.group()
def task():
    """Task actions and tools"""
    pass


@task.command()
@click.option('-sd', '--startdate', type=str, callback=utils.check_date,
              help='Start date')
@click.option('-ed', '--enddate', type=str, callback=utils.check_date,
              help='End date')
@click.option('-tg', '--tag', type=str,
              help='Tag')
@click.option('-de', '--description', type=str,
              help='Description')
@click.option('-ti', '--title', type=str,
              help='Title')
@click.option('-re', '--reminder', type=str, callback=utils.check_time,
              help='Reminder')
@click.option('-ob', '--observers',  type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=str,
              help='Priority')
def add(startdate, enddate, tag, description,
        title, reminder, observers, priority):
    """Adding new task"""
    tag = Tag(tag)
    actions.add_tracked_task(title, description, startdate, enddate,
                             tag, observers, reminder, priority)
    return True


@task.command()
def list():
    """
    Showing list of current tasks
    """
    tasks_list = actions.show_tasks_list()
    console_utils.format_print_tasks(tasks_list)


@task.command()
@click.option('--index', type=int,
              help='Option to done task. Input index of task')
@click.option('--status', type=click.Choice(['done', 'undone', 'process']),
              help='Choose task and s')
def status(index, status):
    """
    Done subtask or task by inputing index of task
    """
    try:
        status = Status[status]
        if status == Status.done:
            actions.done_task(index)
        elif status == Status.process:
            actions.begin_task(index)
        elif status == Status.undone:
            actions.undone_task(index)

    except ValueError as e:
        print(e)
    except Exception as e:
       print(e)


@task.command()
@click.option('--index', type=int,
              help='Option to done task. Input index of task')
@click.option('--field', type=click.Choice(['title', 'start', 'end', 'desc']),
              help='Choose task and s')
def edit(index, field):
    """
    Editing tasks
    """
    try:
        if task:
            task_num = index
            task_field = field
            actions.edit_task(task_num, task_field)
    except ValueError as e:
        print(e)


@task.command()
@click.option('--index', type=int,
              help='Index of task')
def show(index):
    task = actions.get_task(index)
    if task.is_completed == Status.done:
        status = "Done"
        color = 'green'
    elif task.is_completed == Status.undone:
        status = "Undone"
        color = 'red'
    elif task.is_completed == Status.process:
        status = "Process"
        color = 'blue'
    click.echo("Title: \t\t" + click.style(task.title, bold=True, fg='yellow'))
    click.echo("Description: \t" + click.style(task.description, bold=True, fg='yellow'))
    click.echo("Start date: \t" + click.style(str(task.start.date()), bold=True, fg='yellow'))
    click.echo("End date: \t" + click.style(str(task.end.date()), bold=True, fg='yellow'))
    click.echo("Status: \t" + click.style(status, bold=True, fg=color))
    click.echo("tid: \t\t" + click.style(task.tid, bold=True, fg='white'))
    click.echo(click.style("#" + task.tag.tag_name, bold=True, bg='red'))
    if task.connection is not None:
        click.secho("\t\t\t\t\t\t\t\t", bold=True, bg='green', fg='white')
        click.echo("Linked tasks:")
        for tid in task.connection:
            connected_task = actions.get_connected_tasks(tid)
            click.secho(connected_task.title, bold=True, bg = 'green', fg='white')


@task.command()
@click.option('--tag', type=str,
              help="Order by tag")
def orderby(tag):
    tag = Tag(tag)
    ordered_tasks = actions.order_tasks(tag)
    console_utils.format_print_ordered(ordered_tasks)

@task.command()
@click.option('--first', type=str,
              help="First task's tid")
@click.option('--second', type=str,
              help="Second task's tid")
def make_link(first, second):
    actions.make_link(first, second)


# endregion

# region Subtask actions

@cli.group()
def subtask():
    """Subtask actions and tools"""
    pass


@subtask.command()
@click.option('-sd', '--startdate', type=str, callback=utils.check_date,
              help='Start date')
@click.option('-ed', '--enddate', type=str, callback=utils.check_date,
              help='End date')
@click.option('-tg', '--tag', type=str,
              help='Tag')
@click.option('-de', '--description', type=str,
              help='Description')
@click.option('-ti', '--title', type=str,
              help='Title')
@click.option('-re', '--reminder', type=str, callback=utils.check_time,
              help='Reminder')
@click.option('-ob', '--observers',  type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=str,
              help='Priority')
@click.option('-i', '--index', type=int,
              help='Index of task to add subtask')
def add(startdate, enddate, tag, description,
        title, reminder, observers, priority, index):
    """Adding new subtask"""
    tag = Tag(tag)
    actions.add_subtask(index, title, description, startdate, enddate,
                        tag, observers, reminder, priority)
    return True


@subtask.command()
@click.option('--task', type=int,
              help='Index of parent task')
@click.option('--index', type=int,
              help='Option to done task. Input index of task')
@click.option('--status', type=click.Choice(['done', 'undone', 'process']),
              help='Choose task and s')
def status(task, index, status):
    """
    Done subtask or task by inputing index of task
    """
    try:
        status = Status[status]
        if status == Status.done:
            actions.done_subtask(task, index)
        elif status == Status.process:
            actions.begin_subtask(task, index)
        elif status == Status.undone:
            actions.undone_subtask(task, index)

    except ValueError as e:
        print(e)
    except Exception as e:
       print(e)


@subtask.command()
@click.option('--index', type=int,
              help='Index of task')
def list(index):
    try:
        if index is None:
            raise ValueError("Select index")
        tasks_list = actions.show_subtasks_list(index)
        console_utils.format_print_subtasks(tasks_list, index)
    except ValueError as e:
        print (e)
    except Exception as e:
        print (e)



@subtask.command()
@click.option('--task', type=int,
              help='Index of task')
@click.option('--index', type=int,
              help='Index of subtask')
def show(task, index):
    parent = data_storage.DataStorage.get_subtasks_parent(task)
    click.secho("Parent task of chosen subtask is: {}".format(parent), bg='green', fg='white')
    task = actions.get_subtask(task, index)
    if task.is_completed == Status.done:
        status = "Done"
        color = 'green'
    elif task.is_completed == Status.undone:
        status = "Undone"
        color = 'red'
    elif task.is_completed == Status.process:
        status = "Process"
        color = 'blue'
    click.echo("Title: \t\t" + click.style(task.title, bold=True, fg='yellow'))
    click.echo("Description: \t" + click.style(task.description, bold=True, fg='yellow'))
    click.echo("Start date: \t" + click.style(str(task.start.date()), bold=True, fg='yellow'))
    click.echo("End date: \t" + click.style(str(task.end.date()), bold=True, fg='yellow'))
    click.echo("Status: \t" + click.style(status, bold=True, fg=color))
    click.echo("tid: \t\t" + click.style(task.tid, bold=True, fg='white'))
    if task.connection is not None:
        click.echo("Linked tasks:")
        for task in task.connection:
            connected_task = actions.get_connected_tasks(task)
            click.secho(connected_task.title, bold=True, bg = 'green', fg='white')

    click.echo(click.style("#" + task.tag.tag_name, bold=True, bg='red'))

# endregion

# region Sheduler actions
@cli.group()
def util():
    """Utils actions and tools"""
    pass


@util.command()
@click.option('-in', '--interval', type=int,
              help='Interval')
@click.option('-sd', '--startdate', type=str, callback=utils.check_date,
              help='Start date')
@click.option('-ed', '--enddate', type=str,callback=utils.check_date,
              help='End date')
@click.option('-tg', '--tag', type=str,
              help='Tag')
@click.option('-de', '--description', type=str,
              help='Description')
@click.option('-ti', '--title', type=str,
              help='Title')
@click.option('-re', '--reminder', type=str,callback=utils.check_time,
              help='Reminder')
@click.option('-ob', '--observers',  type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=str,
              help='Priority')
def scheduler(startdate, enddate, tag, description,
              title, reminder, observers, priority, interval):

    actions.add_scheduler(title, description, startdate, enddate,
                          tag, observers, reminder, priority, interval)




# endregion


if __name__ == '__main__':
    cli()

