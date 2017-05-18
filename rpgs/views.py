from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.urls import reverse, reverse_lazy
import os

# testing
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.models import Member

from .models import Rpg, Tag
from .forms import RpgForm, RpgManageForm

class Index(generic.ListView):
	template_name = 'rpgs/index.html'
	model = Rpg
	context_object_name = 'rpgs'

class Detail(generic.DetailView):
	template_name = 'rpgs/rpg.html'
	model = Rpg
	context_object_name = 'rpg'

class Filter(Index):
	def get_queryset(self):
		return Rpg.objects.filter(tags__name=self.kwargs['tag'])

@login_required
def join(request):
	rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
	rpg.members.add(request.user.member)
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk':request.POST.get('id')}))

@login_required
def leave(request):
	rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
	rpg.members.remove(request.user.member)
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk':request.POST.get('id')}))

@login_required
def create(request):
	return render(request, 'rpgs/create.html', {'form': RpgForm})

@login_required
def kick(request):
	rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
	if request.user.member == rpg.creator:
		rpg.members.remove(request.POST.get('user-to-remove'))
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk':request.POST.get('id')}) + '?nousername=1')

@login_required
def add_to(request):
	""" adds a player to an RPG using the `username` and `id` fields of form"""
	# Notes: could do this through a URLconf instead?
	# /rpg/<id>/add/<username>? userid instead of username?

	# TODO: This 404 doesn't fire, it just fails silently.
	# Might work to instead try/except and redirect back with error?
	# Also worth noting that this kind of form is exactly the kind of thing
	# that could be enhanced with AJAX, and that could shape the response structure.
	rpg = get_object_or_404(Rpg, id=request.POST.get('id'))
	if request.user.member == rpg.creator:
		users = User.objects.filter(username=request.POST.get('username'))
		if users.count() == 0:
			return HttpResponseRedirect(reverse('rpg', kwargs={'pk':request.POST.get('id')}))
		rpg.members.add(users[0].id)
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk':request.POST.get('id')}))

@login_required
def create_done(request):
	# create a new RPG from all the form's fields
	# except the middleware token
	# and am_i_gm which is used here instead
	# Probably not required? Pretty sure fields not in the model are ignored...
	args = {i : request.POST.get(i, None) for i in request.POST if i!='am_i_gm' and i!='tags' and i!='csrfmiddlewaretoken'}

	args['creator_id'] = request.user.member.id

	# Make a form in order to validate the data
	fargs = RpgForm(args)

	if not fargs.is_valid():
		# TODO: Better error!
		return HttpResponse('Unknown error: RpgForm is not valid')


	me = Member.objects.get(id=request.user.member.id)

	ins = Rpg(**args)
	ins.save()

	"""newtags = []
	for tag in request.POST.get('tags', '').split(','):
		# determine new tag
		newtags.append(Tag.objects.get_or_create(name=tag)[0])"""

	# add tags
	ins.tags = tags_from_str(request.POST.get('tags', ''))

	if(request.POST.get('am_i_gm', None)):
		ins.game_masters.add(me)

	# send them to the page that was created

	return HttpResponseRedirect(reverse('rpg', kwargs={'pk': ins.id}) + '?status=created')

# not a view
def tags_from_str(str):
	tags = []
	for tag in str.split(','):
		if tag == '':
			continue
		tags.append(Tag.objects.get_or_create(name=tag.strip().lower())[0])
	return tags

@login_required
def edit(request, pk):
	rpg = get_object_or_404(Rpg, id=pk)
	# TODO: Test permission code
	if rpg.creator.equiv_user.id != request.user.id:
		return HttpResponseForbidden()
	form = RpgForm(instance=rpg, initial={'tags': rpg.tags_str()})
	context = {'form': form, 'id': pk, 'rpg': rpg}
	return render(request, 'rpgs/edit.html', context)


from .templatetags.rpg_tags import can_manage


@login_required
def edit_process(request, pk):
	rpg=get_object_or_404(Rpg, id=pk)
	if not can_manage(request.user.member, rpg):
		return HttpResponseForbidden()
	form = RpgForm(
		request.POST,
		instance=rpg
		)
	if(form.is_valid):
		"""newtags = []
		for tag in form.data['tags'].split(','):
			# determine new tag
			newtags.append(Tag.objects.get_or_create(name=tag)[0])"""

		# change tags
		rpg.tags = tags_from_str(form.data['tags'])

		# cleanup?
		# remove tags that have no uses
		for tag in Tag.objects.all():
			if(tag.rpg_set.count() == 0):
				tag.delete()

		form.save()
		return HttpResponseRedirect(reverse('rpg', kwargs={'pk':pk}))
	else:
		# TODO: Proper errors
		return HttpResponseBadRequest()

@login_required
def delete(request, pk):

	# TODO: ask user for confirmation !
	rpg = get_object_or_404(Rpg, id=pk)

	if not can_manage(request.user.member, rpg):
		return HttpResponseForbidden()

	rpg.delete()
	return HttpResponseRedirect(reverse('rpgs'))

# this is REALLY not scalable!
# ^ clarify?
# TODO
def manage(request, pk):
	rpg = get_object_or_404(Rpg, id=pk)
	form = RpgManageForm(instance=rpg, initial={'tags': rpg.tags_str})
	context = {'rpg': rpg, 'form': form}
	return render(request, 'rpgs/manage.html', context)

# ??????
def manage_process(request, pk):
	return HttpResponse()
