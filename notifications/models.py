from django.db import models

from users.models import Member
from django.utils import timezone

# TODO:
# Consider merging notifications of the same type. How do we do this???

# Create your models here.
class Notification(models.Model):
	member = models.ForeignKey(Member, related_name='notifications_owned', on_delete=models.CASCADE)
	notify_type = models.CharField(max_length=32)
	url = models.CharField(max_length=512)
	content = models.TextField(max_length=8192)
	unread = models.BooleanField()
	time = models.DateTimeField()

	def notify_icon(self):
		icons = {
			'newsletter': 'fa-newspaper-o',
			'message_received': 'fa-commenting-o',
			'rpg_join': 'fa-sign-in',
			'rpg_leave': 'fa-sign-out',
			'rpg_kick': 'fa-times',
			'rpg_added': 'fa-magic',
			'forum_reply': 'fa-quote-right'
		}
		default_icon = 'fa-circle'
		if self.notify_type in icons:
			return icons[self.notify_type]
		else:
			return default_icon

def notify(member, notify_type, content, url):
	n = Notification.objects.create(member=member, notify_type=notify_type, content=content, url=url, unread=True, time=timezone.now())
	# TODO: Needs to limit number of notifications stored.
	# Likely here just check if >50, if so delete the last.
	n.save()

def notify_all(notify_type, content, url):
	for m in Member.objects.all(): notify(m, notify_type, content, url)
