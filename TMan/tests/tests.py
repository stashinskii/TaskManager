import re
import sys
import unittest
from datetime import datetime

import config
import task_cli
import task_manager_library
import tests
import utility


class MyTest(unittest.TestCase):
    class MyOutput(object):
        def __init__(self):
            self.data = []

        def write(self, s):
            self.data.append(s)

        def __str__(self):
            return "".join(self.data)

    def test_validateLogin(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        task_manager_library.UserTools.add_user("testlogin", "testname", "testsurname")
        self.assertRaises(Exception, task_manager_library.UserTools.validate_login, "testlogin")

    def test_current(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        task_manager_library.UserTools.change_user("testlogin")
        current = task_manager_library.UserTools.get_current_user()
        self.assertEquals("testlogin", current.login)

    def test_check_date(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        expected_date = datetime.strptime("2018-02-05", "%Y-%m-%d")
        tested_date = utility.utils.check_date(None, None, "2018-02-05")
        self.assertEquals(expected_date, tested_date)

    def test_check_time(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        my_time = datetime.strptime("12:00", "%H:%M")
        tested_date = utility.utils.check_time(None, None, "12:00")
        self.assertEquals(my_time, tested_date)

    def test_wrong_adding_task(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        self.assertRaises(Exception, task_cli.add, (True, False, False, "2018-02-03", "2012-02-03", "jero", "dfkldf",
        "fdfddf", "12:00", "herman1", "low", None))

    def test_add_task(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        start_date = datetime.strptime("2018-02-05", "%Y-%m-%d")
        end_date = datetime.strptime("2019-02-05", "%Y-%m-%d")
        my_time = datetime.strptime("12:00", "%H:%M")
        task = task_manager_library.add_tracked_task("fddffd", "fdfdfd", start_date, end_date,
                     "tag", "testlogin",
                     my_time, "low",
                     False, False, None)
        self.assertEquals(task_manager_library.TrackedTask, type(task))

    def test_wrong_login(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        self.assertRaises(Exception, task_manager_library.UserTools.change_user, "dfdffddfdffddf")

    def test_wrong_field_edit(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH

        self.assertRaises(IndexError ,task_manager_library.edit_task, 1,"sdgh")
