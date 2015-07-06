from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Paper(models.Model):
    title = models.CharField(max_length=1000)
    abstract = models.TextField(max_length=1000000)
    user = models.ForeignKey(User)
    cluster = models.IntegerField(default=0)
    length = models.IntegerField(default=60)
    def __str__(self):
        return self.title+" ("+self.user.username+")"

class Author(models.Model):
    name = models.CharField(max_length=255)
    papers = models.ManyToManyField(Paper)
    user = models.ForeignKey(User)
    def __str__(self):
        return self.name+" ("+self.user.username+")"

class ScheduleSettings(models.Model):
    settings_string = models.CharField(max_length=100000)
    schedule_string = models.CharField(max_length=100000, default=[])
    slot_length = models.IntegerField()
    num_days = models.IntegerField()
    user = models.ForeignKey(User)
    def __str__(self):
        return self.settings_string

