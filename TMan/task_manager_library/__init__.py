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

It use JSON serializator for manage data in Storage and SchedulerStorage
classes. SchedulerStorage designed for managing scheduler data at JSON files.
----------------------------------------------------------------------------------------------

-- USAGE --

-- STORAGE USAGE --

0. Firstly, class initialize new json files if needed
    >>> from task_manager_library.storage import task_storage

1. Create new storage instance
    >>> task = Storage()
    Or send new path to storage:
    >>> task = Storage("new/path")
2. Use storage methods like this:
    >>> task.load_tasks_from_json()

After loading tasks: task.load_tasks_from_json() you may get
access to your tasks by using task.tasks

To get more information - get help on task_manager_library.storage.task_storage

----------------------------------------------------------------------------------------------

-- TASK CONTROLLER USAGE --
Main thing which is manage your library is TaskController

How to work with your controller:
0. Import your TaskController module from library:
    >>> from task_manager_library.controllers.task_controller import TaskController
1. Create TaskController instance
    >>> task_controller = TaskController(storage)
    storage - is instance of Storage class (information how to create it written in Storage part)
2. Use methods to manage you task manager!

Examples of usage TaskController:
1. Add new task:
    >>> task = Task(title="New title", Tag("tag-name"))
    >>> task_controller.add(task)

2. Edit task
    >>> task_controller.edit("55545s6d-45ds456ds456d-s45d6s46dsds", title="New title")

3. Delete task
    >>> task_controller.delete("55545s6d-45ds456ds456d-s45d6s46dsds")

Import module and use help to get more methods





"""

