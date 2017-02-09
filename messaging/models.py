from django.db import models

from users.models import Member

class MessageThread(models.Model):
	# todo: allow renaming of group chats? :P
	# seems simple enough
	def __str__(self):
		l = list(self.participants.all())
		return str(', '.join([str(x) for x in l]))

	participants = models.ManyToManyField(Member)

	# retrieve the single MessageThread containing exactly this set of users
	# function can take list of Members as arguments, or as an iterable collection
	def get_thread(*participants_exactly):
		from django.db.models import Count

		# Selects the threads with the correct number of participants
		query = MessageThread.objects.annotate(num_participants=Count('participants')).filter(num_participants=len(participants_exactly))

		# excludes threads that don't contain every symbol
		for x in participants_exactly:
			query = query.filter(participants=x)


		thread, created = query.get_or_create()
		if created:
			for x in participants_exactly:
				thread.participants.add(x)
			
		return thread

	def get_messages(self):
		return self.message_set.order_by('timestamp')
	def get_latest(self):
		return self.message_set.latest(field_name='timestamp')

class Message(models.Model):
	def __str__(self):
		return str(self.sender) + ': ' + str(self.content)
	thread = models.ForeignKey(MessageThread)
	sender = models.ForeignKey(Member)
	content = models.CharField(blank=False, max_length=4096)
	timestamp = models.DateTimeField(auto_now_add=True)
