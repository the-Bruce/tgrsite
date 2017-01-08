from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic, View

from .models import Thread, Response, Forum

# index view: list of all forums
# Render a list of forums that aren't subforums i.e. "root" forums
def index(request):
	context = {
		'forums': Forum.get_parentless_forums(),
		'current': 'Forum'
	}
	return render(request, 'forum/forum.html', context)

# view a specific forum
def forum(request, pk):
	current_forum = Forum.objects.get(id=pk)
	threads = Thread.objects.filter(forum=pk).extra(order_by=['-is_pinned', '-pub_date'])
	context = {
		'current': current_forum,
		'forums': current_forum.get_subforums(),
		'threads': threads,
	}

	return render(request, 'forum/forum.html', context)

# view a particular thread
def thread(request, pk, response_id=False):
	context = {
		'thread': get_object_or_404(Thread, id=pk),
		'responses': Response.objects.filter(thread=pk),
		'response_id': response_id,
	}
	return render(request, 'forum/thread.html', context)

def response(request, pk):
	current=get_object_or_404(Response, id=pk)
	return thread(request, current.thread.id, pk)