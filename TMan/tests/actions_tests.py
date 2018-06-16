import unittest

from task_manager_library.models.task_model import Task, Priority, Status, Tag
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.storage.task_storage import Storage
import uuid


class TestTaskController(unittest.TestCase):
    def set_up(self):
        self.storage = Storage({'path': '/tmp/tman_tests/'}, uuid.uuid1())
        self.task_controller = TaskController(self.storage)
        self.task = Task()

    def test_add_task(self):
        self.set_up()
        self.task_controller.add(self.task)
        self.task_controller.get_list()
        self.assertIn(self.task, self.storage.user_tasks)

    def test_edit_task(self):
        self.set_up()
        self.task_controller.get_list()
        self.task_controller.edit(self.task.tid, title='hello')
        print(self.storage.current_uid)
        #edited_task = self.task_controller.get_task(self.task.tid)
        #self.assertEqual(edited_task, 'hello')




