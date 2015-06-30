from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Paper(models.Model):
    title = models.CharField(max_length=1000)
    abstract = models.TextField(max_length=1000000)
    user = models.ForeignKey(User)
    def __str__(self):
        return self.title+" ("+self.user.username+")"

class Author(models.Model):
    name = models.CharField(max_length=255)
    papers = models.ManyToManyField(Paper)
    user = models.ForeignKey(User)
    def __str__(self):
        return self.name+" ("+self.user.username+")"


