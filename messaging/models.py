from django.db import models

from users.models import Member

class MessageThread(models.Model):
	participants = models.ManyToManyField(Member)

class Message(models.Model):
	thread = models.ManyToManyField(MessageThread)
	sender = models.ForeignKey(Member)
	content = models.CharField(blank=False, max_length=4096)

