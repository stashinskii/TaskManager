import re
import sys
import unittest
from datetime import datetime, timedelta
from faker import Faker

import config
from task_manager_library import DataStorage
from task_manager_library import actions
from task_manager_library.controllers.notification_controller import NotificationController
from task_manager_library.controllers.scheduler_controller import SchedulerController
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.models.notifications_model import Notifications
from task_manager_library.models.scheduler_model import Scheduler
from task_manager_library.models.task_model import Tag, Task, Status, Priority
from console.user import User
from console.user_actions import UserTools
from task_manager_library.utility import utils, logging_utils, console_utils, serialization_utils

DataStorage.PATH = config.DATA_PATH
UserTools.PATH = config.CURRENT_USER_CONFIG
DataStorage.CURRENT_USER = UserTools.get_current_user()

# TODO create class with Faker, signing in and other stuff

login = Faker().state()
task = Task("Test_task", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
            datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
            [], None, datetime.strptime("12:00", "%H:%M"), Priority.high, None, None)


class MyTest(unittest.TestCase):

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

    def test_empty_observers_splitter(self):
        fake_current = User(Faker().name(),
                            Faker().name(),
                            serialization_utils.tid_gen(),
                            Faker().name(),
                            True)
        splitted = serialization_utils.split_str_to_list("", fake_current)
        self.assertEquals(splitted, [fake_current.login])

    def test_id_generator(self):
        id = serialization_utils.tid_gen()
        self.assertIsInstance(id, str)

    def test_date_serialization(self):
        date = serialization_utils.date_to_str(datetime.now())
        self.assertIsInstance(date, str)

    def test_time_serialization(self):
        date = serialization_utils.time_to_str(datetime.now())
        self.assertIsInstance(date, str)

    # endregion

    # region Task controller test

    def test_linking_tasks(self):
        task_1 = Task("LINK2", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
                      datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
                      [], None, datetime.strptime("12:00", "%H:%M"), Priority.high, None, None, None,
                      serialization_utils.tid_gen())
        task_2 = Task("LINK1", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
                      datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
                      [], None, datetime.strptime("12:00", "%H:%M"), Priority.high, None, None, None,
                      serialization_utils.tid_gen())

        TaskController.add(task_1)
        TaskController.add(task_2)

        TaskController.make_link(task_1.tid, task_2.tid)

        task = self.get_by_tid(task_1.tid)

        self.assertEquals(True, task.connection[0] == task_2.tid)

    def test_task_creation(self):
        count_before = len(DataStorage.load_tasks_from_json()[0])
        TaskController.add(task)
        count_after = len(DataStorage.load_tasks_from_json()[0])

        self.assertEquals(count_before + 1, count_after)

    def test_get_by_tid(self):
        TaskController.add(task)
        result = DataStorage.get_task_from_id(task.tid)
        self.assertEqual(result.tid, task.tid)

    def test_get_by_index(self):
        TaskController.add(task)
        last_element = len(DataStorage.load_tasks_from_json()[0]) - 1
        new_task = TaskController.get_by_index(last_element)
        self.assertEquals(new_task.title, task.title)

    def test_progress(self):
        last_element = len(DataStorage.load_tasks_from_json()[2])
        last = DataStorage.load_tasks_from_json()[2][last_element - 1].tid
        TaskController.begin_task(last)
        task_new = DataStorage.get_task_from_id(last)
        self.assertEquals(Status.process, task_new.is_completed)

    def test_done(self):
        last_element = len(DataStorage.load_tasks_from_json()[2])
        last = DataStorage.load_tasks_from_json()[2][last_element - 1].tid
        TaskController.complete_task(last)
        task_new = DataStorage.get_task_from_id(last)
        self.assertEquals(Status.done, task_new.is_completed)

    def test_undone(self):
        last_element = len(DataStorage.load_tasks_from_json()[2])
        last = DataStorage.load_tasks_from_json()[2][last_element - 1].tid
        TaskController.uncomplete_task(last)
        task_new = DataStorage.get_task_from_id(last)
        self.assertEquals(Status.undone, task_new.is_completed)

    def test_order_by_priority(self):

        new_task = Task("Test_task", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
                        datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
                        [], None, datetime.strptime("12:00", "%H:%M"), Priority.low, None, None)
        TaskController.add(new_task)
        before = len(TaskController.order_by_priority(Priority.low))
        TaskController.add(new_task)
        after = len(TaskController.order_by_priority(Priority.low))

        self.assertEqual(before + 1, after)

    def test_order_by_tag(self):
        new_task = Task("Test_task", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
                        datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
                        [], None, datetime.strptime("12:00", "%H:%M"), Priority.low, None, None)
        tag_name = new_task.tag.tag_name
        tag = Tag(tag_name)
        TaskController.add(new_task)
        before = len(TaskController.order_by_tag(tag))
        TaskController.add(new_task)
        after = len(TaskController.order_by_tag(tag))

        self.assertEqual(before + 1, after)

    def test_deletion(self):
        new_task = Task("Test_task", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
                        datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
                        [], None, datetime.strptime("12:00", "%H:%M"), Priority.high, None, None)

        TaskController.add(new_task)
        before_deleting = len(DataStorage.load_tasks_from_json()[0])
        TaskController.delete(new_task.tid)

        after_deleting = len(DataStorage.load_tasks_from_json()[0])
        self.assertEqual(after_deleting + 1, before_deleting)

    # endregion

    # region Test scheduler region

    def test_create_scheduler(self):
        len_before = len(DataStorage.load_schedulers_from_json())

        scheduler = Scheduler(datetime.now(), task, 12)
        SchedulerController.add(scheduler)
        len_after = len(DataStorage.load_schedulers_from_json())
        self.assertEquals(len_before + 1, len_after)

    def test_get_scheduler(self):
        new_task = Task("Test_task", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
                        datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
                        [], None, datetime.strptime("12:00", "%H:%M"), Priority.high, None, None)

        len_of_tasks_before = len(DataStorage.load_tasks_from_json()[0])
        scheduler = Scheduler(datetime.now() - timedelta(days=1), new_task, 0)
        SchedulerController.add(scheduler)
        SchedulerController.get()
        len_of_tasks_after = len(DataStorage.load_tasks_from_json()[0])
        self.assertEquals(len_of_tasks_before + 1, len_of_tasks_after)

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

    def test_user_adding(self):
        new_user = User(Faker().name(),
                        Faker().name(),
                        serialization_utils.tid_gen(),
                        Faker().name(),
                        True)
        self.assertIsInstance(new_user, User)

    def test_get_current_user(self):
        user = UserTools.get_current_user()
        self.assertIsInstance(user, User)

    # endregion

    # region Wrong data tests

    def test__wrong_change_user(self):
        new_login = Faker().name()
        new_login *= 2
        self.assertRaises(Exception, UserTools.set_current_user, new_login)

    def test_empty_edit_field(self):
        self.assertRaises(Exception, TaskController.edit, "df", "title")

    def test_wrong_index_request(self):
        len_data = len(DataStorage.load_tasks_from_json()[0])
        self.assertRaises(IndexError, DataStorage.get_subtasks, len_data + 1)

    # endregion

    # region Models tests
    def test_task_adding(self):
        self.assertIsInstance(task, Task)

    def test_tag_adding(self, name="tag name", description="tag desc"):
        new_tag = Tag(name, description)
        self.assertIsInstance(new_tag, Tag)
        self.assertEquals(new_tag.tag_name, name)
        self.assertEquals(new_tag.description, description)

    def test_priority_ading(self):
        priority = Priority.high
        self.assertIsInstance(priority, Priority)

    def test_status_ading(self):
        status = Status.done
        self.assertIsInstance(status, Status)

    def test_scheduler_creating(self):
        scheduler = Scheduler(datetime.now(), task, 12)
        self.assertIsInstance(scheduler, Scheduler)

    # endregion

    # region Data Storage test

    def test_loading_tasks(self):
        tasks = DataStorage.load_tasks_from_json()[0]
        for task in tasks:
            self.assertIsInstance(task, Task)

    def test_ordered_tasks(self):
        fake_tag = Faker().state()
        task.tag = Tag(fake_tag)
        TaskController.add(task)
        task.tag = Tag(fake_tag)
        ordered_tasks = TaskController.order_by_tag(task.tag)
        for order_task in ordered_tasks:
            self.assertEquals(fake_tag, order_task.tag.tag_name)

    def test_archieve(self):
        archieved_tasks = TaskController.archieve()
        tasks_count = len(DataStorage.load_tasks_from_json()[1])
        if tasks_count != 0:
            for task in archieved_tasks:
                self.assertEquals(task.is_completed, Status.done)

    def test_usage_of_empty_path(self):
        DataStorage.PATH = None
        # Check any method of DataStorage. They should raise exception, cause of empty PATH
        self.assertRaises(Exception, DataStorage.load_tasks_from_json)
        DataStorage.PATH = config.DATA_PATH

    def test_usage_of_empty_user(self):
        DataStorage.CURRENT_USER = None
        # Check any method of DataStorage. They should raise exception, cause of empty CURRENT USER
        self.assertRaises(Exception, DataStorage.load_tasks_from_json)
        DataStorage.CURRENT_USER = UserTools.get_current_user()

    # endregion

    # region Notifications tests

    def test_adding_notification(self):
        len_before = len(DataStorage.load_notifications_from_json())

        new_task = Task("Test_task", "Test_description", datetime.strptime("2018-05-12", "%Y-%m-%d"),
                        datetime.strptime("2018-06-12", "%Y-%m-%d"), Tag("tag_test"), DataStorage.CURRENT_USER.login,
                        [], None, datetime.strptime("12:00", "%H:%M"), Priority.high, None, None)

        TaskController.add(new_task)
        NotificationController.add(datetime.now(), new_task.tid, new_task.title)
        len_after = len(DataStorage.load_notifications_from_json())
        self.assertEqual(len_before + 1, len_after)

    # endregion

    def get_by_tid(self, tid):
        tasks = DataStorage.load_tasks_from_json()[1]
        for task in tasks:
            if task.tid == tid:
                return task
        raise Exception("There is no such task")
