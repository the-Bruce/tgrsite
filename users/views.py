from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError

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

@login_required
def allmembers(request):
	usernames = [ x.username for x in User.objects.all() ]
	return HttpResponse(json.dumps(usernames))

# edit page
@login_required
def edit(request):
	context = {
		'member': request.user.member,
		'result': request.GET.get('result', None),
		'userform': UserForm(instance=request.user),
		'memberform': MemberForm(instance=request.user.member),
	}
	return render(request, 'users/edit.html', context)

# the actual logic for editing the user once the form's sent
@login_required
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
		return HttpResponseRedirect(reverse('me'))

# view for the login form
def login_view(request):
	# if they try and view the login page, and are logged in, redirect
	if(request.user.is_authenticated):
		return HttpResponseRedirect(request.GET.get('next') or reverse('me'))

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
		# FIXME
		# there is a bug here where the user will successfully log in
		# but this branch will still be met
		# Current fix is to make sure that the login page will always redirect to the user page
		# when a user is logged in (which it should do anyway)
		return HttpResponseRedirect(reverse('login') + '?result=invalid')

def signup_view(request):
	form = SignupForm()
	context = {'form': form, 'result': request.GET.get('result')}
	return render(request, 'users/signup.html', context)

def signup_process(request):
	form = SignupForm(request.POST)
	if(form.is_valid()):

		data_valid = True

		# Validate captcha
		import requests
		import os
		data = {
			'secret': os.environ['GCAPTCHA_SECRET'],
			'response': request.POST['g-recaptcha-response'],
		}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)

		if not r.json()['success']:
			form.add_error('g-recaptcha-response', ValidationError('Captcha failed.'))
			data_valid = False

		# CHECK CASE!
		if User.objects.filter(username__iexact=form.cleaned_data['username']).exists():
			form.add_error('username', ValidationError('A user with that name already exists.'))
			data_valid = False
		
		if not data_valid:
			return render(request, 'users/signup.html', {'form': form})

		# now that we're here, the form is DEFINITELY valid.
		u = spawn_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])

		auth = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		if auth is not None:
			login(request, auth)
			return HttpResponseRedirect(reverse('me'))
		else:
			mail_managers(
				'Unknown signup error',
				'Unknown signup error with valid form. Auth is None. Find below form data:\nraw username: {}\nraw email: {}, cleaned username: {}, cleaned email: {}, user id: {}'.format(form.data['username'], form.data['email'], form.cleaned_data['username'], form.cleaned_data['email'], u.id),
				fail_silently=True
			)
			form.add_error(None, ValidationError('Unknown error. The webadmin has been notified.'))
			return render(request, 'users/signup.html', {'form': form})
	else:
		# This should only be true if the username is invalid yet also already exists
		# i.e. never?
		if 'username' in form.data and User.objects.filter(username__iexact=form.data['username']).exists():
			form.add_error('username', ValidationError('A user with that name already exists.'))

		# display the errors from the default validators
		return render(request, 'users/signup.html', {'form': form})

@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

# not a view
# properly sets up a user and member
def spawn_user(username, email, password):
	u = User.objects.create_user(username, email, password)
	m = Member.objects.create(equiv_user=u)
	u.member = m
	u.save()
	m.save()
	return u
