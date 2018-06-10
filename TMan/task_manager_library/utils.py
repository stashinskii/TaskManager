def get_task_index(tid, storage):
    counter = 0
    for task in storage.tasks:
        if task.tid == tid:
            return counter
        counter+=1
    raise IndexError("Task was not found")