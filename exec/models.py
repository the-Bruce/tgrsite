from django.db import models

from users.models import Member


class ExecRole(models.Model):
    def __str__(self):
        return "{0} ({1})".format(self.role_title, str(self.incumbent))

    # sorting priority - lower number means presented further up on the list
    sort_index = models.IntegerField(default=0)
    sort_index.help_text = 'Index for sorting. Lower value = earlier in list.'

    # position name
    role_title = models.CharField(max_length=32)

    bio = models.TextField(blank=True)
    bio.help_text = 'Description of the role and what it entails, as well as a short personal bio.'

    incumbent = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)
    incumbent.help_text = 'Member who is currently in this role'
