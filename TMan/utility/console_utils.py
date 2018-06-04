import click
import os


from task_manager_library import task_info
from task_manager_library import data_storage

STATUS_NAMES = ['done','undone','process']




def check_status_name(ctx, param, value):
    if value[1] not in STATUS_NAMES:
        raise ValueError("Check status name to be changed")


def format_print_tasks(tasks):
    """
    Printing list of tasks
    :param tasks: tuple of Status, index, subtasks and title of task
    :return:
    """
    for task in tasks:
        marker = ' '
        if task[0] == task_info.Status.done:
            marker = 'X'
        elif task[0] == task_info.Status.undone:
            marker = ' '
        elif task[0] == task_info.Status.process:
            marker = 'O'
        else:
            raise ValueError("Status is not status object")

        click.echo("[" + marker + "] - " + str(task[1]) + " - " + click.style(
                   "Subtasks: " + str(task[2]), bold=True, fg='yellow')
                   + " - " + click.style(str(task[3]), bold=True, bg='green'))


def format_print_subtasks(tasks, index):
    """
    Printing list of subtasks
    :param tasks: tuple of Status, index, subtasks and title of task
    :return:
    """
    parent = data_storage.DataStorage.get_subtasks_parent(index)

    click.secho("Parent of chosen task (index: {0}) is: {1}".format(index, parent), bg='green', fg='white', blink=True)

    for task in tasks:
        marker = ' '
        if task[0] == task_info.Status.done:
            marker = 'X'
        elif task[0] == task_info.Status.undone:
            marker = ' '
        elif task[0] == task_info.Status.process:
            marker = 'O'
        else:
            raise ValueError("Status is not status object")

        click.echo("[" + marker + "] - " + str(task[1]) + " - "
                   + " - " + click.style(str(task[2]), bold=True, bg='yellow', fg='white'))