import click
import logging
import os
import TManLibrary
from datetime import datetime, timedelta, date
import calendar
import configparser


data_dir = os.environ['HOME']+'/tmandata/'


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
        """
        Загрузить всех пользователей
        """
        return TManLibrary.data_from_json("User", None)

    @staticmethod
    def set_current(users, chuser):
        """
        Установить текущнго пользователя
        """
        return TManLibrary.change_user(users, chuser)

    @staticmethod
    def show_current(users):
        """
        Показать текущего
        """
        current_user = TManLibrary.set_current(users)
        print("login: {}\nUID: {}".format(current_user.login, current_user.uid))

    @staticmethod
    def import_all_data(users):
        """
        Загрузить все данные
        """
        current_user = TManLibrary.set_current(users)
        simple_tasks = TManLibrary.data_from_json("TODO", current_user)
        tracked_tasks, all_tasks, all_users_tasks = TManLibrary.data_from_json("Task", current_user)
        events = TManLibrary.Sync.to_event(tracked_tasks)
        return (current_user, simple_tasks, tracked_tasks, events, all_tasks, all_users_tasks)


    @staticmethod
    def add_task(current_user, all_tasks, all_users_tasks, users, simple_tasks):
        """
        Добавление новой задачи трекера. Возвращает измененную коллекцию с новым элементом
        """
        try:
            if current_user is None:
                raise Exception("There is no current user. Choose one")
            title = input("Input title: ")
            start = TManLibrary.check_date(input("Choose start date: "))
            end = TManLibrary.check_date(input("Choose end date: "))
            description = input("Add some info about task: ")
            dash = input("Choose dashboard: ")
            tag = input("Add #tag to this task: ")
            observers = input("Please, input logins to share task:")
            if observers != "":
                observers+=',{}'.format(current_user.login)
            else:
                observers = current_user.login
            executor = None  # TODO здесь указать объект пользователя в системе или его uid
            priority = str(TManLibrary.Priority[input("Choose priority: ")].value)
            author = current_user.uid
            reminder = TManLibrary.check_time(input("Reminder: "))
            tid = TManLibrary.tid_gen()
            parent = None

            if click.confirm('Cancel sync w/ TODO list and events in calendar?', default=True):
                cancel_sync = True
            else:
                cancel_sync = False

            return TManLibrary.add_tracked_task(
                all_users_tasks, simple_tasks, tid, title, description, start,end, tag, dash,
                author, observers, executor, cancel_sync, False, reminder, priority, users, current_user, parent, [], None, False)
        except ValueError as e:
            print(e)
            logging.warning(e)
        except Exception as e:
            print(e)
            logging.warning("Some troubles while adding task")

    @staticmethod
    def add_subtask(current_user, all_tasks, all_users_tasks, simple_tasks, tracked_tasks,  users, subtask):

        """subtask -  параметр Click, номер задачи"""

        try:
            title = input("Input title: ")
            start = TManLibrary.check_date(input("Choose start date: "))
            end = TManLibrary.check_date(input("Choose end date: "))
            description = input("Add some info about task: ")
            tid = TManLibrary.tid_gen()
            dash = input("Choose dashboard: ")
            tag = input("Add #tag to this task: ")
            observers = ','.join(tracked_tasks[subtask-1].observers)
            executor = None  # TODO здесь указать объект пользователя в системе или его uid
            priority = str(TManLibrary.Priority[input("Choose priority: ")].value)
            author = current_user.uid
            reminder = TManLibrary.check_time(input("Reminder: "))
            parent_id = tracked_tasks[subtask-1].tid
            global_index = all_tasks.index(tracked_tasks[subtask-1])
            all_tasks[global_index].subtasks.append(tid)
            print(all_tasks[global_index].subtasks)
            return TManLibrary.add_tracked_task(
                all_users_tasks, simple_tasks, tid, title, description, start, end, tag, dash,
                author, observers, executor, True, False, reminder, priority, users, current_user, parent_id, [], None, False)
        except ValueError as e:
            logging.warning("Some troubles while adding subtask. Probably DATE/TIME or PRIORITY")
            print(e)
        except Exception as e:
            logging.warning("Some unexpected troubles while adding subtask")
            print("Some unexpected troubles while adding subtask\n+{}".format(e))

    @staticmethod
    def add_simple_task(users, current_user, simple_tasks):
        """
        Добавить задачу TO DO
        """
        try:
            title = input("Input title: ")
            date = TManLibrary.check_date(input("Choose date (YYYY-MM-DD): "))
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
    def preorder_traversal(task, all_tasks):
        for subtasks in all_tasks:
            click.echo("subtasks.node")



    @staticmethod
    def list_task(tracked_tasks, all_tasks):
        task_gen = TManLibrary.show_tracked_task(tracked_tasks, all_tasks)
        for task in task_gen:
            click.echo("[" + task[0] + "] - " + task[1] + " - " + click.style(
                "Subtasks: " + task[2], bold=True, fg='yellow') + " - " + click.style(task[3], bold=True, bg='green'))
            # Тут можно сделать preorder traversal



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
    def open_nano(data, num):
        os.system("echo \"{}\" >> {}".format(data[num], "/tmp/tman_tempdata.tmp"))
        os.system("nano {}".format("/tmp/tman_tempdata.tmp"))
        file = open("/tmp/tman_tempdata.tmp")
        data[num] = file.read()[0:-1]
        os.system("rm /tmp/tman_tempdata.tmp")
        return data

    @staticmethod
    def edit_task(current, task_num, task_field, all_users_tasks,  tracked_tasks, simple_tasks, all_tasks):
        author_name = tracked_tasks[task_num-1].author
        if author_name != current.uid:
            raise ValueError("Access denied")
            logging.warning("Trying to get access to other user's task")
        try:
            if (task_num - 1) > len(tracked_tasks):
                raise IndexError("Out of range")
            edit = tracked_tasks[task_num - 1]
            # получаем индекс редактируемой задачи относительно коллекции всех задач

            task_index = all_users_tasks.index(edit)
            # или можно сделать из объекта dict и работать с ним прямо по названию task_field
            data = []
            data.append(edit.title)
            data.append(edit.start.date())
            data.append(edit.end.date())
            data.append(edit.description)

            if task_field == "title":
                data = Console.open_nano(data, 0)
            elif task_field == "start":
                data = Console.open_nano(data, 1)
            elif task_field == "end":
                data = Console.open_nano(data, 2)
            elif task_field == "description":
                data = Console.open_nano(data, 3)
            else:
                raise ValueError("ERROR! Unsupported field!")

            all_users_tasks[task_index].title = data[0]
            all_users_tasks[task_index].start = TManLibrary.check_date(str(data[1]))
            all_users_tasks[task_index].end = TManLibrary.check_date(str(data[2]))
            all_users_tasks[task_index].description = data[3]
            TManLibrary.resave_tracked_json(all_users_tasks)

            if tracked_tasks[task_num-1].cancel_sync != True:
                TManLibrary.Sync.sync_changes_todo(all_users_tasks[task_index], simple_tasks)
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
    def delete_todo(todo, simple_tasks,tracked_tasks):
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError
            simple_tasks = TManLibrary.delete_simple_task(simple_tasks, todo, tracked_tasks)
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
    def done_task(task, all_tasks, tracked_tasks, all_users_tasks):
        for subtask in all_tasks:
            if subtask.parent == tracked_tasks[task-1].tid and subtask.is_completed == False:
                raise Exception("You have undone subtasks! Done them all before you finish this one!")
        global_index = all_users_tasks.index(tracked_tasks[task-1])
        all_users_tasks[global_index].complete()
        TManLibrary.resave_tracked_json(all_users_tasks)

    @staticmethod
    def done_subtask(task, all_tasks, tracked_tasks, all_users_tasks):
        """
        Тут не делим вывод с маркером, т.к. с GUI такой вывод не требуется ввиду обычного выделения подзадачи из списка
        Cначала генерируем список с tid подзадач текущей задачи, затем генерируем список этих подзадач - т.е. связанных

        """
        #список подзадач задачи
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tracked_tasks[task-1].tid:
                tid_subtasks.append(subtask)

        #connected_subtasks = [result for result in all_tasks if result.tid in tid_subtasks]
        #получить информацию о завершенных и незавершенных подзадачах
        for subtask in tid_subtasks:
            if subtask.is_completed:
                marker = "X"
            else:
                marker = " "
            click.echo("[" + marker + "] - " + str(tid_subtasks.index(subtask) + 1)
                       + " - " + click.style(subtask.title, bg="red"))

        choose = int(input("Choose subtask: "))
        global_index = all_users_tasks.index(tid_subtasks[choose - 1])
        all_users_tasks[global_index].complete()
        TManLibrary.resave_tracked_json(all_users_tasks)

    @staticmethod
    def show_week(events):
        current_events = [date(x.date.year, x.date.month, x.date.day) for x in events]
        week_range = TManLibrary.Sync.daterange(date.today(), date.today() + timedelta(days=7))
        for week_day in week_range:
            if week_day in current_events:
                click.echo(click.style(str(week_day.day), bold=True, fg='black', bg='white') + " ", nl=False)
            else:
                click.echo(str(week_day.day)+" ", nl=False)
        click.echo("\nEvents for today("+click.style("{}, {}".format(calendar.day_name[date.today().weekday()],
                                                                     str(date.today())), bold=True)+"):")
        for x in events:
            if date(x.date.year, x.date.month, x.date.day) == date.today():
                click.echo(click.style(x.title,bg='red', fg='white'))

    @staticmethod
    def add_scheduler_task(events, all_tasks, current, simple_tasks, users):
        """Если в задачах на сегодня нету planned= True и оно попадает в этот день, то создаем"""
        config = configparser.ConfigParser()
        config.read(data_dir + "/scheduler.ini")
        weekday = calendar.day_name[date.today().weekday()][0:3]
        for section in config.sections():
            weekdays = config.get(section, 'weekday').split(" ")
            status = None
            # есили status = False, то не добавляем
            if config.get(section, 'last_added') is not "":
                is_added = TManLibrary.check_date(config.get(section, 'last_added'))
                if is_added.date() == datetime.today().date():
                    status = False
                else:
                    status = True
            else:
                status = True
            if weekday in weekdays and status is True:
                today = TManLibrary.check_date(
                    str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day))
                title = config.get(section, 'title')
                description = config.get(section, 'basic_description')
                config.set(section, 'last_added', str(date.today().year)
                           + "-" + str(date.today().month) + "-" + str(date.today().day))
                TManLibrary.add_tracked_task(
                    all_tasks, simple_tasks, TManLibrary.tid_gen(), title, description, today,
                    today, "Planned", "Planned",
                    current.uid, None, None, True, False, TManLibrary.check_time("00:00"),
                    str(TManLibrary.Priority['high'].value), users, current, None, [], None, True)
        with open(data_dir+"/scheduler.ini", 'w') as f:
            config.write(f)
        return Console.import_all_data(users)


    @staticmethod
    def add_scheduler():
        click.secho("Choose list of days of the week, title,\nbasic description of your future task  ",
                    bg="green", fg="white", bold=True)
        click.secho("Sample of input weekdays: Wed Tue Mon  ",
                    bg="yellow", fg="white")
        title = input("Input title of shelduler's task: ")
        desc = input("Input small and common description: ")
        weeks = input("Choose weekdays. Split by spaces: ")
        #sid - schelduler ID
        sid = TManLibrary.tid_gen()
        week_list = weeks.split(" ")
        new_scheduler = TManLibrary.Scheduler(week_list, title, desc, sid, None)
        Console.scheduler_cfg(new_scheduler)

    @staticmethod
    def scheduler_cfg(new_scheduler):
        #Временно
        weekdays = str()
        for day in new_scheduler.weekday:
            weekdays = weekdays + " " + day
        #
        config = configparser.ConfigParser()
        section = new_scheduler.sid

        config.add_section(section)
        config.set(section, 'title', new_scheduler.title)
        config.set(section, 'basic_description', new_scheduler.basic_description)
        config.set(section, 'weekday', weekdays)
        config.set(section, 'last_added', "")

        with open(data_dir+"/scheduler.ini", 'a+') as f:
            config.write(f)

    @staticmethod
    def show_by_priority(priority, tracked_tasks, users):
        if not isinstance(priority, TManLibrary.Priority):
            raise TypeError("Incorrect priority type")
        tasks = [x for x in tracked_tasks if x.priority is priority]
        for task in tasks:
            if task.is_completed:
                marker = "X"
            else:
                marker = " "
            click.echo(
                click.style('['+marker+']'+' - '+task.title+'\n', bg='blue', fg='white')
                +click.style(task.description, bg='green', fg='white')+"\n"
                +click.style("From: "+str(task.start)+" - To: "+ str(task.end), bg='green', fg='white') + "\n"
                +click.style("Author: "+TManLibrary.get_login(task.author, users), bg='green', fg='white') + "\n"
                +click.style("#"+task.tag, bg='red', fg='white') + "\n")

    @staticmethod
    def show_by_tag(tag, tracked_tasks):
        #переделать на классы-теги
        tasks = [x for x in tracked_tasks if x.tag == tag]
        for task in tasks:
            if task.is_completed:
                marker = "X"
            else:
                marker = " "
            click.echo(
                click.style('[' + marker + ']' + ' - ' + task.title + '\n', bg='blue', fg='white'))