from django.db import models

from users.models import Member
from django.utils import timezone
from datetime import timedelta

# TODO:
# Consider merging notifications of the same type. How do we do this???
# COULD MERGE BY URL

class NotifType:
	NEWSLETTER = 1
	MESSAGE = 2
	RPG_JOIN = 3
	RPG_LEAVE = 4
	RPG_KICK = 5
	RPG_ADDED = 6
	FORUM_REPLY = 7
	OTHER = 8

class Notification(models.Model):
	notification_types = [
		(NotifType.NEWSLETTER, 'Newsletter'),
		(NotifType.MESSAGE, 'Message Received'),
		(NotifType.RPG_JOIN, 'Joined RPG'),
		(NotifType.RPG_LEAVE, 'Left RPG'),
		(NotifType.RPG_KICK, 'Kicked from RPG'),
		(NotifType.RPG_ADDED, 'Added to RPG'),
		(NotifType.FORUM_REPLY, 'Replied to Forum'),
		(NotifType.OTHER, 'Other Notification')
	]
	member = models.ForeignKey(Member, related_name='notifications_owned', on_delete=models.CASCADE)
	notif_type = models.IntegerField(choices=notification_types, default=NotifType.OTHER)
	url = models.CharField(max_length=512)
	content = models.TextField(max_length=8192)
	is_unread = models.BooleanField()
	time = models.DateTimeField()

	def notify_icon(self):
		default_icon = 'fa-circle'
		icons = {
			NotifType.NEWSLETTER: 'fa-newspaper-o',
			NotifType.MESSAGE: 'fa-commenting-o',
			NotifType.RPG_JOIN: 'fa-sign-in',
			NotifType.RPG_LEAVE: 'fa-sign-out',
			NotifType.RPG_KICK: 'fa-times',
			NotifType.RPG_ADDED: 'fa-magic',
			NotifType.FORUM_REPLY: 'fa-quote-right',
			NotifType.OTHER: default_icon
		}
		if self.notif_type in icons:
			return icons[self.notif_type]
		else:
			return default_icon

def notify(member, notif_type, content, url):
	n = create_notification(member, notif_type, content, url)
	n.save()
	delete_old(member)

def create_notification(member, notif_type, content, url):
	return Notification(member=member, notif_type=notif_type, content=content, url=url, is_unread=True, time=timezone.now())

def delete_old(member):
	week_ago = timezone.now() - timedelta(days=7)
	Notification.objects.filter(member=member, is_unread=False, time__lt=week_ago).delete()

def delete_all_old():
	week_ago = timezone.now() - timedelta(days=7)
	Notification.objects.filter(is_unread=False, time__lt=week_ago).delete()

def notify_everybody(notif_type, content, url):
	notifications = [create_notification(m, notif_type, content, url) for m in Member.objects.all()]
	Notification.objects.bulk_create(notifications)
	delete_all_old()
