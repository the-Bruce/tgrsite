from django.db import models
from django.contrib.auth.models import User
import urllib.parse as urllib
import hashlib

# extension to django's User class which has authentication details
# as well as some basic info such as name
class Member(models.Model):
	def gravatar(self, size=128):
		default="https://pbs.twimg.com/media/Civ9AUkVAAAwihS.jpg"
		h = hashlib.md5(
			self.equiv_user.email.encode('utf8').lower()
		).hexdigest()
		q = urllib.urlencode({
			#'d':default,
			'd': 'identicon',
			's':str(size),
		})

		return 'https://www.gravatar.com/avatar/{}?{}'.format(h, q)

	equiv_user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.equiv_user.username
	bio = models.CharField(max_length=4096, blank=True)
	signature = models.CharField(max_length = 1024, blank=True)

	def notification_count(self):
		return len(self.notifications_owned.filter(is_unread=True))

	official_photo_url = models.CharField(max_length=512, null=True, blank=True)

	def is_exec(self):
		return len(self.execrole_set.all()) > 0