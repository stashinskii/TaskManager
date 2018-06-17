import unittest

from task_manager_library.models.user_model import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_name(self):
        self.assertIsNone(self.user.name)

    def test_uid(self):
        self.assertIsInstance(self.user.uid, str)