from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Notification, delete_old

@login_required
def all_notifications(request):
	context = {
		'notifications': Notification.objects.filter(member=request.user.member).order_by('-is_unread','-time'),
	}
	return render(request, 'notifications/index.html', context)

@login_required
def read_all(request):
	Notification.objects.filter(member=request.user.member).update(is_unread=False)
	delete_old(request.user.member)
	return HttpResponseRedirect('/notifications')

@login_required
def mark_read(request, pk):
	user_notifs = Notification.objects.filter(member=request.user.member)
	notif = get_object_or_404(user_notifs, id=pk)
	notif.is_unread = False
	notif.save()
	delete_old(request.user.member)
	if notif.url and notif.url != '':
		return HttpResponseRedirect(notif.url)
	else:
		return HttpResponseRedirect('/notifications')
