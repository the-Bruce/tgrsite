from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound,HttpResponse
from django.urls import reverse

from users.models import Member
from .models import Message, MessageThread

import re

# not a view
# helper function to send messages
def send_message(member, thread, message):
	return Message.objects.create(sender=member, thread=thread, content=message)

def send_to(sender, message, *pals_usernames):
	pals = (Member.objects.get(equiv_user__username=x) for x in pals_usernames)
	thread = MessageThread.get_thread(pals)
	return send_message(sender, thread, message)

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
