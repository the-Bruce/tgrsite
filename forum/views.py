import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Thread, Response, Forum
from .forms import ThreadForm, ResponseForm

# index view: list of all forums
# Render a list of forums that aren't subforums i.e. "root" forums
def index(request):
	context = {
		'forums': Forum.get_parentless_forums(),
		'current': 'Forum',
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
		'form': ThreadForm(),
	}

	return render(request, 'forum/forum.html', context)

# view a particular thread
def thread(request, pk, response_id=False):
	context = {
		'thread': get_object_or_404(Thread, id=pk),
		'responses': Response.objects.filter(thread=pk),
		'response_id': response_id,
		'form': ResponseForm(),
	}
	return render(request, 'forum/thread.html', context)

# link to a particular response
# dealt with in the thread() view
def response(request, pk):
	current=get_object_or_404(Response, id=pk)
	return thread(request, current.thread.id, pk)

@login_required
def create_thread(request):
	form = ThreadForm(request.POST)
	if(form.is_valid()):
		thread = Thread(
			title=form.cleaned_data['title'],
			body=form.cleaned_data['body'],
			author=request.user.member,
			pub_date=datetime.datetime.now(),
			forum=Forum.objects.get(id=request.POST.get('forum')),
		)

		thread.save()
		return HttpResponseRedirect(reverse('viewthread', kwargs={'pk':thread.id}))
	else:
		return HttpResponse(repr(form.errors))

@login_required
def create_response(request):
	form = ResponseForm(request.POST)
	if(form.is_valid()):
		res = Response(
			body=form.cleaned_data['body'],
			author=request.user.member,
			pub_date=datetime.datetime.now(),
			thread=Thread.objects.get(id=request.POST.get('thread')),
		)

		res.save()
		return HttpResponseRedirect(reverse('viewthread', kwargs={'pk': request.POST.get('thread')}))
	else:
		return HttpResponse(repr(form.errors))
