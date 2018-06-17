import unittest

from task_manager_library.models.task_model import Task, Priority, Status, Tag
from task_manager_library.models.user_model import User
from datetime import datetime, timedelta
from task_manager_library.models.scheduler_model import Scheduler
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.controllers.scheduler_controller import SchedulerController
from task_manager_library.storage.task_storage import Storage
from task_manager_library.storage.scheduler_storage import SchedulerStorage
import uuid


class TestSchedulerController(unittest.TestCase):
    def setUp(self):
        self.storage = Storage({'storage_path': '/tmp/tman_tests/'})
        self.scheduler_storage = SchedulerStorage({'storage_path': '/tmp/tman_tests/'})
        self.user = User("test_user", "test", "test ")
        self.storage.save_new_user_to_json(self.user)
        self.storage.change_user_config(self.user.login)
        self.task_controller = TaskController(self.storage)
        self.scheduler = Scheduler()
        self.scheduler_controller = SchedulerController(self.scheduler_storage, self.storage)
        self.storage.load_user_tasks()

    def test_add_scheduler(self):
        task = Task("Hello, world")
        scheduler = Scheduler(task=task, uid=self.storage.current_uid)
        len_before = len(self.scheduler_controller.get())
        self.scheduler_controller.add(scheduler)
        len_after = len(self.scheduler_controller.get())
        self.assertEqual(len_before + 1, len_after)

    def test_get_scheduler(self):
        last = datetime.now() - timedelta(days=10)
        task = Task("Hello, world")
        scheduler = Scheduler(last=last, task=task, uid=self.storage.current_uid)

        self.scheduler_controller.add(scheduler)
        new_scheduler = self.scheduler_controller.get()[-1]
        self.task_controller.task_storage.load_tasks_from_json()
        len_before = len(self.task_controller.task_storage.tasks)

        self.scheduler_controller.generate_task(new_scheduler)

        self.task_controller.task_storage.load_tasks_from_json()
        len_after = len(self.task_controller.task_storage.tasks)
        self.assertEqual(len_before+1, len_after)

    # region Instance Creation

    def test_last(self):
        self.assertIsNone(self.scheduler.last)

    def test_task(self):
        self.assertIsInstance(self.scheduler.task, Task)

    def test_sid(self):
        self.assertIsInstance(self.scheduler.sid, str)

    def test_uid(self):
        self.assertIsNone(self.scheduler.uid)

    def test_interval(self):
        self.assertEqual(self.scheduler.interval, 0)

    # endregion

