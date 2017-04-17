from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views import generic, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Thread, Response, Forum
from .forms import ThreadForm, ResponseForm

# landing page: "root forum"
def index(request):
	context = {
		'forums': Forum.get_parentless_forums(),
		'current': 'Forum',
	}
	return render(request, 'forum/forum.html', context)

# subforum view
def forum(request, pk):
	current_forum = get_object_or_404(Forum, id=pk)

	# put pinned/stickied threads first
	threads = Thread.objects.filter(forum=pk).extra(order_by=['-is_pinned', '-pub_date'])
	context = {
		'current': current_forum,
		'forums': current_forum.get_subforums(),
		'threads': threads,
		'form': ThreadForm(),
	}
	return render(request, 'forum/forum.html', context)

# views a thread, optionally with a linked response id
def thread(request, pk, response_id=False):
	context = {
		'thread': get_object_or_404(Thread, id=pk),
		'responses': Response.objects.filter(thread=pk),

		# this currently does not do anything
		# but may be used later to like,
		# anchor to the response
		'response_id': response_id,
		'form': ResponseForm(),
	}
	return render(request, 'forum/thread.html', context)

# a wrapper around thread() for the sake of the urlconf being less convoluted
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
			pub_date=timezone.now(),
			forum=Forum.objects.get(id=request.POST.get('forum')),
		)
		thread.save()
		return HttpResponseRedirect(reverse('viewthread', kwargs={'pk':thread.id}))
	else:
		# TODO: placeholder error
		return HttpResponse(repr(form.errors))

@login_required
def create_response(request):
	form = ResponseForm(request.POST)
	if(form.is_valid()):
		res = Response(
			body=form.cleaned_data['body'],
			author=request.user.member,
			pub_date=timezone.now(),
			thread=Thread.objects.get(id=request.POST.get('thread')),
		)
		res.save()
		return HttpResponseRedirect(reverse('viewthread', kwargs={'pk': request.POST.get('thread')}))
	else:
		# TODO: placeholder error
		return HttpResponse(repr(form.errors))

@login_required
def delete_thread(request, pk):
	thread = Thread.objects.get(id=pk)
	if thread.author.equiv_user.id != request.user.id:
		# TODO: placeholder error
		return HttpResponseForbidden()
	url = reverse('subforum', kwargs={'pk': thread.forum.id})
	thread.delete()
	return HttpResponseRedirect(url)

@login_required
def delete_response(request, pk):
	response = Response.objects.get(id=pk)
	if response.author.equiv_user.id != request.user.id:
		# TODO: placeholder error
		return HttpResponseForbidden()
	url = reverse('viewthread', kwargs={'pk': response.thread.id})
	response.delete()
	return HttpResponseRedirect(url)

@login_required
def edit_thread_view(request, pk):
	thread = get_object_or_404(Thread, id=pk)
	if thread.author.equiv_user.id != request.user.id:
		# TODO: placeholder error
		return HttpResponseForbidden()
	form = ThreadForm(instance=thread)
	context = {'form': form, 'id':pk}
	return render(request, 'forum/edit_thread.html', context)

@login_required
def edit_response_view(request, pk):
	response = get_object_or_404(Response, id=pk)
	if response.author.equiv_user.id != request.user.id:
		return HttpResponseForbidden()
	form = ResponseForm(instance=response)
	context = {'form': form, 'id':pk}
	return render(request, 'forum/edit_response.html', context)

@login_required
def edit_thread_process(request):
	id = request.POST.get('id')
	if(request.method != 'POST'):
		return HttpResponseRedirect("/")

	thread = get_object_or_404(Thread, id=id)

	# first, standard permissions junk
	if thread.author.equiv_user.id != request.user.id:
		return HttpResponseForbidden()

	form = ThreadForm(request.POST, instance=thread)
	if(form.is_valid()):
		form.save()
		res = HttpResponseRedirect(reverse('viewthread', kwargs={'pk':id}))
	else:
		res = HttpResponseRedirect(reverse('viewthread', kwargs={'pk':id}) + '?result=invalid')
	return res

@login_required
def edit_response_process(request):
	id = request.POST.get('id')
	if(request.method != 'POST'):
		return HttpResponseRedirect("/")

	response = get_object_or_404(Response, id=id)

	# first, standard permissions junk
	if response.author.equiv_user.id != request.user.id:
		return HttpResponseForbidden()

	form = ResponseForm(request.POST, instance=response)
	if(form.is_valid()):
		form.save()
		res = HttpResponseRedirect(reverse('viewthread', kwargs={'pk':response.thread.id}))
	else:
		res = HttpResponseRedirect(reverse('viewthread', kwargs={'pk':response.thread.id}) + '?result=invalid')
	return res

