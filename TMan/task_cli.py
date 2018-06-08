"""
This module is entry point of console application.

It collects data and prepare for future usage by using actions module.

This app using click module for developing CLI interface. Whole app divided into categories (groups)
for better understanding.

For more information of app usage use help: tman [options] [commands] ... [options] --help
"""
import click
import os

import config
from task_manager_library import actions
from task_manager_library.data_storage import DataStorage
from task_manager_library.models.task_model import Status, Priority, Task, Tag
from user_actions import UserTools
from utility import console_utils
from utility import logging_utils
from utility import serialization_utils
from utility import utils


@click.group(invoke_without_command=True)
def cli():
    """Task Manager (tman) application for managing tasks and events"""
    #click.clear()
    try:
        DataStorage.PATH = config.DATA_PATH
        UserTools.PATH = config.CURRENT_USER_CONFIG
        DataStorage.CURRENT_USER = UserTools.get_current_user()
        actions.get_schedulers()
        notifications = actions.get_notification()

        if notifications is not None:
            console_utils.print_notifications(notifications)

        logging_utils.get_logging_config("DEBUG")
    except ValueError as e:
        print(e)



# region User actions


@cli.group()
def user():
    """User actions and tools"""
    pass


@user.command()
@click.option('--login', type=str,
              help='Login to switch the users')
def change(login):
    """Set user as current (Sign In)"""
    try:
        UserTools.set_current_user(login)
    except Exception as e:
        print(e)


@user.command()
@click.option('--login', type=str, default=None,
              help='Unique login of new user')
@click.option('--name', type=str, default='UserName',
              help='Name of new user')
@click.option('--surname', type=str, default='UserName',
              help='surname of new user')
def add_user(login, name, surname):
    """Add new user"""
    UserTools.add_user(login, name, surname)


@user.command()
def current():
    """Showing current user"""
    try:
        current = UserTools.get_current_user()
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
@click.option('-sd', '--startdate', type=str, callback=utils.check_date, default=None,
              help='Start date')
@click.option('-ed', '--enddate', type=str, callback=utils.check_date, default=None,
              help='End date')
@click.option('-tg', '--tag', type=str,
              help='Tag')
@click.option('-de', '--description', type=str,
              help='Description')
@click.option('-ti', '--title', type=str,
              help='Title')
@click.option('-re', '--reminder', type=str, callback=utils.check_time, default='12:00',
              help='Reminder')
@click.option('-ob', '--observers', type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=str,
              help='Priority')
@click.option('-pa', '--parent', type=str, default=None,
              help='Parent tid')
def add(startdate, enddate, tag, description,
        title, reminder, observers, priority, parent):
    """Adding new task"""
    try:

        if startdate is None or enddate is None:
            raise ValueError("Inpute date")
        actions.add_tracked_task(title, description, startdate, enddate,
                                 tag, observers, reminder, priority, parent)
    except ValueError as e:
        click.echo(e)
    #except Exception as e:
    #    click.echo(e)


@task.command()
def list():
    """Showing list of user's tasks"""
    tasks_list = actions.show_tasks_list()
    console_utils.format_print_tasks(tasks_list)


@task.command()
@click.option('--tid', type=str,
              help='Option to done task. Input tid of task')
@click.option('--status', type=click.Choice(['done', 'undone', 'process']),
              help='Choose task and s')
def status(tid, status):
    """Done by inputing index of task"""
    try:
        status = Status[status]
        if status == Status.done:
            actions.done_task(tid)
        elif status == Status.process:
            actions.begin_task(tid)
        elif status == Status.undone:
            actions.undone_task(tid)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)


@task.command()
@click.option('--tid', type=str,
              help='Option to done task. Input tid of task')
@click.option('--field', type=click.Choice(['title', 'start', 'end', 'desc']),
              help='Choose task and s')
def edit(tid, field):
    """Editing tasks. Choose index and field"""
    try:
        if task:
            task_tid = tid
            task_field = field
            actions.edit_task(task_tid, task_field)
    except ValueError as e:
        print(e)


@task.command()
@click.option('--index', type=int,
              help='Index of task')
@click.option('--tid', type=str,
              help='TID of task')

