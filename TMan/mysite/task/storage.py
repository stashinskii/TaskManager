from .models import Task

def get_user_tasks(user):
    tasks = [upr for upr in Task.objects.filter(author=user, parent=None)]
    return tasks

def get_subtasks(user, parent_task):
    subtasks = [subtask for subtask in Task.objects.filter(author=user, parent=parent_task)]
    return subtasks

def order_by_status(user, status):
    tasks = [upr for upr in Task.objects.filter(status=status, author=user)]
    return tasks

