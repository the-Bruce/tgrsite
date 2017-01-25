from django.db import models

from users.models import Member

class ExecRole(models.Model):
	def __str__(self):
		return "{0} ({1})".format(self.role_title, str(self.incumbent))

	# numerical value to use for sorting
	# sorted ascending
	# eg if you wanted president to go first
	# give them 0
	sort_order = models.IntegerField(default=0)
	sort_order.help_text = 'Lower values are earlier in the list'

	# name of the exec role eg "president"
	role_title = models.CharField(max_length=32)

	# long description of the role for the site
	bio = models.TextField(blank=True)
	bio.help_text = 'Description of the role and what it entails, as well as a short personal bio.'

	# current member who is filling the role
	incumbent = models.ForeignKey(Member, null=True, blank=True)
	incumbent.help_text = 'Member who is currently in this role'
