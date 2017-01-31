from django.test import TestCase

# Models
from django.contrib.auth.models import User
from users.models import Member
from .models import *

from users.views import spawn_user

class Messaging(TestCase):
	def setUp(self):
		spawn_user('Alice', 'alice@tagarople.com', 'ySLLe8uy')
		spawn_user('Bob', 'bob@tagarople.com', 'X3u9C4bp')
		spawn_user('Eve', 'eve@shady.site', '5rX6zrQm')

	def test_direct_message(self):
		alice = User.objects.get(username='Alice')
		bob = User.objects.get(username='Bob')
		eve = User.objects.get(username='Eve')
		# TODO: Tests
