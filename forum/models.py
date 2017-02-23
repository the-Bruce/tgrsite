from django.db import models
from users.models import Member

class Forum(models.Model):
	def __str__(self):
		return self.title
	
	parent = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		blank=True, null=True,
		related_name='subforums')

	# string that represents the forum's location
	# eg "Roleplaying / LARP / Character Sheets"
	# might be useful to generalise this for Threads
	def get_parent_tree(self):
		# root forums don't display this on the site, so this line only affects the admin page
		if self.parent is None: return '-'
		
		tree = ''
		
		# walk up through tree to root
		x = self.parent
		while True:
			tree = ' / ' + str(x) + tree
			if x.parent is not None:
				# 
				x = x.parent
			else:
				# reached root
				break
		# cut off the leading slash and space (first two characters)
		return tree[3:]

	get_parent_tree.short_description = 'location'

	title = models.CharField(max_length=64)
	title.verbose_name = 'Name'

	description = models.CharField(max_length=256, blank=True)

	def get_subforums(self):
		return Forum.objects.filter(parent=self.id)

	def get_subforums_str(self):
		return [str(x) for x in self.get_subforums()]
	get_subforums.short_description='Subforums'
	get_subforums_str.short_description='Subforums'

	def get_parentless_forums():
		return Forum.objects.filter(parent__isnull=True)

	# mostly for the sake of the admin widget
	def get_threads_count(self):
		return Thread.objects.filter(forum=self.id).count()	
	get_threads_count.short_description='threads'

class Thread(models.Model):
	def __str__(self):
		return self.title

	def get_author(self):
		return Member.objects.get(id=self.author.id)
	get_author.short_description = 'Author'

	# cascade because we need to be able to delete forums maybe?
	forum = models.ForeignKey(Forum, on_delete = models.CASCADE)

	title = models.CharField(max_length=64)
	body = models.CharField(max_length=8192)
	pub_date = models.DateTimeField('date published')

	# pinned/stickied/whatever threads will show up before all others in their forums
	is_pinned = models.BooleanField(default=False)

	# we should not be "hard" deleting users so
	author = models.ForeignKey(Member, on_delete=models.PROTECT)

	def get_response_count(self):
		return Response.objects.filter(thread=self.id).count()

class Response(models.Model):
	def __str__(self):
		return self.body

	def get_author(self):
		return Member.objects.get(id=self.author.id)
	get_author.short_description = 'Author'

	# when a thread is deleted its responses are deleted
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	body = models.CharField(max_length=8192)
	
	# TODO: auto_now_add
	pub_date = models.DateTimeField('date posted')
	author = models.ForeignKey(Member, on_delete=models.PROTECT)
