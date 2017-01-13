from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect

from rpgs.models import Rpg
from exec.models import ExecRole
from forum.models import Thread, Response

from .models import Member
from .forms import MemberForm, UserForm, LoginForm, SignupForm

#temp
import json

def viewmember(request, pk):
	if(pk == 'me'):
		# if we're logged in, get the user id and use that
		if(request.user.is_authenticated):
			pk = request.user.member.id
		else:
			# if we're not logged in then it's an inappropriate request
			return HttpResponseRedirect('/', status=400)

	member = get_object_or_404(Member, id=pk)

	execroles = ExecRole.objects.filter(incumbent__id=pk)

	# = ','.join(str()

	context = {
		# whether the viewed user is the logged in one
		'me': member.id == pk,
		'result': request.GET.get('result', None),
		'member': member,

		# activity info
		'recent_threads': Thread.objects.filter(author__id=pk).order_by('-pub_date')[:3],
		'recent_responses': Response.objects.filter(author__id=pk).order_by('-pub_date')[:3],
		'rpgs': Rpg.objects.filter(game_masters__id=pk),
		'execroles': execroles,
	}
	return render(request, 'users/view.html', context)

def edit(request):
	context = {
		'member': request.user.member,
		'result': request.GET.get('result', None),
		'userform': UserForm(instance=request.user),
		'memberform': MemberForm(instance=request.user.member),
	}
	return render(request, 'users/edit.html', context)

def update(request):
	if(request.method == 'POST'):
		# generate a filled form from the post request
		memberform = MemberForm(request.POST, instance=request.user.member)
		userform = UserForm(request.POST, instance=request.user)
		if(memberform.is_valid() and userform.is_valid()):
			memberform.save()
			userform.save()
			res = HttpResponseRedirect(reverse('me') + '?result=success')
			return res
		else:
			return HttpResponseRedirect(reverse('edit') + '?result=invalid')

	else:
		return HttpResponse('GET !')

# view for the login form
def login_view(request):
	form = LoginForm()
	context = {'form': form, 'result': request.GET.get('result'), 'next': request.GET.get('next')}
	return render(request, 'users/login.html', context)

# actually logs the user in
def login_process(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(request.GET.get('next') or '/')
	else:
		return HttpResponseRedirect(reverse('login') + '?result=invalid')

def signup_view(request):
	form = SignupForm()
	context = {'form': form, 'result': request.GET.get('result')}
	return render(request, 'users/signup.html', context)

def signup_process(request):
	form = SignupForm(request.POST)
	if(form.is_valid()):

		u = User.objects.create_user(form.data['username'], form.data['email'], form.data['password'])
		m = Member.objects.create(equiv_user=u)
		u.save()
		auth = authenticate(username=form.data['username'], password=form.data['password'])
		if auth is not None:
			login(request, auth)
			return HttpResponseRedirect(reverse('me'))
		else:
			return HttpResponse('auth after signup failed to login')
	else:
		# TODO: Proper error lol
		return HttpResponse('form not valid')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
