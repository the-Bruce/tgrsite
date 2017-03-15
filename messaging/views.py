from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound,HttpResponse
from django.urls import reverse

from users.models import Member
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
	# TODO: Protect against empty form!

	if request.POST.get('threadid'):
		thread = get_object_or_404(MessageThread, id=request.POST.get('threadid'))
	else:
		targets = request.POST.get('target').split(',')
		targets += [request.user.username]
		targets = tuple(set(targets))
		print(targets)
		thread = MessageThread.get_thread_from_str(*targets)
	m = send_message(request.user.member, thread, request.POST.get('message'))
	print(m)
	return HttpResponseRedirect(request.GET.get('next'))

@login_required
def index(request):
	# todo: update member's "last access to messages page" variable
	threads = MessageThread.objects.filter(participants=request.user.member)
	context = {
		'threads': threads
	}
	return render(request, 'messaging/index.html', context)

@login_required
def thread(request, pk):
	# make sure the user is in the thread :P
	thread = get_object_or_404(MessageThread, id=pk)
	if request.user.member not in thread.participants.all():
		return HttpResponseNotFound()

	return render(request, 'messaging/detail.html', {'thread':thread})
