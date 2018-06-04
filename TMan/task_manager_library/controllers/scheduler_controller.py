from task_manager_library.data_storage import DataStorage


class SchedulerController():

    @staticmethod
    def add(scheduler):
        DataStorage.save_scheduler_to_json(scheduler)

    @staticmethod
    def get():
        schedulers = DataStorage.load_schedulers_from_json()
        for scheduler in schedulers:
            if datetime.now().date() >= scheduler.date.date():
                all_tasks = DataStorage.load_tasks_from_json()[2]
                all_tasks.append(scheduler.task)
                DataStorage.resave_all_tasks_to_json(all_tasks, scheduler.task)
                DataStorage.delete_scheduler_from_json(scheduler)