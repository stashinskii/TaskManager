import re
import sys
import unittest
from datetime import datetime
from faker import Faker

import config
from task_manager_library import DataStorage
from task_manager_library import actions
from task_manager_library.controllers.scheduler_controller import SchedulerController
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.models.scheduler_model import Scheduler
from task_manager_library.models.task_model import Tag, Task, Status, Priority
from user_actions import UserTools
from utility import utils, logging_utils, console_utils, serialization_utils

DataStorage.PATH = config.DATA_PATH
UserTools.PATH = config.CURRENT_USER_CONFIG
DataStorage.CURRENT_USER = UserTools.get_current_user()

login = Faker().state()
task = Task("Test_task", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
            datetime.strptime("2018-06-12", "%Y-%m-%d"),Tag("tag_test"), DataStorage.CURRENT_USER.login,
            [], None, datetime.strptime("12:00", "%H:%M"), Priority.high, None, None)


class MyTest(unittest.TestCase):


    class MyOutput(object):
        def __init__(self):
            self.data = []

        def write(self, s):
            self.data.append(s)

        def __str__(self):
            return "".join(self.data)

    # region Utils test

    def test_check_date(self):
        expected_start_date = datetime.strptime("2018-05-12", "%Y-%m-%d")
        start = utils.check_date(None, None, "2018-05-12")
        self.assertEquals(start, expected_start_date)

    def test_check_time(self):
        expected_start_date = datetime.strptime("12:00", "%H:%M")
        start = utils.check_time(None, None, "12:00")
        self.assertEquals(start, expected_start_date)

    def test_validate_login(self):
        new_login = Faker().name()
        UserTools.add_user(new_login, "TestName", "TestSurname")
        result = UserTools.validate_login(new_login)
        self.assertEquals(False, result)

    # endregion

    # region Task controller test

    def test_task_creation(self):
        count_before = len(DataStorage.load_tasks_from_json()[0])
        TaskController.add(task)
        count_after = len(DataStorage.load_tasks_from_json()[0])

        self.assertEquals(count_before + 1, count_after)

    def test_get_by_index(self):
        last_element = len(DataStorage.load_tasks_from_json()[0]) - 1
        new_task = TaskController.get_by_index(last_element)
        self.assertEquals(new_task.title, task.title)

    def test_progress(self):
        last_element = len(DataStorage.load_tasks_from_json()[0]) - 1
        TaskController.begin_task(last_element)
        task_new = TaskController.get_by_index(last_element)
        self.assertEquals(Status.process, task_new.is_completed)

    def test_done(self):
        last_element = len(DataStorage.load_tasks_from_json()[0]) - 1
        TaskController.complete_task(last_element)
        task_new = TaskController.get_by_index(last_element)
        self.assertEquals(Status.done, task_new.is_completed)

    def test_undone(self):
        last_element = len(DataStorage.load_tasks_from_json()[0]) - 1
        TaskController.uncomplete_task(last_element)
        task_new = TaskController.get_by_index(last_element)
        self.assertEquals(Status.undone, task_new.is_completed)

    # endregion

    # region Test scheduler region

    def test_create_scheduler(self):
        len_before = len(DataStorage.load_schedulers_from_json())
        scheduler = Scheduler(datetime.now(), task, 12)
        print(type(scheduler.task.start))
        SchedulerController.add(scheduler)
        len_after = len(DataStorage.load_schedulers_from_json())
        self.assertEquals(len_before + 1, len_after)

    # endregion

    # region User actions test

    def test_create_user(self):
        login = Faker().name()
        len_before = len(DataStorage.load_users_from_json())
        UserTools.add_user(login, "TestName", "TestSurname")
        len_after = len(DataStorage.load_users_from_json())
        self.assertEquals(len_before + 1, len_after)

    def test_change_user(self):
        new_login = Faker().name()
        UserTools.add_user(new_login, "TestName", "TestSurname")
        status = UserTools.set_current_user(new_login)
        self.assertEquals(status, True)

    # endregion

    # region Wrong data tests

    def test__wrong_change_user(self):
        new_login = Faker().name()
        new_login *= 2
        self.assertRaises(Exception, UserTools.set_current_user, new_login)

    def test_empty_edit_field(self):
        len_data = len(DataStorage.load_tasks_from_json()[0])
        self.assertRaises(IndexError, TaskController.edit, len_data + 1, "title")

    #def test_wrong_adding_task(self):
    #    task = Task("df", "fd", "2012-02-02", "2012-02-02", "fdfd", None, "", None,
    #                "12:00", Priority.low, None, None)
    #    self.assertRaises(TypeError, TaskController.add, task)

    # endregion

    # region Models tests
    def test_task_adding(self):
        self.assertIsInstance(task, Task)

    def test_tag_adding(self, name="tag name", description = "tag desc"):
        new_tag = Tag(name, description)
        self.assertIsInstance(new_tag, Tag)
        self.assertEquals(new_tag.tag_name, name)
        self.assertEquals(new_tag.description, description)

    def test_priority_ading(self):
        priority = Priority.high
        self.assertIsInstance(priority, Priority)

    # endregion

    # region Data Storage test

    # TODO implement this region

    # endregion





















    '''


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
        self.assertEquals(task_manager_library.Task, type(task))

    def test_wrong_login(self):
        task_manager_library.DataStorage.PATH = config.DATA_PATH
        self.assertRaises(Exception, task_manager_library.UserTools.set_current_user, "dfdffddfdffddf")

    def test_wrong_edit_field(self):
        task_manager_library.UserTools.set_current_user("herman")
        self.assertRaises(ValueError, task_manager_library.edit_task, 2,"sdgh")

    def test_empty_edit_field(self):
        new_login = utility.serialization_utils.tid_gen()
        task_manager_library.UserTools.add_user(new_login, "testname", "testsurname")
        task_manager_library.UserTools.set_current_user(new_login)
        self.assertRaises(IndexError, task_manager_library.edit_task, 50,"title")

    def test_task_object_creation(self):
        start_date = datetime.strptime("2018-02-05", "%Y-%m-%d")
        end_date = datetime.strptime("2019-02-05", "%Y-%m-%d")
        my_time = datetime.strptime("12:00", "%H:%M")
        task = task_manager_library.add_tracked_task("fddffd", "fdfdfd", start_date, end_date,
                                                     "tag", "testlogin",
                                                     my_time, "low",
                                                     False, False, None)
        self.assertEquals(task.is_completed,task_manager_library.Status.undone)
        '''

