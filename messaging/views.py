from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound,HttpResponse
from django.urls import reverse
from django.db.models import Count
from users.models import Member
from .models import Message, MessageThread
from django.contrib.auth.models import User
from notifications.models import notify, NotifType

import re

# not a view
# helper function to send messages
def send_message(member, thread, message):
	# Send the notification to everyone in the thread except the sender.
	url = reverse('message_thread', args=[thread.id])
	for receiver in thread.participants.all():
		if member != receiver:
			notify(receiver, NotifType.MESSAGE, 'You got a message from '+str(member.equiv_user.username)+': '+message, url)
	return Message.objects.create(sender=member, thread=thread, content=message)

def send_to(sender, message, *pals_usernames):
	pals = (Member.objects.get(equiv_user__username=x) for x in pals_usernames)
	thread = MessageThread.get_thread(pals)
	return send_message(sender, thread, message)

# specific message between two users
# expected form: 'message': message body, 'target': recipient username
@login_required
def direct_message(request):
	# if it's all spaces then send them away
	if re.match(r'^\s*$',request.POST.get('message')):
		return HttpResponseRedirect(request.GET.get('next'))

	target = get_object_or_404(Member, equiv_user__username=request.POST.get('target'))

	query = MessageThread.objects.annotate(num_participants=Count('participants'))
	query = query.filter(participants=target)
	if target.id == request.user.member.id:
		query = query.filter(num_participants=1)
	else:
		query = query.filter(num_participants=2)
		query = query.filter(participants=request.user.member)

	t, c = query.get_or_create()

	if c:
		t.participants.add(request.user.member)
		t.participants.add(target)

	m = send_message(request.user.member, t, request.POST.get('message'))
	# not sure if this works just yet :0
	return HttpResponseRedirect(request.GET.get('next'))

# for messaging a groupchat.
# expected form: 'message': message body.
@login_required
def group_message(request, threadid):
	# if it's all spaces then send them away
	if re.match(r'^\s*$',request.POST.get('message')):
		return HttpResponseRedirect(request.GET.get('next'))

	thread = get_object_or_404(MessageThread, id=threadid)

	t = get_object_or_404(MessageThread, id=threadid)
	print("Sending message from {} to thread {} with body {}".format(request.user.member, thread, request.POST.get('message')))
	m = send_message(request.user.member, thread, request.POST.get('message'))
	return HttpResponseRedirect(reverse('message_thread', args=[threadid]))

# DEPRECATED
"""
@login_required
def dm(request):
	if re.match(r'^\s*$',request.POST.get('message')):
		return HttpResponseRedirect(request.GET.get('next'))

	# if we are messaging a known thread
	if request.POST.get('threadid'):
		thread = get_object_or_404(MessageThread, id=request.POST.get('threadid'))

	# otherwise we are being given comma-separated users and need to find or make the thread
	else:
		targets = request.POST.get('target').split(',')

		# sending user always is in group
		targets += [request.user.username]

		# eliminate duplicates ;)
		targets = tuple(set(targets))

		thread = MessageThread.get_thread_from_str(*targets)

	m = send_message(request.user.member, thread, request.POST.get('message'))
	# not sure if this works just yet :0
	return HttpResponseRedirect(request.GET.get('next'))
"""
@login_required
def index(request):
	# todo: if we keep track on a Member their last time they visited the messages page,
	# we might be able to use that to do notifications
	# though keeping track of specific messages being "read" would be better
	threads = MessageThread.objects.filter(participants=request.user.member)
	context = {
		'threads': threads
	}
	return render(request, 'messaging/index.html', context)

@login_required
def thread(request, pk):
	thread = get_object_or_404(MessageThread, id=pk)
	# make sure the user is in the thread :P
	if request.user.member not in thread.participants.all():
		return HttpResponseNotFound()

	return render(request, 'messaging/detail.html', {'thread':thread})

# redirects to the thread containing messages between logged-in user and recipient
@login_required
def get_dm_thread(request, recipient):

	# recipient member
	rec = Member.objects.get(id=recipient)
	q = MessageThread.objects.annotate(num_participants=Count('participants'))

	q = q.filter(participants=rec)

	print(rec)

	if rec == request.user.member:
		q = q.filter(num_participants=1)
	else:
		q = q.filter(num_participants=2)
		q = q.filter(participants=request.user.member)
	q, c = q.get_or_create()

	if c:
		q.participants.add(request.user.member)
		q.participants.add(rec)

	print(q)

	return HttpResponseRedirect(reverse('message_thread', kwargs={'pk': q.id}))
