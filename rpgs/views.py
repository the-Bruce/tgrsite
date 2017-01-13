from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.urls import reverse, reverse_lazy
import os

# testing
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from users.models import Member

from .models import Rpg
from .forms import RpgForm

class Index(generic.ListView):
	template_name = 'rpgs/index.html'
	model = Rpg
	context_object_name = 'rpgs'

class Detail(generic.DetailView):
	template_name = 'rpgs/rpg.html'
	model = Rpg
	context_object_name = 'rpg'

class Join(View):
	def get(self, request):
		res = HttpResponseBadRequest('You shouldn\'t visit this URL in your browser - use the <a href=' + reverse('rpgs') + '>RPG page</a> instead.')
		return res

	def post(self, request):
		# if user is signed in:
		if request.user.is_authenticated:
			return HttpResponse('watch this space')
		else:
			# redirect to signup?
			# TODO
			res = HttpResponse('You need to be logged in.', status=302)
			return res

@login_required
def create(request):
	return render(request, 'rpgs/create.html', {'form': RpgForm})

@login_required
def create_done(request):
	# create a new RPG from all the form's fields
	# except the middleware token
	# and am_i_gm which is used here instead
	args = {i : request.POST.get(i, None) for i in request.POST if i!='csrfmiddlewaretoken' and i!='am_i_gm'}

	args['creator_id'] = request.user.member.id

	# Make a form in order to validate the data
	fargs = RpgForm(args)

	if not fargs.is_valid():
		return HttpResponse('Form invalid?!?!?!')
	me = Member.objects.get(id=request.user.member.id)

	ins = Rpg(**args)
	ins.save()
	if(request.POST.get('am_i_gm', None)):
		ins.game_masters.add(me)

	# redirect to RPG
	return HttpResponseRedirect(reverse('rpg', kwargs={'pk': ins.id}) + '?status=created')
