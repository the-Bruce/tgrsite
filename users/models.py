import hashlib
import urllib.parse as urllib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import Q


# extension to django's User class which has authentication details
# as well as some basic info such as name
class Member(models.Model):
    equiv_user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord = models.CharField(max_length=100, blank=True)
    pronoun = models.CharField(max_length=50, blank=True, verbose_name="pronouns")
    bio = models.TextField(max_length=4096, blank=True)
    signature = models.TextField(max_length=1024, blank=True)
    official_photo_url = models.CharField(max_length=512, null=True, blank=True)
    dark = models.BooleanField(default=False, help_text="Enable Dark Mode(beta) on this account")

    def gravatar(self, size=128):
        h = hashlib.md5(
            self.equiv_user.email.encode('utf8').lower()
        ).hexdigest()
        q = urllib.urlencode({
            'd': 'identicon',
            's': str(size),
        })
        return 'https://www.gravatar.com/avatar/{}?{}'.format(h, q)

    def badge(self):
        if self.equiv_user.is_superuser:
            return "fas fa-crown text-gold"
        elif self.is_exec():
            return "fas fa-star text-gold"
        elif self.is_ex_exec():
            return "fas fa-award text-muted"
        else:
            return False

    def __str__(self):
        return self.equiv_user.username

    def notification_count(self):
        return self.notifications_owned.filter(is_unread=True).count()

    def is_exec(self):
        return self.exec_roles.count() > 0 or self.equiv_user.groups.filter(name='exec').exists()

    def is_ex_exec(self):
        return self.equiv_user.groups.filter(name='ex_exec').exists()

    # Make .member idempotent i.e. user.member is valid even if user is actually a member
    @property
    def member(self):
        return self

    @staticmethod
    def users_with_perm(perm_name):
        return Member.objects.filter(
            Q(equiv_user__is_superuser=True) |
            Q(equiv_user__user_permissions__codename=perm_name) |
            Q(equiv_user__groups__permissions__codename=perm_name)).distinct()
