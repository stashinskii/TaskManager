import calendar
import click
import configparser
import logging
import os
from datetime import datetime, timedelta, date

import task_manager_library

data_dir = os.environ['HOME']+'/tmandata/'


class Console:
    @staticmethod
    def add_task(sd, ed, tg, de, ti, re, ob, pr):
        try:
            current_user = task_manager_library.UserTools.get_current_user()
            pr = str(task_manager_library.Priority[pr].value)
            if ob != "":
                ob+=',{}'.format(current_user.login)
            else:
                ob = current_user.login

            if ob != "":
                ob = ob.split(",")
            else:
                ob = []

            executor = None
            author = current_user.uid
            task_manager_library.add_tracked_task(ti, de, sd, ed, tg, author, ob, executor, re, pr)

        except ValueError as e:
            print(e)
            logging.warning(e)
        #except Exception as e:
        #    print(e)
        #    logging.warning("Some troubles while adding task")

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
    def done_subtask(task, all_tasks, tracked_tasks, all_users_tasks):

        #список подзадач задачи
        tid_subtasks = []

        for subtask in all_tasks:
            if subtask.parent == tracked_tasks[task-1].tid:
                tid_subtasks.append(subtask)

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

