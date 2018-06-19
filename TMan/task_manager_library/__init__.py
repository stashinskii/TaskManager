r"""
This library designed to use in task manager

How to use library in your app:

Firstly, import this library:
    >>> import task_manager_library

There are 2 main task controllers, designed to manage your entities, receive request from
app, return objects and exceptions

Main entities represents in models:

1. Task
2. Priority
3. Status
4. Tag
5. Scheduler

It use JSON serializator for manage data in Storage and SchedulerStorage classes. SchedulerStorage
designed for managing scheduler data at JSON files.

Storage:

Firstly, class initialize new json files if needed

    >>> from task_manager_library.storage import task_storage

To load data and deserialize it use:
    >>> task_storage.load_tasks_from_json()

It stores data in Storage - tasks
To get users tasks use:
    >>> task_storage.load_user_tasks()

It stores data in Storage - user_tasks
To get more information - get help on task_manager_library.storage.task_storage

Same actions used for SchedulerStorage

TaskController:
Designed for managing tasks

To create instance, send Storage's object

For more help use help on task_manager_library.controollers.task_controller


"""

