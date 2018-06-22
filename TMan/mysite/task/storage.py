from .models import Task

def get_user_tasks(user):
    tasks = [upr for upr in Task.objects.filter(author=user)]
    return tasks