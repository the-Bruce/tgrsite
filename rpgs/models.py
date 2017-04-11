from django.db import models
from django.utils.safestring import mark_safe, mark_for_escaping
from django.urls import reverse

from users.models import Member

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
	description = models.TextField(blank=True)

	players_wanted = models.IntegerField()

	# players
	members = models.ManyToManyField(Member, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	# get string name of timeslot
	def timeslot_str(self):
		return self.TIMESLOT_CHOICES[self.timeslot][1]
		# TODO TODO TODO TODO TODO
		# ^ ???

	# The timeslot system was imagined based on the Society's current RPG days
	# (Saturday and Thursday), though this means that
	# a) if the society changes these again, this will need to be updated; and
	# b) it's not very helpful for people running at other times.
	# In the future it might be better to change this to a simple charfield
	# I think mostly I wanted a chance to use the choices thing
	THURSDAY = 0
	SATURDAY_A = 1
	SATURDAY_B = 2
	OTHER_TIME = -1
	TIMESLOT_CHOICES = (
		(THURSDAY, 'Thursday evening'),
		(SATURDAY_A, 'Saturday afternoon'),
		(SATURDAY_B, 'Saturday evening'),
		(OTHER_TIME, 'See description'),
	)
	timeslot = models.IntegerField(choices=TIMESLOT_CHOICES)

# an individual session of a game, run on a specific date
# currently not used by the site frontend
class Session(models.Model):
	def __str__(self):
		date = self.plan_date
		return self.game.title + ' ' + date.strftime('%d %b')
	game = models.ForeignKey(Rpg)

	# when it's planned to run
	plan_date = models.DateField()

	# optional set of notes for the GMs to scribble in
	gm_notes = models.TextField(blank=True)
