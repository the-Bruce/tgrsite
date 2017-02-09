from django.shortcuts import render

from .models import Message, MessageThread

# not a view
# helper function to send messages
def send_message(member, thread, message):
	return Message.objects.create(sender=member, thread=thread, content=message)

def index(request):
	# todo: update member's "last access to messages page" variable
	threads = MessageThread.objects.filter(participants=request.user.member)
	context = {
		'threads': threads
	}
	return render(request, 'messaging/index.html', context)