import datetime

from django.db import models


# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    date = models.DateField(default=datetime.date.today())
