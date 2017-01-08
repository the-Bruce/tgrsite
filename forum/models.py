from django.db import models
from users.models import Member

# Forum for threads to be inside
class Forum(models.Model):
	def __str__(self):
		return self.title

	# subforuming
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	title = models.CharField(max_length=64)
	title.verbose_name = 'Name'
	def get_subforums(self):
		return Forum.objects.filter(parent=self.id)
	def get_subforums_str(self):
		return [str(x) for x in self.get_subforums()]
	get_subforums.short_description='Subforums'
	get_subforums_str.short_description='Subforums'

	def get_parentless_forums():
		return Forum.objects.filter(parent__isnull=True)

# Forum thread
class Thread(models.Model):
	# TODO: implement pinned posts in rendering
	def __str__(self):
		return self.title

	def get_author(self):
		return Member.objects.get(id=self.author.id)
	get_author.short_description = 'Author'

	forum = models.ForeignKey(Forum, on_delete = models.CASCADE)

	title = models.CharField(max_length=64)
	body = models.CharField(max_length=8192)
	pub_date = models.DateField('date published')

	is_pinned = models.BooleanField(default=False)

	# we should not be "hard" deleting users
	author = models.ForeignKey(Member, on_delete=models.PROTECT)

class Response(models.Model):
	def __str__(self):
		return self.body

	def get_author(self):
		return Member.objects.get(id=self.author.id)
	get_author.short_description = 'Author'

	# when a thread is deleted its responses are deleted
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	# Do thread responses need titles?
	body = models.CharField(max_length=8192)
	pub_date = models.DateField('date posted')
	author = models.ForeignKey(Member, on_delete=models.PROTECT)
