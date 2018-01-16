from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse

from users.models import Member

import re

# Create your models here.
class Rpg(models.Model):
	def __str__(self):
		return self.title

	# list of game master names
	def game_master_list(self):
		# TODO: restructure this so we don't mess with rendering inside a model i.e. use a template tag
		# array comprehension over GM list
		gmstrings = [
			# stop from escaping
			mark_safe('<a href="{}">{}</a>'.format(reverse('user', args=[x.id]), str(x)))
			for x in self.game_masters.all()
		]
		if len(gmstrings) == 0: return 'nobody'

		if len(gmstrings) == 1: return gmstrings[0]

		# [Tom, Dick, Harry] => 'Tom, Dick and Harry'
		return mark_safe(
			', '.join(gmstrings[:-1]) + ' and ' + gmstrings[-1]
		)

	# who _created_ the entry - should not change
	creator = models.ForeignKey(Member, related_name='rpgs_owned', on_delete = models.PROTECT)

	# who's listed as _running_ the game - may change
	game_masters = models.ManyToManyField(Member, related_name='rpgs_running', blank=True)

	# the game/campaign/oneshot's name, eg My Cool 5E Newbie Game
	title = models.CharField(max_length=64)
	title.verbose_name = 'Name'

	# the system that's being used, eg D&D
	system = models.CharField(max_length=64, blank=True)

	# longform description
	description = models.TextField(max_length=8192, blank=True)

	players_wanted = models.IntegerField()

	# players
	members = models.ManyToManyField(Member, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	# if the event is in the past, this should be marked
	is_in_the_past = models.BooleanField(default=False)
	is_in_the_past.help_text='Has the event already happened?'

	# It was kind of sad killing off the IntegerField because Ash said
	# they used it because they wanted to try it out, for fun. Oh well.
	timeslot = models.CharField(max_length=64, blank=True)

	def get_timeslot_or_unspecified(self):
		if re.match(r'^\s*$', self.timeslot):
			return "Unspecified, see description."
		else:
			return self.timeslot


	tags = models.ManyToManyField('Tag')
	def tags_str(self):
		return ','.join([str(x) for x in self.tags.all()])

# an individual session of a game, run on a specific date
# currently not used by the site frontend
class Session(models.Model):
	def __str__(self):
		date = self.plan_date
		return self.game.title + ' ' + date.strftime('%d %b')
	game = models.ForeignKey(Rpg, on_delete=models.PROTECT)

	# when it's planned to run
	plan_date = models.DateField()

	# optional set of notes for the GMs to scribble in
	gm_notes = models.TextField(blank=True)

# tags are a way of categorising games signups
# the previous implementation stored them on the Rpg model using a delimited string!
# which is horrible in all sorts of ways, not least that it violated 1NF :P
# rather than that mess, this solution creates a simple model with a ManyToMany relation
class Tag(models.Model):
	name = models.CharField(max_length=32)
	def __str__(self):
		return self.name
