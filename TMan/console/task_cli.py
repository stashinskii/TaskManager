import click
import os
from datetime import datetime

import config
from console import console_utils
from console.actions import Actions
from task_manager_library.models.task_model import Status, Priority, Task, Tag


@click.group(invoke_without_command=True)
def cli():
    """Task Manager (tman) application for managing tasks and events"""
    try:
        manager = Actions()
        manager.get_schedulers()
    except Exception as e:
        click.echo(e)


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
        manager = Actions()
        manager.change_user(login)
    except Exception as e:
        print(e)


@user.command()
@click.option('--login', type=str, default=None,
              help='Unique login of new user')
@click.option('--name', type=str, default='UserName',
              help='Name of new user')
@click.option('--surname', type=str, default='UserName',
              help='Surname of new user')
def add_user(login, name, surname):
    """Add new user"""
    manager = Actions()
    manager.add_new_user(login, name, surname)


@user.command()
def current():
    """Showing current user"""
    try:
        manager = Actions()
        current = manager.task_storage.load_user(manager.task_storage.current_uid)
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
@click.option('-sd', '--startdate', type=str,  default=None,
              help='Start date. Format YYYY-MM-DD')
@click.option('-ed', '--enddate', type=str, default=None,
              help='End date. Format YYYY-MM-DD')
@click.option('-tg', '--tag', type=str,
              help='Tag')
@click.option('-de', '--description', type=str,default="",
              help='Description')
@click.option('-ti', '--title', type=str,
              help='Title')
@click.option('-re', '--reminder', type=str,  default='12: 00',
              help='Reminder. Format "HH:MM"')
@click.option('-ob', '--observers', type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=click.Choice(['high', 'low', 'meduim']), default='high',
              help='Priority')
@click.option('-pa', '--parent', type=str, default=None,
              help='Parent tid for creating subtask')
def add(startdate, enddate, tag, description,
        title, reminder, observers, priority, parent):
    """Adding new task"""
    try:
        observers = console_utils.split_str_to_list(observers)
        priority = Priority[priority]
        tag = Tag(tag)
        manager = Actions()
        manager.add_task(title,
                         datetime.strptime(startdate, "%Y-%m-%d"),
                         datetime.strptime(enddate, "%Y-%m-%d"),
                         tag=tag,
                         description=description,
                         observers=observers,
                         reminder=datetime.strptime(reminder, "%H:%M"),
                         priority=priority,
                         parent=parent)
    except ValueError as e:
        click.echo("ValueError:"+str(e))

    except Exception as e:
        click.echo("Exception:" + str(e))


@task.command()
def list():
    """Showing list of user's tasks"""
    manager = Actions()
    tasks_list = manager.get_tasks_list()
    console_utils.print_tree(manager, tasks_list)


@task.command()
@click.option('--tid', type=str,
              help='TID (task ID) of task to be changed')
@click.option('--status', type=click.Choice(['done', 'undone', 'process']),
              help='Status of task to be changed')
def status(tid, status):
    """Change status of task: done, undone, process. Required data: TID, status name"""
    try:
        manager = Actions()
        status = Status[status]

        if status == Status.done:
            manager.complete_task(tid)
        elif status == Status.process:
            manager.begin_task(tid)
        elif status == Status.undone:
            manager.uncomplete_task(tid)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)


@task.command()
@click.option('--observer', type=str,
              help='User to share with')
@click.option('--tid', type=str,
              help='TID of chosen task')
def share(observer, tid):
    """Share task with other users"""
    try:
        manager = Actions()
        manager.share_task(observer, tid)
    except Exception as e:
        click.echo(e)


@task.command()
@click.option('--tid', type=str, default=None,
              help='TID (task ID) of chosen task')
@click.option('--description', type=str, default=None,
              help='Description')
@click.option('--tag', type=str, default=None,
              help='tag')
@click.option('--title', type=str, default=None,
              help='Title')
@click.option('--priority', type=str, default=None,
              help='Priority')
@click.option('--end', type=str, default=None,
              help='End date')
def edit(tid, tag, description, title, priority, end):
    """Editing tasks. Choose index and field"""
    try:
        manager = Actions()
        if tid is None:
            raise ValueError("Input tid!")
        manager.edit_task(tid,
                          title=title,
                          tag=tag,
                          priority=priority,
                          description=description,
                          end=end)
    except Exception as e:
        click.echo(e)


@task.command()
@click.option('--tid', type=str,
              help='TID (task ID) of task')