def show(index, tid):
    """Showing full info about task: choose INDEX or TID"""

    if index:
        task = actions.get_task(index)
    if tid:
        task = actions.get_task_from_id(tid)

    try:
        subtasks = actions.get_subtasks(task.tid)

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
        if task.connection:
            click.secho("\t\t\t\t\t\t\t\t", bold=True, bg='green', fg='white')
            click.echo("Linked tasks:")
            for tid in task.connection:
                connected_task = actions.get_connected_tasks(tid)
                click.secho(connected_task.title, bold=True, bg='green', fg='white')
        if subtasks != []:
            click.echo("Subtasks:")
        for subtask in subtasks:
            click.secho(subtask.title + ' - '+ subtask.tid, fg='white', bold=True, bg='red')
    except IndexError as e:
        click.echo(e)
    except Exception as e:
        click.echo("Something went wrong: {}".format(e))


@task.group()
@click.option('--tag', type=str,
              help="Order by tag")
def orderby(tag):
    """Order tasks by tag"""
    pass

@orderby.command()
@click.argument('name')
def tag(name):
    try:
        tag = Tag(name)
        ordered_tasks = actions.order_tasks(tag)
        click.echo("Ordered by tag:" + click.style(tag.tag_name, bg='red', fg='white'))
        click.echo()
        console_utils.format_print_ordered(ordered_tasks)
    except IndexError as e:
        click.echo(e)
    except Exception as e:
        click.echo(e)


@orderby.command()
@click.argument('name')
def priority(name):
    try:
        priority = Priority[name]
        ordered_tasks = actions.order_by_priority(priority)
        click.echo("Ordered by priority:" + click.style(name, bg='red', fg='white'))
        click.echo()
        console_utils.format_print_ordered(ordered_tasks)
    except IndexError as e:
        click.echo(e)
    except Exception as e:
        click.echo(e)



@task.command()
@click.option('--tid', type=str,
              help='Task ID of deleting task')
def delete_task(tid):
    actions.delete_task(tid)


@task.command()
@click.option('--first', type=str,
              help="First task's tid")
@click.option('--second', type=str,
              help="Second task's tid")
def make_link(first, second):
    """Make link between 2 tasks """
    actions.make_link(first, second)


@task.command()
def archieve():
    """Show list of completed tasks"""
    tasks = actions.show_archieve()
    if tasks is None:
        click.secho("Archieve is empty", bg='red', fg='white')
    click.secho("Archieved tasks:", bg='red', fg='white')

    for task in tasks:
        if task.parent is None:
            click.secho(task.title, bg='green', fg='white')
        else:
            click.echo(click.style(task.title, bg='green', fg='white')
                       + click.style(" ◑ subtask ◑", bg='blue', fg='white'))


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
@click.option('-ob', '--observers', type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=str,
              help='Priority')
def scheduler(startdate, enddate, tag, description,
              title, reminder, observers, priority, interval):
    actions.add_scheduler(title, description, startdate, enddate,
                          tag, observers, reminder, priority, interval)


@util.command()
@click.option('--date', type=str, callback=utils.check_date,
              help='Date')
@click.option('--tid', type=str,
              help='TID of task')
@click.option('--title', type=str,
              help='Title')
def notifications(date, tid, title):
    actions.add_notification(date, tid, title)


# endregion


if __name__ == '__main__':
    cli()






"""

# region Subtask actions

@cli.group()
def subtask():
    Subtask actions and tools
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
@click.option('-ob', '--observers', type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=str,
              help='Priority')
@click.option('-i', '--index', type=int,
              help='Index of task to add subtask')
def add(startdate, enddate, tag, description,
        title, reminder, observers, priority, index):
    Adding new subtask
    tag = Tag(tag)
    actions.add_subtask(index, title, description, startdate, enddate,
                        tag, observers, reminder, priority)
    return True


@subtask.command()
@click.option('--task', type=int,
              help='Index of parent task')
@click.option('--index', type=int,
              help='Option to done task. Input index of task')
@click.option('--field', type=click.Choice(['title', 'start', 'end', 'desc']),
              help='Choose task title, etc.')
def edit(task, index, field):
    Editing tasks. Choose index and field
    try:
        if task:
            task_num = task
            subtask_num = index
            task_field = field
            actions.edit_subtask(task_num, subtask_num, task_field)
    except ValueError as e:
        print(e)


@subtask.command()
@click.option('--task', type=int,
              help='Index of parent task')
@click.option('--index', type=int,
              help='Option to done task. Input index of task')
@click.option('--status', type=click.Choice(['done', 'undone', 'process']),
              help='Choose task and s')
def status(task, index, status):
    Done subtask or task by inputing index of task
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
    Show list of subtasks of chosen task
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
    Showing full info
    parent = DataStorage.get_subtasks_parent(task)
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
            click.secho(connected_task.title, bold=True, bg='green', fg='white')

    click.echo(click.style("#" + task.tag.tag_name, bold=True, bg='red'))


# endregion"""