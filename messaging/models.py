from django.db import models

from users.models import Member


class MessageThread(models.Model):
    participants = models.ManyToManyField(Member)
    title = models.CharField(max_length=64, blank=True)

    def __str__(self):
        if self.title != '':
            return self.title
        else:
            return ', '.join([str(x) for x in self.participants.all()])

    # latest five messages
    def five(self):
        return self.get_messages().reverse()[:5]

    def get_messages(self):
        return self.message_set.order_by('timestamp')

    def get_latest(self):
        return self.message_set.latest(field_name='timestamp')


class Message(models.Model):
    def __str__(self):
        return str(self.sender) + ': ' + str(self.content)

    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.CharField(blank=False, max_length=4096)
    timestamp = models.DateTimeField(auto_now_add=True)
