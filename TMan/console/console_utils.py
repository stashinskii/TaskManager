"""
Module represents methods required for inputing and outputing data to console interface
"""

import click
import os

from task_manager_library.models.task_model import Status, Task, Priority


def print_tree(manager, tasks):
    """
    Printing task tree. Includes subtasks on their level/ heights
    Use recursive function print_sub
    :param manager: manager (Actions instance) to get required data from storage
    :param tasks: list of user's tasks
    :return:
    """
    click.clear()
    root_tasks = [task for task in tasks if task.parent is None]

    for task in root_tasks:
        marker = get_status_marker(task)
        click.echo(marker + " - " + task.tid + " - " +
                   click.style(str(task.title), fg='yellow'))

        subtasks = manager.get_subtasks(task.tid)

        for subtask in subtasks:
            marker = get_status_marker(subtask)
            print(subtask.height*"\t" + marker + " - " + subtask.tid + " - " +
                  click.style(subtask.title, fg='yellow'))
            print_sub(manager, subtask)


def print_sub(manager, _task):
    """Recursive function for getting tasks"""
    subtasks = manager.get_subtasks(_task.tid)
    for subtask in subtasks:
        marker = get_status_marker(subtask)
        print(subtask.height * "\t" + marker + " - " + subtask.tid +
              " - " + click.style(subtask.title, fg='yellow'))
        print_sub(manager, subtask)


def format_print_info(task, subtasks, manager):
    """
    Printing full information about chosen task
    Use click module to get access to format printing in CLI
    """
    if task.is_completed == Status.done:
        status = "Done"
        color = 'green'
    elif task.is_completed == Status.undone:
        status = "Undone"
        color = 'red'
    elif task.is_completed == Status.process:
        status = "Process"
        color = 'blue'
    click.echo("Title: \t\t" + click.style(str(task.title), bold=True, fg='yellow'))
    click.echo("Description: \t" + click.style(str(task.description), bold=True, fg='yellow'))
    click.echo("Start date: \t" + click.style(str(task.start.date()), bold=True, fg='yellow'))
    click.echo("End date: \t" + click.style(str(task.end.date()), bold=True, fg='yellow'))
    click.echo("Status: \t" + click.style(status, bold=True, fg=color))
    click.echo("tid: \t\t" + click.style(task.tid, bold=True, fg='white'))
    click.echo(click.style("#" + str(task.tag.tag_name), bold=True, bg='red'))
    if task.connection:
        click.secho("\t\t\t\t\t\t\t\t", bold=True, bg='green', fg='white')
        click.echo("Linked tasks:")
        for tid in task.connection:
            connected_task = manager.get_task_by_tid(tid)
            click.secho(connected_task.title, bold=True, bg='green', fg='white')
    if subtasks:
        click.echo("Subtasks:")
    for subtask in subtasks:
        click.secho(subtask.title + ' - ' + subtask.tid, fg='white', bold=True, bg='red')


def get_status_marker(task):
    """Get marker of task's status"""
    if task.is_completed == Status.done:
        marker = click.style('[X]', fg='green')
    elif task.is_completed == Status.undone:
        marker = click.style('[ ]', fg='red')
    else:
        marker = click.style('[O]', fg='blue')
    return marker


def split_str_to_list(splitter):
    """Split string separated by ',' and convert it to list"""
    if splitter == "":
        return []

    splitter = splitter.split(",")
    return splitter


def format_print_ordered(ordered_tasks):
    """Showing full info of ordered tasks"""

    for task in ordered_tasks:
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

