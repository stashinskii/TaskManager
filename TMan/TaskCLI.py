from ConsoleLib import *
import DeamonLib

# Коллекции, хранящие задачи
simple_tasks = []
tracked_tasks = []
calendar_events = []
all_tasks = []


users = []
current_user = None


@click.group(invoke_without_command=True)
@click.option('--chuser', type=str,
              help='Смена пользователя')
@click.option('--setuser', is_flag=True,
              help='Добавить пользователя')
@click.option('--current', is_flag=True,
              help='Просмотеть текущего полльзователя')
def cli(chuser, setuser, current):
    click.clear()
    global simple_tasks, tracked_tasks, calendar_events, current_user, users, all_tasks
    try:
        users = Console.import_users()
        if (chuser):
            users = Console.set_current(users, chuser)
        elif (setuser):
            Console.create_new_user(users)
        elif (current):
            Console.show_current(users)
        else:
            (current_user, simple_tasks, tracked_tasks, calendar_events, all_tasks) = Console.import_all_data(users)
            (current_user, simple_tasks, tracked_tasks, calendar_events, all_tasks) = Console.add_scheduler_task(
                calendar_events, all_tasks, current_user, simple_tasks, users)
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
@click.option('--plan', is_flag=True,
              help='Задать конфигурацию планировщика')
@click.option('--todo', is_flag=True,
              help='Опция для добавления в todo')
def add(task, subtask, todo, plan):
    """Добавление задачи"""
    global simple_tasks, tracked_tasks, calendar_events, current_user, users, subtasks

    if task:
        tracked_tasks = Console.add_task(current_user, all_tasks, users, simple_tasks)
    elif subtask:
        subtasks = Console.add_subtask(current_user, all_tasks, tracked_tasks, users, subtask)
    elif plan:
        Console.add_scheduler()
    elif todo:
        simple_tasks = Console.add_simple_task(users, current_user, simple_tasks)


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
        Console.list_task(tracked_tasks, all_tasks)
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
    global simple_tasks, tracked_tasks, calendar_events
    try:
        if task:
            Console.done_task(task, all_tasks, tracked_tasks)
        elif todo:
            Console.done_todo(todo, simple_tasks)
        elif subtask:
            Console.done_subtask(subtask, all_tasks, tracked_tasks)

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
@click.option('--task', type=(int, str),
              help='Опция для редактирования задач')
@click.option('--todo', type=int,
              help='Опция для редактирования todo')
@click.option('--event', type=int,
              help='Опция для редактирования события в календаре')
def edit(task, todo, event):
    """Просмотра подробной информации"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        task_num = task[0]
        task_field = task[1]
        Console.edit_task(task_num, task_field, tracked_tasks, simple_tasks, all_tasks)
    elif todo:
        Console.edit_task(todo, simple_tasks)
    elif event:
        pass


if __name__ == '__main__':
    cli()

