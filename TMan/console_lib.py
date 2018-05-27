import click
import logging
import os
import task_manager_library
from datetime import datetime, timedelta, date
import calendar
import configparser


data_dir = os.environ['HOME']+'/tmandata/'


class Console:


    @staticmethod
    def create_new_user(users):
        login = input("Login: ")
        if (task_manager_library.validate_login(users, login)):
            name = input("Name: ")
            surname = input("Surname: ")
            task_manager_library.add_user(users, name, surname, login, {"simple": [], "task": [], "event": []})


    @staticmethod
    def import_users():

        return task_manager_library.load_users_from_json()

    @staticmethod
    def set_current(users, chuser):
        return task_manager_library.change_user(users, chuser)

    @staticmethod
    def show_current(users):

        current_user = task_manager_library.set_current(users)
        print("login: {}\nUID: {}".format(current_user.login, current_user.uid))

    @staticmethod
    def import_all_data(users):

        current_user = task_manager_library.set_current(users)
        tracked_tasks, all_tasks, all_users_tasks = task_manager_library.load_tasks_from_json(current_user)
        events = task_manager_library.EventActions.to_event(tracked_tasks)
        return (current_user, tracked_tasks, events, all_tasks, all_users_tasks)


    @staticmethod
    def add_task(sd, ed, tg, de, ti, re, ob, pr):
        try:
            current_user = task_manager_library.get_current_user()
            pr = str(task_manager_library.Priority[pr].value)
            if ob != "":
                ob+=',{}'.format(current_user.login)
            else:
                ob = current_user.login
            executor = None
            author = current_user.uid
            task_manager_library.add_tracked_task(ti, de, sd, ed, tg, author, ob, executor, re, pr)

        except ValueError as e:
            print(e)
            logging.warning(e)
        except Exception as e:
            print(e)
            logging.warning("Some troubles while adding task")

    @staticmethod
    def add_subtask(current_user, all_tasks, all_users_tasks, tracked_tasks,  users, subtask,
                    sd, ed, tg, de, ti, re, ob, pr):

        try:

            pr = str(task_manager_library.Priority[pr].value)
            if ob != "":
                ob += ',{}'.format(current_user.login)
            else:
                ob = current_user.login
            executor = None
            author = current_user.uid
            tid = task_manager_library.tid_gen()
            parent_id = tracked_tasks[subtask-1].tid
            global_index = all_tasks.index(tracked_tasks[subtask-1])
            all_tasks[global_index].subtasks.append(tid)

            return task_manager_library.add_tracked_task(
                all_users_tasks, tid, ti, de, sd, ed, tg,
                author, ob, executor, False, re, pr, users, current_user, parent_id, [], None, False)
        except ValueError as e:
            logging.warning("Some troubles while adding subtask. Probably DATE/TIME or PRIORITY")
            print(e)
        except Exception as e:
            logging.warning("Some unexpected troubles while adding subtask")
            print("Some unexpected troubles while adding subtask\n+{}".format(e))

    @staticmethod
    def preorder_traversal(task, all_tasks):
        for subtasks in all_tasks:
            click.echo("subtasks.node")

    @staticmethod
    def list_task(tracked_tasks, all_tasks):
        task_gen = task_manager_library.show_tracked_task(tracked_tasks, all_tasks)
        for task in task_gen:
            click.echo("[" + task[0] + "] - " + task[1] + " - " + click.style(
                "Subtasks: " + task[2], bold=True, fg='yellow') + " - " + click.style(task[3], bold=True, bg='green'))
            # Тут можно сделать preorder traversal


    @staticmethod
    def done_todo(todo, simple_tasks):
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError("Out of range")
            simple_tasks = task_manager_library.complete_simple_task(simple_tasks, todo)
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
    def edit_task(current, task_num, task_field, all_users_tasks,  tracked_tasks, all_tasks):
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
            all_users_tasks[task_index].start = task_manager_library.check_date(str(data[1]))
            all_users_tasks[task_index].end = task_manager_library.check_date(str(data[2]))
            all_users_tasks[task_index].description = data[3]
            task_manager_library.resave_task_to_json(all_users_tasks)


        except Exception as e:
            logging.warning(e)
            print(e)


    @staticmethod
    def delete_todo(todo, simple_tasks,tracked_tasks):
        try:
            if (todo - 1) > len(simple_tasks):
                raise IndexError
            simple_tasks = task_manager_library.delete_simple_task(simple_tasks, todo, tracked_tasks)
        except IndexError as e:
            logging.warning("Out of range while deleting. Index was: {}".format(todo))
            print(e)
        except Exception as e:
            print(e)
            logging.warning("Something done wrong while deleting. Index was: {}".format(todo))


    #TODO - переделать на DataLib
    @staticmethod
    def done_task(task, all_tasks, tracked_tasks, all_users_tasks):
        for subtask in all_tasks:
            if subtask.parent == tracked_tasks[task-1].tid and subtask.is_completed == False:
                raise Exception("You have undone subtasks! Done them all before you finish this one!")
        global_index = all_users_tasks.index(tracked_tasks[task-1])
        all_users_tasks[global_index].complete()
        task_manager_library.resave_task_to_json(all_users_tasks)

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
        task_manager_library.resave_task_to_json(all_users_tasks)

    @staticmethod
    def show_week(events):
        current_events = [date(x.date.year, x.date.month, x.date.day) for x in events]
        week_range = task_manager_library.EventActions.daterange(date.today(), date.today() + timedelta(days=7))
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
    def add_scheduler_task(events, all_tasks, current, users):
        """Если в задачах на сегодня нету planned= True и оно попадает в этот день, то создаем"""
        config = configparser.ConfigParser()
        config.read(data_dir + "/scheduler.ini")
        weekday = calendar.day_name[date.today().weekday()][0:3]
        for section in config.sections():
            weekdays = config.get(section, 'weekday').split(" ")
            status = None
            # есили status = False, то не добавляем
            if config.get(section, 'last_added') is not "":
                is_added = task_manager_library.check_date(config.get(section, 'last_added'))
                if is_added.date() == datetime.today().date():
                    status = False
                else:
                    status = True
            else:
                status = True
            if weekday in weekdays and status is True:
                today = task_manager_library.check_date(
                    str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day))
                title = config.get(section, 'title')
                description = config.get(section, 'basic_description')
                config.set(section, 'last_added', str(date.today().year)
                           + "-" + str(date.today().month) + "-" + str(date.today().day))
                task_manager_library.add_tracked_task(
                    all_tasks, task_manager_library.tid_gen(), title, description, today,
                    today, "Planned", "Planned",
                    current.uid, None, None, True, False, task_manager_library.check_time("00:00"),
                    str(task_manager_library.Priority['high'].value), users, current, None, [], None, True)
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
        sid = task_manager_library.tid_gen()
        week_list = weeks.split(" ")
        new_scheduler = task_manager_library.Scheduler(week_list, title, desc, sid, None)
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
        if not isinstance(priority, task_manager_library.Priority):
            raise TypeError("Incorrect priority type")
        tasks = [x for x in tracked_tasks if x.priority is priority]
        for task in tasks:
            if task.is_completed:
                marker = "X"
            else:
                marker = " "
            click.echo(
                click.style('['+marker+']'+' - '+task.title+'\n', bg='blue', fg='white')
                + click.style(task.description, bg='green', fg='white') +"\n"
                + click.style("From: "+str(task.start)+" - To: "+ str(task.end), bg='green', fg='white') + "\n"
                + click.style("Author: " + task_manager_library.get_login(task.author, users), bg='green', fg='white') + "\n"
                + click.style("#"+task.tag, bg='red', fg='white') + "\n")

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

    @staticmethod
    def set_logger(level, format, file):
        try:
            print(level)
            if level == "INFO":
                level = logging.INFO
            elif level == "WARNING":
                level = logging.WARNING
            else:
                raise Exception
            task_manager_library.loggingConfig.set_logging_config(level, str(format), str(file))
        except ValueError:
            pass
        except Exception:
            click.echo("Choose correct level")

