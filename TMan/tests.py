import unittest
import re
import sys
import console_lib
import task_manager_library


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
        users = console_lib.Console.import_users()
        current = console_lib.Console.set_current(users, "testuser")
        try:
            sys.stdout = my_stdout
            console_lib.Console.show_current(users)
        finally:
            sys.stdout = stdout_org

        self.assertEquals(str(my_stdout), "login: testuser\nUID: testid\n")

    def test_add_task(self):
        users = console_lib.Console.import_users()
        (current_user, tracked_tasks,
         calendar_events, all_tasks, all_users_tasks) = console_lib.Console.import_all_data(users)
        self.assertRaises(AttributeError,
                          task_manager_library.add_tracked_task,
                          all_users_tasks, "testid", "test", "test", "testdate","testdate", "testate", "",
                "users", True, False, None, None, users, current_user, None, [], None, False)

    def check_index(self):
        users = console_lib.Console.import_users()
        current_user = task_manager_library.set_current(users)
        simple_tasks = task_manager_library.data_from_json("TODO", current_user)
        self.assertRaises(IndexError, console_lib.Console.info_todo, 1000000000, simple_tasks)

    def test_without_user(self):
        users = console_lib.Console.import_users()
        user = task_manager_library.logout(users)
        self.assertRaises(Exception, task_manager_library.set_current, users)

    def test_show_tools(self):
        users = console_lib.Console.import_users()
        user = task_manager_library.logout(users)
        self.assertRaises(TypeError, console_lib.Console.show_by_priority, "high", [], [])

    def test_check_date(self):
        self.assertRaises(TypeError, task_manager_library.check_date(None, "fdfd"))

    def test_check_time(self):
        self.assertRaises(TypeError, task_manager_library.check_time(None, "9:00"))





