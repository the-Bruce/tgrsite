from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import SubscriptionForm
from .models import Notification, delete_old, NotificationSubscriptions


class UpdateSubscriptions(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = NotificationSubscriptions
    form_class = SubscriptionForm
    template_name = "notifications/preferences.html"
    success_url = reverse_lazy("homepage")

    def get_queryset(self):
        data, new = NotificationSubscriptions.objects.get_or_create(member=self.request.user.member)
        return data

    def get_object(self, queryset=None):
        data, new = NotificationSubscriptions.objects.get_or_create(member=self.request.user.member)
        return data

    def get_success_message(self, cleaned_data):
        return "Personal Subscription Settings Updated!"


@login_required
def email_notifications(request):
    context = {
        'notifications': Notification.objects.filter(member=request.user.member).order_by('-is_unread', '-time'),
    }
    return render(request, 'notifications/summary-email.html', context)


@login_required
def all_notifications(request):
    context = {
        'notifications': Notification.objects.filter(member=request.user.member).order_by('-is_unread', '-time'),
    }
    return render(request, 'notifications/index.html', context)


@login_required
def read_all(request):
    Notification.objects.filter(member=request.user.member).update(is_unread=False)
    delete_old(request.user.member)
    return HttpResponseRedirect(reverse('all_notifications'))


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
        return HttpResponseRedirect(reverse('all_notifications'))
