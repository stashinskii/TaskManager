from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default='')


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)



class SchedulerModel(models.Model):
    interval = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_added = models.DateTimeField()


    STATUS = ((0, "UNDONE"), (1, "PROCESS"), (2, "DONE"))

    PRIORITY = ((0, "LOW"), (1, "MEDIUM"), (2, "HIGH"))
    title = models.CharField(max_length=50, default="Empty title")
    description = models.CharField(max_length=250, default=None)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    tag = models.CharField(max_length=10, default="None")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    priority = models.IntegerField(choices=PRIORITY, default=2)
    parent = models.ForeignKey('self', null=True, blank=True)


class Task(models.Model):
    STATUS = (
        (0, "UNDONE"),
        (1, "PROCESS"),
        (2, "DONE")
    )

    PRIORITY = (
        (0, "LOW"),
        (1, "MEDIUM"),
        (2, "HIGH")
    )

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    tag = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    priority = models.IntegerField(choices=PRIORITY, default=2)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return "%s %s " % (self.title, self.id)

    class Meta:
        verbose_name="Title"
        verbose_name_plural="Titles"

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)


