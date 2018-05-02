import sys, os, time, atexit, signal, click
from datetime import datetime, timedelta


class Daemon:
    """Общий класс дл работы с демоном.
    Предполагает переопределение его методов дочерними классами"""

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        """Демонизация"""

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        os.chdir('/')
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        #os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Запуск демона"""
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            sys.exit(1)
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        if not pid:
            message = "pidfile {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return

        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        pass


class TManReminder(Daemon):
    """
    Демон, следящий за напоминаниями в ближайшие 5 часов
    """
    def __init__(self, tracked_tasks, pidfile):
        Daemon.__init__(self,  pidfile)
        self.tracked_tasks = tracked_tasks

    def run(self):
        from TManLibrary import Sync, TaskLib

        #Коллекция, содержащая задачи, которые доступны сегодня
        observed_day = []

        for task in self.tracked_tasks:
            for info in Sync.daterange(task.start.date(), (task.end + timedelta(days=1)).date()):
                if datetime.today().date() == info:
                    observed_day.append(task)

        while True:
            time.sleep(1)
            if len(observed_day) != 0:
                click.echo(click.style("\nYou have tasks in near 5 hours!\t\t\t", bg='green', fg='white'))
            #проверяем, что данная задача имеет статус напоминания +- 5 часов от текущего времени
            for task in observed_day:
                dt1 = datetime.now() + timedelta(hours=5)
                dt2 = datetime.now() - timedelta(hours=5)
                if (task.reminder.time() <= dt1.time() or task.reminder.time() >= dt2.time()):
                    click.echo(task.title)
            #Прекращаем отслеживание на 30 минут
            time.sleep(1800)


