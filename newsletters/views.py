from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from notifications.models import notify_everybody, NotifType
from notifications.tasks import doNewsletterMailings
from .forms import NewsletterForm
from .models import Newsletter


class Index(generic.ListView):
    model = Newsletter
    ordering = ['ispublished', '-pub_date']


class Detail(generic.DetailView):
    model = Newsletter

    def get_object(self, queryset=None):
        obj = super(Detail, self).get_object()
        if not obj.ispublished and not self.request.user.has_perm('newsletters.change_newsletter'):
            raise Http404
        return obj


class Create(PermissionRequiredMixin, generic.edit.CreateView):
    model = Newsletter
    form_class = NewsletterForm

    permission_required = 'newsletters.add_newsletter'

    def form_valid(self, form):
        form.instance.author = self.request.user.member
        form.instance.pub_date = timezone.now()
        s = super(Create, self).form_valid(form)
        if form.instance.ispublished:
            notify_everybody(NotifType.NEWSLETTER,
                             'The newsletter "{}" has been published!'.format(form.instance.title),
                             form.instance.get_absolute_url())
        return s

    def get_success_url(self):
        if self.object.ispublished:
            doNewsletterMailings(self.object.id)
        return super().get_success_url()


class Update(PermissionRequiredMixin, generic.edit.UpdateView):
    model = Newsletter
    form_class = NewsletterForm

    permission_required = 'newsletters.change_newsletter'
    raise_exception = True

    def form_valid(self, form):
        # If newsletter goes from unpublished to published.
        if form.instance.ispublished and not Newsletter.objects.get(id=form.instance.id).ispublished:
            form.instance.pub_date = timezone.now()
            notify_everybody(NotifType.NEWSLETTER,
                             'The newsletter "{}" has been published!'.format(form.instance.title),
                             form.instance.get_absolute_url())
            doNewsletterMailings(form.instance.id)
        return super(Update, self).form_valid(form)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user, or request.user can change others. """
        obj = super(Update, self).get_object()
        if obj.author and (obj.author != self.request.user.member and not self.request.user.has_perm(
                'newsletters.modify_others')):
            # If neither owned it nor have modify_others
            raise Http404
        return obj


def latest(req):
    letter = Newsletter.objects.order_by('-pub_date').filter(ispublished=True)[0]
    return redirect(letter)


class Delete(PermissionRequiredMixin, generic.edit.DeleteView):
    model = Newsletter

    permission_required = 'newsletters.delete_newsletter'
    raise_exception = True
    success_url = reverse_lazy('newsletters_index')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user, or request.user can change others. """
        obj = super(Delete, self).get_object()
        if obj.author and (obj.author != self.request.user.member and not self.request.user.has_perm(
                'newsletters.modify_others')):
            raise Http404
        return obj
