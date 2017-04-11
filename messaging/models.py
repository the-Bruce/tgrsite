from django.db import models

from users.models import Member
class MessageThread(models.Model):
	def __str__(self):
		l = list(self.participants.all())
		return str(', '.join([str(x) for x in l]))

	participants = models.ManyToManyField(Member)

	# latest five messages
	def five(self):
		# for some reason reverse() doesn't do what we want
		# when you use slices, it messes with it.
		# List()[::-1] is beautiful pythonic code to reverse a list
		# [start:end] is common but [start:end:step] is possible
		# and as always Python handles negatives nicely
		return self.get_messages().reverse()[:5][::-1]

	# @param *pals_str list of usernames (strings) of involved members
	# @return the messagethread containing exactly these users (created if none exists)
	def get_thread_from_str(*pals_str):
		members = (Member.objects.get(equiv_user__username=x) for x in pals_str)
		return MessageThread.get_thread(*members)

	# retrieve the single MessageThread containing exactly this set of users
	# function can take list of Members as arguments, or as an iterable collection, because Python
	def get_thread(*participants_exactly):
		from django.db.models import Count

		# Selects the threads with the correct number of participants
		query = MessageThread.objects.annotate(num_participants=Count('participants')).filter(num_participants=len(participants_exactly))

		# make sure each participant is in the set
		for x in participants_exactly:
			query = query.filter(participants=x)

		# we now have a strong enough condition:
		# if we have exactly the right number of people,
		# and no person looked for is absent,
		# then therefore the list of present is exactly the list of people looked for!

		thread, created = query.get_or_create()
		# so if after all that, no thread exists, we need to make it and add people in
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
