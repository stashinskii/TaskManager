from ConsoleLib import *
import DeamonLib

# Коллекции, хранящие задачи
simple_tasks = []
tracked_tasks = []
calendar_events = []
subtasks = []


users = []
current_user = None


@click.group(invoke_without_command=True)
@click.option('--chuser', type=str,
              help='Смена пользователя')
@click.option('--setuser', is_flag=True,
              help='Добавить пользователя')
@click.option('--current', is_flag=True,
              help='Просмотеть текущего полльзователя')
@click.option('--off', is_flag=True,
              help='Отключить напоминания')

def cli(chuser, setuser, current, off):
    check_reminds = DeamonLib.TManReminder('/tmp/daemon-reminders.pid')

    global simple_tasks, tracked_tasks, calendar_events, current_user, users, subtasks
    click.clear()
    try:
        users = Console.import_users()
        if (chuser):
            users = Console.set_current(users, chuser)
        elif (setuser):
            Console.create_new_user(users)
        elif (current):
            Console.show_current(users)
        elif (off):
            check_reminds.stop()
        else:
            (current_user, simple_tasks, tracked_tasks, subtasks, calendar_events) = Console.import_all_data(users)
        """
        
        with open('/tmp/tman_reminder.tmp', 'r'):
            if not off:
                check_reminds.start()
        
        """
    except IOError as e:
        pass
    except Exception as e:
        print(e)
        logging.warning("Some troubles while open app")
        raise click.Abort()


@cli.command()
@click.option('--task', is_flag=True,
              help='Опция для добавления задачи в трекер задач')
@click.option('--subtask', type=int,
              help='Опция для добавления подзадачи')
@click.option('--todo', is_flag=True,
              help='Опция для добавления в todo')
@click.option('--event', is_flag=True,
              help='Опция для добавления события в календарь')
def add(task, subtask, todo, event):
    """Добавление задачи"""
    global simple_tasks, tracked_tasks, calendar_events, current_user, users, subtasks

    if task:
        tracked_tasks = Console.add_task(current_user,tracked_tasks, users, simple_tasks)
    elif subtask:
        subtasks = Console.add_subtask(current_user, subtasks, tracked_tasks, subtask)
    elif todo:
        simple_tasks = Console.add_simple_task(users, current_user, simple_tasks)
    else:
        print("event")


@cli.command()
@click.option('--week', is_flag=True,
              help='Опция для просмотра задач')
@click.option('--month', is_flag=True,
              help='Опция для просмотра todo')
def cal(week, month):
    """Работа с календарем"""
    global simple_tasks, tracked_tasks, calendar_events
    if week:
        Console.show_week(calendar_events)
    elif month:
        pass


@cli.command()
@click.option('--task', is_flag=True,
              help='Опция для просмотра задач')
@click.option('--todo', is_flag=True,
              help='Опция для просмотра todo')
@click.option('--event', is_flag=True,
              help='Опция для просмотра события в календаре')
def list(task, todo, event):
    """Просмотр всех задач"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        Console.list_task(tracked_tasks)
    elif todo:
        Console.list_todo(simple_tasks)
    elif event:
        pass


@cli.command()
@click.option('--task', type=int,
              help='Опция для выполнения задачи')
@click.option('--todo', type=int,
              help='Опция для выполнения todo')
@click.option('--subtask', type=int,
              help='Опция для выполнения подзадачи')
def done(task, todo, subtask):
    """Выполнение задачи по номеру"""
    global simple_tasks, tracked_tasks, calendar_events, subtasks
    try:
        if task:
            Console.done_task(task, subtasks, tracked_tasks)
        elif todo:
            Console.done_todo(todo, simple_tasks)
        elif subtask:
            Console.done_subtask(subtask, subtasks, tracked_tasks)

    except Exception as e:
        print(e)
        logging.warning("Troubles while trying to done task")


@cli.command()
@click.option('--task', type=int,
              help='Опция для удаления задачи')
@click.option('--todo', type=int,
              help='Опция для удаления todo')
@click.option('--event', type=int,
              help='Опция для удаления события')
def delete(task, todo, event):
    """Удаление задачи по номеру"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        pass
    elif todo:
        Console.delete_todo(todo, simple_tasks, tracked_tasks)


@cli.command()
@click.option('--task', type=int,
              help='Опция для просмотра задач')
@click.option('--todo', type=int,
              help='Опция для просмотра todo')
@click.option('--event', type=int,
              help='Опция для просмотра события в календаре')
def info(task, todo, event):
    """Просмотра подробной информации"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        pass
    elif todo:
        Console.info_todo(todo, simple_tasks)
    elif event:
        pass


@cli.command()
@click.option('--task', type=int,
              help='Опция для редактирования задач')
@click.option('--todo', type=int,
              help='Опция для редактирования todo')
@click.option('--event', type=int,
              help='Опция для редактирования события в календаре')
def edit(task, todo, event):
    """Просмотра подробной информации"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        Console.edit_task(task, tracked_tasks, simple_tasks)
    elif todo:
        Console.edit_task(todo, simple_tasks)
    elif event:
        pass


if __name__ == '__main__':
    cli()

