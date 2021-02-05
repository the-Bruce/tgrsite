from django.db import models

from users.models import Member


class MessageThread(models.Model):
    participants = models.ManyToManyField(Member)
    title = models.CharField(max_length=64, blank=True)
    dmthread = models.BooleanField(default=False)

    def __str__(self):
        return self.title or (', '.join([str(x) for x in self.participants.all()]))

    # latest five messages
    def five(self):
        return self.get_messages().reverse()[:5]

    def get_messages(self):
        return self.message_set.filter(deleted__isnull=True).order_by('timestamp')

    def get_latest(self):
        return self.message_set.filter(deleted__isnull=True).latest('timestamp')

    def reported(self):
        return self.message_set.filter(messagereport__resolved=False)


class Message(models.Model):
    def __str__(self):
        return str(self.sender) + ': ' + str(self.content)

    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.CharField(blank=False, max_length=4096)
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = (
            ("can_moderate", "Can moderate message threads"),
        )

    @property
    def reports(self):
        return self.messagereport_set.filter(resolved=False)


class MessageReport(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    resolution = models.TextField(blank=True)

    def __str__(self):
        return f"{self.member.username}: {self.message.content[:35]}"