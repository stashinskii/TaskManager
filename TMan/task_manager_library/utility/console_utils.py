"""
Module represents methods required for inputing and outputing data to console interface
"""

import click
import os

from task_manager_library import data_storage
from task_manager_library.models.task_model import Status, Task, Priority

STATUS_NAMES = ['done', 'undone', 'process']


def check_status_name(ctx, param, value):
    """Checking inputing values of status(done, undone, process)"""
    if value[1] not in STATUS_NAMES:
        raise ValueError("Check status name to be changed")


def format_print_tasks(tasks):
    """Printing list of tasks"""
    for task in tasks:
        marker = ' '
        if task[0] == Status.done:
            marker = 'X'
        elif task[0] == Status.undone:
            marker = ' '
        elif task[0] == Status.process:
            marker = 'O'
        else:
            raise ValueError("Status is not status object")

        click.echo("[" + marker + "] - " + str(task[1]) + " - " + click.style(
            "Subtasks: " + str(task[2]), bold=True, fg='yellow')
                   + " - " + click.style(str(task[3]), bold=True, bg='green'))


def format_print_ordered(ordered_tasks):
    """Showing full info of orderedn tasks"""

    for task in ordered_tasks:
        marker = ' '
        if task.is_completed == Status.done:
            marker = 'X'
        elif task.is_completed == Status.undone:
            marker = ' '
        elif task.is_completed == Status.process:
            marker = 'O'
        else:
            raise ValueError("Status is not status object")

        click.echo("[" + marker + "] - "
                   + click.style(task.title, bold=True, bg='yellow', fg='white'))


def print_notifications(notifications):
    """Ptint current notification"""
    click.secho("You have {} reminders for today:".format(len(notifications)),
                bg='yellow', bold=True, fg='white')
    for notify in notifications:
        click.secho(notify.title, bg='green', bold=True, fg='white')
