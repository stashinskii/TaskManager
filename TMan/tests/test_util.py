import unittest

from task_manager_library.models.task_model import Task, Priority, Status, Tag
from task_manager_library.models.user_model import User
from task_manager_library.controllers.task_controller import TaskController
from task_manager_library.storage.task_storage import serialization
from task_manager_library import utility
import uuid
from datetime import datetime

class TestUtils(unittest.TestCase):
    def test_serialization(self):
        task = Task(start=datetime.now(),
                    end=datetime.now(),
                    priority=Priority.HIGH,
                    tag=Tag("Name"))
        dict_task = serialization.task_to_dict(task).__dict__

        self.assertIsInstance(dict_task['start'], str)
        self.assertIsInstance(dict_task['end'], str)
        self.assertIsInstance(dict_task['priority'], str)

    def test_deserialize(self):
        task=Task()
        task_dict = serialization.task_to_dict(task).__dict__
        task = serialization.dict_to_task(task_dict)
        self.assertIsInstance(task.priority, Priority)

    def test_str_to_date(self):
        str_date = "2018-02-08"
        date = utility.utils.str_to_date(str_date)
        self.assertIsInstance(date, datetime)

    def test_str_to_time(self):
        str_time = "12:00"
        time = utility.utils.str_to_time(str_time)
        self.assertIsInstance(time, datetime)

    def test_date_to_str(self):
        date = datetime.now()
        str_date = serialization.date_to_str(date)
        self.assertIsInstance(str_date, str)

    def test_time_to_str(self):
        time = datetime.now()
        str_time = serialization.date_to_str(time)
        self.assertIsInstance(str_time, str)