import unittest

from task_manager_library.models.task_model import Task, Priority, Status, Tag


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task()

    def test_title(self):
        self.assertIsNone(self.task.title)

    def test_task_id(self):
        self.assertIsInstance(self.task.tid, str)

    def test_priority(self):
        self.assertEqual(self.task.priority, Priority.LOW)

    def test_connection_list(self):
        self.assertIsInstance(self.task.connection, list)

    def test_status(self):
        self.assertEqual(self.task.is_completed, Status.UNDONE)

    def test_complete(self):
        self.task.complete()
        self.assertEqual(self.task.is_completed, Status.DONE)

    def test_begin(self):
        self.task.begin()
        self.assertEqual(self.task.is_completed, Status.PROCESS)


