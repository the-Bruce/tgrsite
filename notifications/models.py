from django.db import models

from users.models import Member
from django.utils import timezone
from datetime import timedelta

# TODO:
# Consider merging notifications of the same type. How do we do this???
# COULD MERGE BY URL

class Notification(models.Model):
	member = models.ForeignKey(Member, related_name='notifications_owned', on_delete=models.CASCADE)
	notif_type = models.CharField(max_length=32)
	url = models.CharField(max_length=512)
	content = models.TextField(max_length=8192)
	is_unread = models.BooleanField()
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
		if self.notif_type in icons:
			return icons[self.notif_type]
		else:
			return default_icon

def notify(member, notif_type, content, url):
	n = Notification.objects.create(member=member, notif_type=notif_type, content=content, url=url, is_unread=True, time=timezone.now())
	n.save()
	delete_old(member)

def delete_old(member):
	week_ago = timezone.now() - timedelta(days=7)
	Notification.objects.filter(member=member, is_unread=False, time__lt=week_ago).delete()

def notify_everybody(notif_type, content, url):
	for m in Member.objects.all(): notify(m, notif_type, content, url)
