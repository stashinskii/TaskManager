import unittest
import re
import sys
import ConsoleLib
import TManLibrary


class MyTest(unittest.TestCase):
    class MyOutput(object):
        def __init__(self):
            self.data = []

        def write(self, s):
            self.data.append(s)

        def __str__(self):
            return "".join(self.data)

    def test_current(self):
        stdout_org = sys.stdout
        my_stdout = self.MyOutput()
        users = ConsoleLib.Console.import_users()
        current = ConsoleLib.Console.set_current(users, "testuser")
        try:
            sys.stdout = my_stdout
            ConsoleLib.Console.show_current(users)
        finally:
            sys.stdout = stdout_org

        self.assertEquals(str(my_stdout), "login: testuser\nUID: testid\n")

    def test_add_task(self):
        users = ConsoleLib.Console.import_users()
        (current_user, simple_tasks, tracked_tasks,
         calendar_events, all_tasks, all_users_tasks) = ConsoleLib.Console.import_all_data(users)
        self.assertRaises(AttributeError,
        TManLibrary.add_tracked_task,
                all_users_tasks, simple_tasks, "testid", "test", "test", "testdate","testdate", "testate", "",
                "user", "users", "users", True, False, None, None, users, current_user, None, [], None, False)

    def check_index(self):
        users = ConsoleLib.Console.import_users()
        current_user = TManLibrary.set_current(users)
        simple_tasks = TManLibrary.data_from_json("TODO", current_user)
        self.assertRaises(IndexError, ConsoleLib.Console.info_todo, 1000000000, simple_tasks)

    def test_without_user(self):
        users = ConsoleLib.Console.import_users()
        user = TManLibrary.logout(users)
        self.assertRaises(Exception, TManLibrary.set_current, users)

    def test_show_tools(self):
        users = ConsoleLib.Console.import_users()
        user = TManLibrary.logout(users)
        self.assertRaises(TypeError, ConsoleLib.Console.show_by_priority, "high", [], [])





