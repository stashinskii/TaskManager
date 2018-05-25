from ConsoleLib import *
import os

# Коллекции, хранящие задачи
simple_tasks = []
tracked_tasks = []
calendar_events = []
all_tasks = []
all_users_tasks = []


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
    global simple_tasks, tracked_tasks, calendar_events, current_user, users, all_tasks, all_users_tasks
    try:
        users = Console.import_users()
        if (chuser):
            users = Console.set_current(users, chuser)
        elif (setuser):
            Console.create_new_user(users)
        elif (current):
            Console.show_current(users)
        else:
            (current_user, tracked_tasks,
             calendar_events, all_tasks, all_users_tasks) = Console.import_all_data(users)
            (current_user, tracked_tasks, calendar_events, all_tasks, all_users_tasks) = Console.add_scheduler_task(
                calendar_events, all_tasks, current_user, users)
    except IOError as e:
        pass
    #except Exception as e:
    #    print(e)
    #    logging.warning("Some troubles while open app")
    #    raise click.Abort()


@cli.command()
@click.option('--task', is_flag=True,
              help='Опция для добавления задачи в трекер задач')
@click.option('--subtask', type=int,
              help='Опция для добавления подзадачи')
@click.option('--plan', is_flag=True,
              help='Задать конфигурацию планировщика')
@click.option('-sd', type=str,
              help='Начало')
@click.option('-ed', type=str,
              help='Конец')
@click.option('-tg', type=str,
              help='Тег')
@click.option('-de', type=str,
              help='Описание')
@click.option('-ti', type=str,
              help='Название')
@click.option('-re', type=str,
              help='Название')
@click.option('-ob', type=str,
              help='Наблюдатели')
@click.option('-pr', type=str,
              help='Приоритет')
def add(task, subtask, plan, sd, ed, tg, de, ti, re, ob, pr):
    """Добавление задачи"""
    global tracked_tasks, calendar_events, current_user, users, subtasks, all_users_tasks
    if task:
        tracked_tasks = Console.add_task(current_user, all_tasks, all_users_tasks, users, sd, ed, tg, de, ti, re, ob, pr)
    elif subtask:
        subtasks = Console.add_subtask(current_user, all_tasks, all_users_tasks, tracked_tasks, users, subtask,
                                       sd, ed, tg, de, ti, re, ob, pr)
    elif plan:
        Console.add_scheduler()



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
@click.option('--event', is_flag=True,
              help='Опция для просмотра события в календаре')
def list(task, event):
    """Просмотр всех задач"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        Console.list_task(tracked_tasks, all_tasks)
    elif event:
        pass


@cli.command()
@click.option('--task', type=int,
              help='Опция для выполнения задачи')
@click.option('--subtask', type=int,
              help='Опция для выполнения подзадачи')
def done(task, todo, subtask):
    """Выполнение задачи по номеру"""
    global simple_tasks, tracked_tasks, calendar_events, all_users_tasks, all_tasks
    try:
        if task:
            Console.done_task(task, all_tasks, tracked_tasks, all_users_tasks)
        elif subtask:
            Console.done_subtask(subtask, all_tasks, tracked_tasks, all_users_tasks)

    except Exception as e:
        print(e)
        logging.warning("Troubles while trying to done task")


@cli.command()
@click.option('--task', type=int,
              help='Опция для удаления задачи')
def delete(task):
    """Удаление задачи по номеру"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        pass


@cli.command()
@click.option('--task', type=int,
              help='Опция для просмотра задач')
@click.option('--event', type=int,
              help='Опция для просмотра события в календаре')
def info(task, event):
    """Просмотра подробной информации"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        pass
    elif event:
        pass


@cli.command()
@click.option('--task', type=(int, str),
              help='Опция для редактирования задач')

def edit(task):
    """Просмотра подробной информации"""
    global simple_tasks, tracked_tasks, calendar_events, all_users_tasksm, current_user
    try:
        if task:
            task_num = task[0]
            task_field = task[1]
            Console.edit_task(current_user, task_num, task_field, all_users_tasks, tracked_tasks, all_tasks)

    except ValueError as e:
        print(e)

@cli.command()
@click.option('--tag', type = str)
@click.option('--value', type=click.Choice(['high', 'medium', 'low']))
def showtools(tag, value):
    """Форматированный вывод по заданным критериям"""
    global tracked_tasks, users
    if tag:
        Console.show_by_tag(tag, tracked_tasks)
    elif value:
        priority = TManLibrary.Priority[value]
        Console.show_by_priority(priority, tracked_tasks, users)


if __name__ == '__main__':
    cli()

