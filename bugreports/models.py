from django.db import models
from users.models import Member
from django.urls import reverse
# if I can be bothered, could use GitHub API to integrate with repo issues tracker?
class Report(models.Model):
	datetime = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=128)
	body = models.TextField(max_length=8192)

	# currently broken - would need to customise form shit to do this zzz
	reporter = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)

	NEEDSREVIEW=None
	CLOSED=-1
	OPEN=1
	DUPLICATE=2
	WONTFIX=3
	NOTABUG=4
	STATUS_CHOICES=(
		(NEEDSREVIEW, 'Needs review'),
		(CLOSED, 'Closed'),
		(OPEN, 'Open'),
		(DUPLICATE, 'Duplicate'),
		(WONTFIX, 'Won\'t fix'),
		(NOTABUG, 'Not a bug'),
	)
	status = models.IntegerField(choices=STATUS_CHOICES, null=True)

	EXEC=1
	SCHEDULE=2
	GALLERY=3
	FORUM=4
	RPGS=5
	MESSAGES=6
	LOGIN=7
	OTHER=10
	FEATURE_CHOICES=(
		(EXEC, 'Exec page'),
		(SCHEDULE, 'Schedule'),
		(GALLERY, 'Gallery'),
		(FORUM, 'Forum'),
		(RPGS, 'RPGs app'),
		(MESSAGES, 'Messaging app'),
		(LOGIN, 'Login system'),
		(OTHER, 'Other'),
	)
	feature=models.IntegerField(choices=FEATURE_CHOICES)

	duplicate_of = models.ForeignKey('self', on_delete=models.PROTECT,null=True,blank=True)
	# related = models.ManyToManyField(...)

	dev_response=models.TextField(max_length=8192, blank=True)

	def __str__(self):
		return "[{}] {}".format(self.id, self.title)

	# Important! If this changes, change the URL too!
	def get_absolute_url(self):
		return reverse('bug_detail', kwargs={'pk': self.id})
