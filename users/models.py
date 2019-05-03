import hashlib
import urllib.parse as urllib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import Q


# extension to django's User class which has authentication details
# as well as some basic info such as name
class Member(models.Model):
    equiv_user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=4096, blank=True)
    signature = models.TextField(max_length=1024, blank=True)
    official_photo_url = models.CharField(max_length=512, null=True, blank=True)


    def gravatar(self, size=128):
        default = "https://pbs.twimg.com/media/Civ9AUkVAAAwihS.jpg"
        h = hashlib.md5(
            self.equiv_user.email.encode('utf8').lower()
        ).hexdigest()
        q = urllib.urlencode({
            # 'd':default,
            'd': 'identicon',
            's': str(size),
        })

        return 'https://www.gravatar.com/avatar/{}?{}'.format(h, q)

    def __str__(self):
        return self.equiv_user.username

    def notification_count(self):
        return len(self.notifications_owned.filter(is_unread=True))

    def is_exec(self):
        return len(self.execrole_set.all()) > 0

    @staticmethod
    def users_with_perm(perm_name):
        return Member.objects.filter(
            Q(equiv_user__is_superuser=True) |
            Q(equiv_user__user_permissions__codename=perm_name) |
            Q(equiv_user__groups__permissions__codename=perm_name)).distinct()