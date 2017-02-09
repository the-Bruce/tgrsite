from django.shortcuts import render

from .models import Message, MessageThread

# not a view
# helper function to send messages
def send_message(member, thread, message):
	return Message.objects.create(sender=member, thread=thread, content=message)
