import click
import logging
import os
import TManLibrary


data_dir = '/home/herman/Рабочий стол/TaskTracker/taskmanager/TMan/TaskData'

class Console:
    """Класс для организации работы с терминалом."""

    @staticmethod
    def create_new_user(users):
        login = input("Login: ")
        if (TManLibrary.validate_login(users, login)):
            name = input("Name: ")
            surname = input("Surname: ")
            TManLibrary.add_user(users, name, surname, login, {"simple": [], "task": [], "event": []})

    @staticmethod
    def import_users():
        return TManLibrary.data_from_json("User", None)

    @staticmethod
    def set_current(users, chuser):
        return TManLibrary.change_user(users, chuser)

    @staticmethod
    def show_current(users):
        current_user = TManLibrary.set_current(users)
        print("login: {}\nUID: {}".format(current_user.login, current_user.uid))

    @staticmethod
    def import_all_data(users):
        current_user = TManLibrary.set_current(users)
        simple_tasks = TManLibrary.data_from_json("TODO", current_user)
        tracked_tasks = TManLibrary.data_from_json("Task", current_user)
        subtasks = TManLibrary.data_from_json("Subtask", current_user)
        return (current_user, simple_tasks, tracked_tasks, subtasks)

    @staticmethod
    def add_task(current_user, tracked_tasks, users, simple_tasks):
        """
        Добавление новой задачи трекера. Возвращает измененную коллекцию с новым элементом
        """
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
            tid = TManLibrary.tid_gen()

            if click.confirm('Canel sync w/ TODO list and events in calendar?', default=True):
                cancel_sync = True
            else:
                cancel_sync = False

            return TManLibrary.add_tracked_task(
                tracked_tasks, simple_tasks, tid, title, description, start,
                end, tag, dash, author, observers, executor, cancel_sync, False, reminder, priority, [], users, current_user)
        except ValueError:
            logging.warning("ValueError: some troubles while adding task")

    @staticmethod
    def add_subtask(current_user, subtasks, tracked_tasks, subtask):

        """subtask -  параметр Click, номер подзадачи"""

        title = input("Input title: ")
        start = input("Choose start date: ")
        end = input("Choose end date: ")
        description = input("Add some info about task: ")
        tid = TManLibrary.tid_gen()
        dash = input("Choose dashboard: ")
        tag = input("Add #tag to this task: ")
        observers = None  # TODO здесь указать объект пользователя в системе или его uid
        executor = None  # TODO здесь указать объект пользователя в системе или его uid
        priority = input("Choose priority: ")
        author = current_user.uid
        reminder = input("Reminder: ")
        parent_id = tracked_tasks[subtask-1].tid
        return TManLibrary.add_subtask(subtasks, tid, parent_id, title, description, start, end, tag, dash, author,
                                       observers, executor, False, False, reminder, priority, tracked_tasks, subtask)

    @staticmethod
    def add_simple_task(users, current_user, simple_tasks):
        try:
            title = input("Input title: ")
            date = input("Choose date (YYYY-MM-DD): ")
            #year, month, day = map(int, date.split('-'))
            #date = datetime.date(year, month, day)
            description = input("Add some info about task: ")
            priority = input("Choose priority: ")
            tag = input("Add #tag to this task: ")
            tid = TManLibrary.tid_gen()
            is_completed = False
            return TManLibrary.add_simple_task(users, current_user, simple_tasks, title, date,
                                                   description, priority, tid, is_completed, tag)
        except TypeError as e:
            logging.warning("Trouble while input data at todo")
            print("Trouble while input data at todo")
        except Exception as e:
            print(e)

    @staticmethod
    def list_todo(simple_tasks):
        task_gen = TManLibrary.show_simple_task(simple_tasks)
        for task in task_gen:
            print(task)

    @staticmethod
    def list_task(tracked_tasks):
        task_gen = TManLibrary.show_tracked_task(tracked_tasks)
        for task in task_gen:
            click.echo("[" + task[0] + "] - " + task[1] + " - " + click.style(
                "Subtasks: " + task[2], bold=True, fg='yellow') + " - " + click.style(task[3], bold=True, bg='green'))

    @staticmethod
    def done_todo(todo, simple_tasks):
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError("Out of range")
            simple_tasks = TManLibrary.complete_simple_task(simple_tasks, todo)
        except IndexError as e:
            logging.warning("Out of range")
            print(e)


    @staticmethod
    def edit_task(task, tracked_tasks, simple_tasks):
        try:
            if (task - 1) > len(tracked_tasks):
                raise IndexError("Out of range")
            edit = tracked_tasks[task - 1]
            data = []
            data.append(edit.title)
            data.append(edit.start)
            data.append(edit.end)
            data.append(edit.description)
            for x in data:
                os.system("echo \"{}\" >> {}".format(x, "/tmp/tman_tempdata.tmp"))
            os.system("nano {}".format("/tmp/tman_tempdata.tmp"))
            data = []
            file = open("/tmp/tman_tempdata.tmp")
            for line in file:
                data.append(line[0:-1])
            os.system("rm /tmp/tman_tempdata.tmp")
            if len(data) != 4:
                raise Exception("Incorrect data")
            else:
                tracked_tasks[task - 1].title = data[0]
                tracked_tasks[task - 1].start = data[1]
                tracked_tasks[task - 1].end = data[2]
                tracked_tasks[task - 1].description = data[3]
            TManLibrary.resave_tracked_json(tracked_tasks)

            if tracked_tasks[task-1].cancel_sync != True:
                TManLibrary.Sync.sync_changes_todo(tracked_tasks[task-1], simple_tasks)
        except Exception as e:
            logging.warning(e)
            print(e)

    @staticmethod
    def edit_todo(todo, simple_tasks):
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError("Out of range")
            edit = simple_tasks[todo - 1]
            data = []
            data.append(edit.title)
            data.append(edit.date)
            data.append(edit.tag)
            data.append(edit.description)
            for x in data:
                os.system("echo \"{}\" >> {}".format(x, "/tmp/tman_tempdata.tmp"))
            os.system("nano {}".format("/tmp/tman_tempdata.tmp"))
            data = []
            file = open("/tmp/tman_tempdata.tmp")
            for line in file:
                data.append(line[0:-1])
            os.system("rm /tmp/tman_tempdata.tmp")
            if len(data) != 4:
                raise Exception("Incorrect data")
            else:
                simple_tasks[todo - 1].title = data[0]
                simple_tasks[todo - 1].date = data[1]
                simple_tasks[todo - 1].tag= data[2]
                simple_tasks[todo - 1].description = data[3]
            TManLibrary.resave_simple_json(simple_tasks)
        except Exception as e:
            print(e)



    @staticmethod
    def delete_todo(todo, simple_tasks):
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError
            simple_tasks = TManLibrary.delete_simple_task(simple_tasks, todo)
        except IndexError as e:
            logging.warning("Out of range while deleting. Index was: {}".format(todo))
            print(e)
        except Exception as e:
            print(e)
            logging.warning("Something done wrong while deleting. Index was: {}".format(todo))

    @staticmethod
    def info_todo(todo, simple_tasks):
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError("Такой задачи не существует. Выход за границы списка")
            selected_task = TManLibrary.show_simple_info(simple_tasks, todo)
            click.echo(click.style("TODO Task description: \t\t\t", bold=True, blink=True, bg='green'))
            click.echo("Title: "+click.style(str('\t\t' + selected_task.title), fg='white', bold=True))
            click.echo("Description: " + click.style(str('\t' + selected_task.description), fg='yellow'))
            click.echo("Date: " + click.style(str('\t\t' + selected_task.date), fg='yellow'))
            click.echo("Tag: " + click.style(str('\t\t' + selected_task.tag), fg='yellow'))
            click.echo("Is completed: " + click.style('\t' + str(selected_task.is_completed), fg='yellow'))
        except IndexError as e:
            logging.warning("Out of range while showing todo task info. Index was: {}".format(todo))
            print(e)

    #TODO - переделать на DataLib
    @staticmethod
    def done_task(task, subtasks, tracked_tasks):
        tid_subtasks = [x for x in tracked_tasks[task-1].subtasks]
        for subtask in subtasks:
            if subtask.is_completed == False and subtask.tid in tid_subtasks:
                raise Exception("You have undone subtasks! Done them all before you finish this one!")
        tracked_tasks[task-1].complete()
        TManLibrary.resave_tracked_json(tracked_tasks)

    @staticmethod
    def done_subtask(task, subtasks, tracked_tasks):
        """
        Тут не делим вывод с маркером, т.к. с GUI такой вывод не требуется ввиду обычного выделения подзадачи из списка
        Cначала генерируем список с tid подзадач текущей задачи, затем генерируем список этих подзадач - т.е. связанных

        """
        tid_subtasks = [x for x in tracked_tasks[task-1].subtasks]
        connected_subtasks = [result for result in subtasks if result.tid in tid_subtasks]
        for subtask in connected_subtasks:
            if subtask.is_completed:
                marker = "X"
            else:
                marker = " "
            click.echo("[" + marker + "] - " + str(connected_subtasks.index(subtask)+1)
                           + " - " + click.style(subtask.title, bg="red"))

        choose = int(input("Choose subtask: "))
        global_index = subtasks.index(connected_subtasks[choose-1])
        subtasks[global_index].complete()
        TManLibrary.resave_subtask_json(subtasks)

