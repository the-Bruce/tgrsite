from django.test import TestCase

# Models
from django.contrib.auth.models import User
from users.models import Member
from .models import Message, MessageThread
from .views import send_message

from users.views import spawn_user

# useful utility function to find members by username
# I should maybe actually put this in like users.members
def get_member(*usernames):
	members = []
	for x in usernames:
		members.append(User.objects.get(username=x).member)
	return tuple(members)

class Messaging(TestCase):
	def setUp(self):
		a_user = spawn_user('Alice', 'alice@tagarople.com', 'ySLLe8uy')
		b_user = spawn_user('Bob', 'bob@tagarople.com', 'X3u9C4bp')
		e_user = spawn_user('Eve', 'eve@shady.site', '5rX6zrQm')

		alice = a_user.member
		bob = b_user.member
		eve = e_user.member

		ab = MessageThread()
		ab.save()
		ab.participants.add(alice, bob)

		ae = MessageThread()
		ae.save()
		ae.participants.add(alice, eve)

		abe = MessageThread()
		abe.save()
		abe.participants.add(alice, bob, eve)

		# m1 = Message(thread=ab, sender=alice, content='Hello')

	def test_get_threads(self):
		alice = User.objects.get(username='Alice').member
		bob = User.objects.get(username='Bob').member
		eve = User.objects.get(username='Eve').member

		alice, bob, eve = get_member('Alice', 'Bob', 'Eve')

		print("test_get_threads(alice, bob)")
		print(MessageThread.get_thread(alice, bob))


	def test_get_threads_create(self):
		alice, bob, eve = get_member('Alice', 'Bob', 'Eve')
		print("test_get_threads(bob, eve)")
		print(MessageThread.get_thread(bob, eve))


	def test_send_message(self):
		# TODO! Broken!
		alice, bob = get_member('Alice', 'Bob')
		thread = MessageThread.get_thread(alice, bob)
		m = send_message(alice, thread, 'Hi Bob')
		print('test_send_message(alice: Hi Bob)')
		print(m)
		print(thread.message_set)