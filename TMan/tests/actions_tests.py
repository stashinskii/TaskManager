import unittest

from task_manager_library.models.task_model import Task, Priority, Status, Tag
from task_manager_library.models.user_model import User
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.storage.task_storage import Storage
import uuid
import shutil



class TestTaskController(unittest.TestCase):
    def setUp(self):
        self.storage = Storage({'storage_path': '/tmp/tman_tests/'})

        self.user = User("test_user", "test", "test ")
        self.storage.save_new_user_to_json(self.user)
        self.storage.change_user_config(self.user.login)

        self.task_controller = TaskController(self.storage)
        self.task = Task()
        self.storage.load_user_tasks()

    def test_add_task(self):
        task = Task()
        self.task_controller.add(task)
        self.task_controller.get_list()
        self.assertIn(task, self.storage.tasks)

    def test_delete_task(self):

        tid = self.storage.tasks[-1].tid
        len_before = len(self.task_controller.task_storage.tasks)
        self.task_controller.delete(tid)
        len_after = len(self.task_controller.task_storage.tasks)
        self.assertEqual(len_after + 1, len_before)

    def test_complete(self):
        task = Task()

        self.task_controller.add(task)
        tid = self.task_controller.get_list()[-1].tid

        self.task_controller.complete_task(tid)

        loaded_task = self.task_controller.get_task(tid)
        self.assertEqual(str(Status.done.value), loaded_task.is_completed)

    def test_begin(self):
        task = Task()

        self.task_controller.add(task)
        tid = self.task_controller.get_list()[-1].tid

        self.task_controller.begin_task(tid)

        loaded_task = self.task_controller.get_task(tid)
        self.assertEqual(str(Status.process.value), loaded_task.is_completed)

    def test_uncomplete(self):
        task = Task()

        self.task_controller.add(task)
        tid = self.task_controller.get_list()[-1].tid

        self.task_controller.uncomplete_task(tid)

        loaded_task = self.task_controller.get_task(tid)
        self.assertEqual(str(Status.undone.value), loaded_task.is_completed)

    def test_add_subtask(self):
        first = Task()
        second = Task(parent=first.tid)

        self.assertEqual(first.tid, second.parent)

