from .models import Task, SchedulerModel
from django.utils import timezone
from datetime import datetime, timedelta


def scheduler(func):
    def wrapper(user, *args, **kwargs):
        schedulers = [scheduler for scheduler in SchedulerModel.objects.filter(author=user)]
        for scheduler in schedulers:
            if scheduler.last_added + timedelta(days=scheduler.interval) < timezone.now():
                new = Task.objects.create(
                    title=scheduler.title,
                    description=scheduler.description,
                    start_date=scheduler.start_date,
                    end_date=scheduler.end_date,
                    author=scheduler.author,
                    tag=scheduler.tag,
                    priority=scheduler.priority,
                    parent=None,status=0,
                )
                new.subscribers.add(user)
                new.save()
                scheduler = SchedulerModel.objects.get(id=scheduler.id)
                scheduler.last_added = timezone.now()
                scheduler.save()
        return func(user, *args, **kwargs)
    return wrapper

def get_schedulers(user):
    return [scheduler for scheduler in SchedulerModel.objects.filter(author=user)]

@scheduler
def get_user_tasks(user):
    tasks = [upr for upr in Task.objects.filter(subscribers=user, parent=None)]
    return tasks

@scheduler
def get_subtasks(user, parent_task):
    subtasks = [subtask for subtask in Task.objects.filter(author=user, parent=parent_task)]
    return subtasks

@scheduler
def order_by_status(user, status):
    tasks = [upr for upr in Task.objects.filter(status=status, author=user)]
    return tasks



