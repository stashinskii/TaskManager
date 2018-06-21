from django.db import models




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
    author = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATUS)
    priority = models.IntegerField(choices=PRIORITY)

    def __str__(self):
        return "%s %s " % (self.title, self.id)

    class Meta:
        verbose_name="Title"
        verbose_name_plural="Titles"

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
