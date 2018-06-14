import json
import os
from datetime import datetime
import uuid

from task_manager_library.utility import utils
from task_manager_library.storage import serialization
import configparser


class SchedulerStorage:
    def __init__(self, configuration=None, external_user=None):
        if configuration is not None and configuration.get('storage_path') is not None:
            self.path = configuration.get('storage_path')
        else:
            self.path = os.path.dirname(__file__) + "/tmandata/"
        if external_user is not None:
            self.current_uid = external_user
        else:
            try:
                utils.check_json_files(self.path, 'users.json')
                utils.check_cfg_files(self.path, 'current.ini')
                config = configparser.ConfigParser()
                config.read(self.path+'current.ini')
                section = "USER"
                uid = config.get(section, "uid")
                self.current_uid = uid
            except Exception as e:
                self.current_uid = None
        self.schedulers = []
        self.user_schedulers = []

    def load_schedulers_from_json(self):
        utils.check_json_files(self.path, '/schedulers.json')

        if self.schedulers:
            return

        with open(self.path + 'schedulers.json', 'r') as scheduler_file:
            scheduler_data = json.load(scheduler_file)

        for task_dict in scheduler_data:
            loaded_scheduler = serialization.dict_to_scheduler(task_dict)
            self.schedulers.append(loaded_scheduler)

    def load_user_schedulers(self):
        if not self.schedulers:
            self.load_schedulers_from_json()

        if self.user_schedulers:
            return

        self.user_schedulers = [scheduler for scheduler in self.schedulers
                                if scheduler.uid == self.current_uid]


    def add_scheduler(self, scheduler):
        self.load_schedulers_from_json()
        self.schedulers.append(scheduler)
        self.resave()

    def update(self, sid):
        index = utils.get_scheduler_index(sid, self)
        self.schedulers[index].last = datetime.now()
        self.schedulers[index].task.tid = str(uuid.uuid1())
        self.resave()

    def resave(self):
        data = []
        for scheduler in self.schedulers:
            scheduler = serialization.scheduler_to_dict(scheduler)
            data.append(scheduler.__dict__)

        with open(self.path + '/schedulers.json', 'w') as scheduler_file:
            json.dump(data, scheduler_file, indent=2, ensure_ascii=False)