def show(tid):
    """Showing full info about task: choose INDEX or TID"""

    try:
        manager = Actions()
        task = manager.get_task_by_tid(tid)
        subtasks = manager.get_subtasks(tid)
        console_utils.format_print_info(task, subtasks, manager)

    except IndexError as e:
        click.echo("IndexError: "+e)
    except Exception as e:
        click.echo("Something went wrong: {}".format(e))


@task.group()
def orderby():
    """Order tasks by tag or priority"""
    pass


@orderby.command()
@click.argument('name')
def tag(name):
    """Ordering task by tag"""
    try:
        manager = Actions()
        ordered_tasks = manager.order_by_tag(name)
        click.echo("Ordered by tag:" + name)
        click.echo()
        console_utils.format_print_ordered(ordered_tasks)
    except IndexError as e:
        click.echo(e)
    except Exception as e:
        click.echo(e)


@orderby.command()
@click.argument('name', default="high")
def priority(name):
    """Ordering task by priority"""
    try:
        manager = Actions()
        priority = Priority[name]
        ordered_tasks = manager.order_by_priority(priority)
        click.echo("Ordered by priority:" + click.style(name, bg='red', fg='white'))
        click.echo()
        console_utils.format_print_ordered(ordered_tasks)
    except IndexError as e:
        click.echo("IndexError: "+e)
    except Exception as e:
        click.echo(e)


@task.command()
@click.option('--tid', type=str,
              help='Task ID of chosen task')
def delete_task(tid):
    """Deleting task"""
    manager = Actions()
    manager.delete_task(tid)


@task.command()
@click.option('--first', type=str,
              help="First task's tid")
@click.option('--second', type=str,
              help="Second task's tid")
def make_link(first, second):
    """Make link between 2 tasks """
    manager = Actions()
    manager.make_link(first, second)


@task.command()
@click.option('--sid', type=str,
              help='Scheduler ID')
def planned(sid):
    """Show list of completed tasks"""
    manager = Actions()
    tasks = manager.get_planned_list(sid)
    if not tasks:
        click.echo("No tasks with such sid")
        return
    click.secho("Scheduler ID: " + sid, fg='yellow')
    for task in tasks:
        click.echo(task.tid + " - "  + task.title)



@task.command()
def archieve():
    """Show list of completed tasks"""
    manager = Actions()
    archieved_tasks = manager.get_archieve()
    if archieved_tasks is None:
        click.secho("Archieve is empty", bg='red', fg='white')
        return

    console_utils.print_tree(manager, archieved_tasks)


# endregion

# region Sheduler actions
@cli.group()
def util():
    """Utils actions and tools"""
    pass


@util.command()
@click.option('-sd', '--startdate', type=str,  default=None,
              help='Start date. Format YYYY-MM-DD')
@click.option('-ed', '--enddate', type=str, default=None,
              help='End date. Format YYYY-MM-DD')
@click.option('-tg', '--tag', type=str, default="-",
              help='Tag')
@click.option('-de', '--description', type=str,default="",
              help='Description')
@click.option('-ti', '--title', type=str,
              help='Title')
@click.option('-re', '--reminder', type=str,  default='12: 00',
              help='Reminder. Format "HH:MM"')
@click.option('-ob', '--observers', type=str, default='',
              help='Observers')
@click.option('-pr', '--priority', type=click.Choice(['high', 'low', 'meduim']), default='high',
              help='Priority')
@click.option('-in', '--interval', type=int, default=1,
              help='Interval')
def scheduler(startdate, enddate, tag, description,
              title, reminder, observers, priority, interval):
    """Crating new scheduler for task"""
    observers = console_utils.split_str_to_list(observers)
    priority = Priority[priority]
    tag = Tag(tag)
    manager = Actions()
    manager.add_scheduler(title,
                          datetime.strptime(startdate, "%Y-%m-%d"),
                          datetime.strptime(enddate, "%Y-%m-%d"),
                          interval,
                          tag=tag,
                          description=description,
                          observers=observers,
                          reminder=datetime.strptime(reminder, "%H:%M"),
                          priority=priority)


@util.command()
def plans():
    manager = Actions()
    schedulers = manager.get_schedulers()
    for scheduler in schedulers:
        click.echo("Scheduler ID(sid): "+
                   scheduler.sid +
                   click.style("\nTask title: " + scheduler.task.title +"\n\n", fg='white', bold=True))


@util.command()
@click.option('--sid', type=str,
              help='Scheduler ID')
@click.option('--title', type=str,
              help='New task title')
@click.option('--interval', type=str,
              help='New interval of plan scheduler')
def edit(sid, title, interval):
    manager = Actions()
    manager.edit_scheduler(sid, title=title, interval=interval)


# endregion


if __name__ == '__main__':
    cli()
