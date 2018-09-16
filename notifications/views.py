from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Notification

# Create your views here.
@login_required
def all_notifications(request):
	context = {
		'notifs': Notification.objects.filter(member=request.user.member).order_by('-unread','-time'),
	}
	return render(request, 'notifications/index.html', context)

@login_required
def read_all(request):
	Notification.objects.filter(member=request.user.member).update(unread=False)
	return HttpResponseRedirect('/notifications')

@login_required
def read_notification(request, pk):
	user_notifs = Notification.objects.filter(member=request.user.member)
	notif = get_object_or_404(user_notifs, id=pk)
	notif.unread = False
	notif.save()
	if notif.url and notif.url != '':
		return HttpResponseRedirect(notif.url)
	else:
		return HttpResponseRedirect('/notifications')
