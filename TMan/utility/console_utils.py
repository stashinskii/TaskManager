import click
import os

from task_manager_library import task_info

STATUS_NAMES = ['done','undone','process']

def open_nano(data, num):
    """
    Open nano editor
    :param data: list of task's title, startdate, enddate and description
    :param num: position in list to be changed
    :return: changed data
    """
    os.system("echo \"{}\" >> {}".format(data[num], "/tmp/tman_tempdata.tmp"))
    os.system("nano {}".format("/tmp/tman_tempdata.tmp"))
    file = open("/tmp/tman_tempdata.tmp")
    data[num] = file.read()[0:-1]
    os.system("rm /tmp/tman_tempdata.tmp")
    return data


def check_status_name(ctx, param, value):
    if value[1] not in STATUS_NAMES:
        raise ValueError("Check status name to be changed")


def format_print_list(tasks):
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