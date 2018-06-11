"""
Module represents methods required for inputing and outputing data to console interface
"""

import click
import os

from task_manager_library.models.task_model import Status, Task, Priority


def format_print_tasks(tasks):
    """Printing list of tasks"""
    click.secho("User tasks:", bg='green', fg='white')
    for task in tasks:
        if task.is_completed == Status.done:
            marker = 'X'
        elif task.is_completed == Status.undone:
            marker = ' '
        elif task.is_completed == Status.process:
            marker = 'O'
        else:
            raise ValueError("Status is not status object")
        click.echo("[" + marker + "] - " + "TID:" +str(task.tid) + " - "+str(task.title))


def split_str_to_list(splitter):
    """
    Split string separated by ',' and convert it to list
    """
    if splitter == "":
        return []

    splitter = splitter.split(",")
    return splitter


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
                   + click.style(str(task.title), bold=True, bg='yellow', fg='white'))


def print_notifications(notifications):
    """Ptint current notification"""
    click.secho("You have {} reminders for today:".format(len(notifications)),
                bg='yellow', bold=True, fg='white')
    for notify in notifications:
        click.secho(notify.title, bg='green', bold=True, fg='white')
