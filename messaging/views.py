from django.shortcuts import render

from .models import Message, MessageThread

# not a view
# helper function to send messages
def send_message(member, thread, message):
	# Todo! Broken!
	m = Message.objects.create(sender=member, thread=thread, content=message)
	m.save()
	return m