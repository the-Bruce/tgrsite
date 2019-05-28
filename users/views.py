# temp
import datetime
import hmac
import json
import re

from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import add_message, constants
from django.core.mail import mail_managers
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from exec.models import ExecRole
from forum.models import Thread, Response
from rpgs.models import Rpg
from .captcha import make_captcha
from .forms import MemberForm, UserForm, LoginForm, SignupForm
from .models import Member


def viewmember(request, pk):
    if (pk == 'me'):
        # if we're logged in, get the user id and use that
        if (request.user.is_authenticated):
            pk = request.user.member.id
        else:
            # if we're not logged in then it's an inappropriate request
            return HttpResponseRedirect('/', status=400)

    member = get_object_or_404(Member, id=pk)

    execroles = ExecRole.objects.filter(incumbent__id=pk)

    # = ','.join(str()

    is_me=False
    if (request.user.is_authenticated):
        is_me=(request.user.member.id == pk)
    
    
    context = {
        # whether the viewed user is the logged in one
        'me': is_me,
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
    usernames = [x.username for x in User.objects.all()]
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
    if (request.method == 'POST'):
        # generate a filled form from the post request
        memberform = MemberForm(request.POST, instance=request.user.member)
        userform = UserForm(request.POST, instance=request.user)
        if (memberform.is_valid() and userform.is_valid()):
            memberform.save()
            userform.save()
            add_message(request, constants.SUCCESS, "Successfully updated.")
            res = HttpResponseRedirect(reverse('me'))
            return res
        else:
            add_message(request, constants.ERROR, "There were problems with the form.")
            return HttpResponseRedirect(reverse('edit'))

    else:
        return HttpResponseRedirect(reverse('me'))


# view for the login form
def login_view(request):
    # if they try and view the login page, and are logged in, redirect
    if (request.user.is_authenticated):
        return HttpResponseRedirect(request.GET.get('next') or reverse('me'))

    form = LoginForm()
    context = {'form': form, 'result': request.GET.get('result'), 'next': request.GET.get('next')}
    return render(request, 'users/login.html', context)


# actually logs the user in
def login_process(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
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
    context = add_captcha_to_form(form)
    context['result'] = request.GET.get('result')
    return render(request, 'users/signup.html', context)


def add_captcha_to_form(form):
    (question, answer, captcha_help) = make_captcha()
    return {'form': form, 'captcha': question, 'token': hash3(answer), 'captcha_help': captcha_help}

def getSecret():
    # This means that captcha is invalid over midnight but reduces replay attacks to beyond the
    # difficulty of actually solving the captcha
    return settings.SECRET_KEY + str(datetime.date.today())

def hash3(inp):
    return hmac.new(key=getSecret().encode(), msg=str(inp).encode(), digestmod="sha256").hexdigest()


def signup_process(request):
    form = SignupForm(request.POST)
    if (form.is_valid()):

        data_valid = True
        captcha_input = re.sub(r'\s', '', request.POST['captcha'])
        captcha_target = re.sub(r'\s', '', request.POST['captcha-token'])
        # CHECK CAPTCHA!
        if not hmac.compare_digest(hash3(captcha_input), captcha_target):
            # Should be attached to captcha, but this is the closest thing.
            form.add_error(None, ValidationError('You didn\'t answer the captcha correctly!'))
            data_valid = False
        # CHECK CASE!
        elif User.objects.filter(username__iexact=form.cleaned_data['username']).exists():
            form.add_error('username', ValidationError('A user with that name already exists.'))
            data_valid = False

        if not data_valid:
            return render(request, 'users/signup.html', add_captcha_to_form(form))

        # now that we're here, the form is DEFINITELY valid.
        u = spawn_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])

        auth = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if auth is not None:
            login(request, auth)
            return HttpResponseRedirect(reverse('edit'))
        else:
            mail_managers(
                'Unknown signup error',
                'Unknown signup error with valid form. Auth is None. Find below form data:\nraw username: {}\nraw email: {}, cleaned username: {}, cleaned email: {}, user id: {}'.format(
                    form.data['username'], form.data['email'], form.cleaned_data['username'],
                    form.cleaned_data['email'], u.id),
                fail_silently=True
            )
            form.add_error(None, ValidationError('Unknown error. The webadmin has been notified.'))
            return render(request, 'users/signup.html', add_captcha_to_form(form))
    else:
        # This should only be true if the username is invalid yet also already exists
        # i.e. never?
        if 'username' in form.data and User.objects.filter(username__iexact=form.data['username']).exists():
            form.add_error('username', ValidationError('A user with that name already exists.'))

        # display the errors from the default validators
        return render(request, 'users/signup.html', add_captcha_to_form(form))


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
