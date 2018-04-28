import click
import logging
import DataLib
import UserLib
import TaskLib


# Коллекции, хранящие задачи
simple_tasks = []
tracked_tasks = []
calendar_events = []


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
    global simple_tasks, tracked_tasks, calendar_events, current_user
    click.clear()
    try:
        users = DataLib.data_from_json("User")
        if (chuser):
            users = UserLib.change_user(users, chuser)
        elif (setuser):
            login = input("Login: ")
            if (UserLib.validate_login(users, login)):
                name = input("Name: ")
                surname = input("Surname: ")
                users = UserLib.add_user(users, name, surname, login)
        elif (current):
            current_user = UserLib.set_current(users)
            print("login: {}\nUID: {}".format(current_user.login, current_user.uid))
        else:
            simple_tasks = DataLib.data_from_json("TODO")
            tracked_tasks = DataLib.data_from_json("Task")
            current_user = UserLib.set_current(users)

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
    global simple_tasks, tracked_tasks, calendar_events, current_user

    if task:
        try:
            if current_user is None:
                raise Exception("There is no current user. Choose")
            title = input("Input title: ")
            start = input("Choose start date: ")
            end = input("Choose end date: ")
            description = input("Add some info about task: ")
            dash = input("Choose dashboard: ")
            tag = input("Add #tag to this task: ")
            observers = None  # TODO здесь указать объект пользователя в системе или его uid
            executor = None  # TODO здесь указать объект пользователя в системе или его uid
            priority = input("Choose priority: ")
            author = current_user.uid
            reminder = input("Reminder: ")
            tid = DataLib.tid_gen()

            tracked_tasks = DataLib.add_tracked_task(
                tracked_tasks, tid, title, description, start,
                end, tag, dash, author, observers, executor, True, False, reminder, priority, [])
        except ValueError:
            logging.warning("ValueError: some troubles while adding task")
    elif subtask:
        title = input("Input title: ")
        start = input("Choose start date: ")
        end = input("Choose end date: ")
        description = input("Add some info about task: ")
        dash = input("Choose dashboard: ")
        tag = input("Add #tag to this task: ")
        observers = None  # TODO здесь указать объект пользователя в системе или его uid
        executor = None  # TODO здесь указать объект пользователя в системе или его uid
        priority = input("Choose priority: ")
        author = current_user.uid
        reminder = input("Reminder: ")
        tracked_tasks = DataLib.add_subtask(tracked_tasks, subtask, title, description, start,
                end, tag, dash, author, observers, executor, True, False, reminder, priority)
    elif todo:
        try:
            title = input("Input title: ")
            date = input("Choose date (YYYY-MM-DD): ")
            #year, month, day = map(int, date.split('-'))
            #date = datetime.date(year, month, day)
            description = input("Add some info about task: ")
            priority = input("Choose priority: ")
            tag = input("Add #tag to this task: ")
            tid = DataLib.tid_gen()
            permission = None
            is_completed = False
            simple_tasks = DataLib.add_simple_task(simple_tasks, title, date,
                                                   description, priority, tid, permission, is_completed, tag)
        except TypeError as e:
            logging.warning("Trouble while input data at todo")
            print("Trouble while input data at todo")
        except Exception as e:
            print(e)
    else:
        print("event")


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
        task_gen = DataLib.show_tracked_task(tracked_tasks)
        for task in task_gen:
            print(task)
    elif todo:
        task_gen = DataLib.show_simple_task(simple_tasks)
        for task in task_gen:
            print(task)
    elif event:
        pass


@cli.command()
@click.option('--task', type=int,
              help='Опция для выполнения задачи')
@click.option('--todo', type=int,
              help='Опция для выполнения todo')
def done(task, todo):
    """Выполнение задачи по номеру"""
    global simple_tasks, tracked_tasks, calendar_events
    if task:
        pass
    elif todo:
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError("Выход за границы списка")
            simple_tasks = DataLib.complete_simple_task(simple_tasks, todo)
        except IndexError as e:
            logging.warning("Out of range")
            print(e)


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
        try:
            if (delete - 1) > len(simple_tasks):
                raise IndexError
            simple_tasks = DataLib.delete_simple_task(simple_tasks, delete)
        except IndexError as e:
            logging.warning("Out of range while deleting. Index was: {}".format(delete))
            print(e)
        except Exception as e:
            print(e)
            logging.warning("Something done wrong while deleting. Index was: {}".format(delete))


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
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError("Такой задачи не существует. Выход за границы списка")
            selected_task = DataLib.show_simple_info(simple_tasks, todo)
            click.echo(click.style("TODO Task description: \t\t\t", bold=True, blink=True, bg='green'))
            click.echo("Title: "+click.style(str('\t\t' + selected_task.title), fg='white', bold=True))
            click.echo("Description: " + click.style(str('\t' + selected_task.description), fg='yellow'))
            click.echo("Date: " + click.style(str('\t\t' + selected_task.date), fg='yellow'))
            click.echo("Tag: " + click.style(str('\t\t' + selected_task.tag), fg='yellow'))
            click.echo("Is completed: " + click.style('\t' + str(selected_task.is_completed), fg='yellow'))
        except IndexError as e:
            logging.warning("Out of range while showing todo task info. Index was: {}".format(todo))
            print(e)
    elif event:
        pass


class pcolors:
    """Палитра цветов для форматированного вывода"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# TODO переделать вывод через click.echo


def formatprint(title, value, type):
    """Форматированный вывод с подсветкой информации о задаче"""
    print(title + type+ "\033[1m"+ value + pcolors.ENDC)


if __name__ == '__main__':
    cli()

