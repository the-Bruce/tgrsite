from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Message, MessageThread


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
	# TODO: validate
	#  ^ how??? ^
	targets = request.POST.get('target').split(',')
	targets = tuple(set(targets))
	print(targets)
	return HttpResponseRedirect('/')
	thread = MessageThread.get_thread_from_str(*targets)
	send_message(request.user.member, thread, request.POST.get('message'))
	return HttpResponseRedirect(reverse('message_list'))

@login_required
def index(request):
	# todo: update member's "last access to messages page" variable
	threads = MessageThread.objects.filter(participants=request.user.member)
	context = {
		'threads': threads
	}
	return render(request, 'messaging/index.html', context)
