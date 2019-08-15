import re

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import FormView, ListView, TemplateView, RedirectView

from notifications.models import notify, NotifType
from users.models import Member
from .models import Message, MessageThread
from .forms import QuickDM, Respond, MemberFormset


# not a view
# helper function to send messages
def find_group(*members):
    members = set(members)
    query = MessageThread.objects.all()
    query = query.annotate(num_participants=Count('participants')).filter(num_participants=len(members))
    for i in members:
        query = query.filter(participants=i)
    try:
        return query.get()
    except MessageThread.DoesNotExist:
        m_thread = MessageThread.objects.create(title="")
        for member in members:
            m_thread.participants.add(member)
        m_thread.save()
        return m_thread
    except MessageThread.MultipleObjectsReturned:
        for i in query:
            print(i)
        raise AssertionError("Impossible State Reached")  # TODO: DO NOT LEAVE IN PROD!!!


def send_message(member, thread, message):
    # Send the notification to everyone in the thread except the sender.
    url = reverse('message:message_thread', args=[thread.id])
    for receiver in thread.participants.all():
        if member != receiver:
            notify(receiver, NotifType.MESSAGE,
                   'You got a message from ' + str(member.equiv_user.username) + ': ' + message, url)
    return Message.objects.create(sender=member, thread=thread, content=message)


@login_required
@require_http_methods(["POST"])
def rename_thread(request):
    target = get_object_or_404(MessageThread, pk=request.POST.get('thread'))

    if request.user.member not in target.participants.all():
        raise Http404()

    target.title = request.POST.get('rename', None)
    target.full_clean()
    target.save()
    return HttpResponseRedirect(reverse('message:message_thread', kwargs={'pk': request.POST.get('thread')}))


class Index(LoginRequiredMixin, FormView):
    form_class = QuickDM
    template_name = "messaging/index.html"

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data(**kwargs)
        threads = MessageThread.objects.filter(participants=self.request.user.member).annotate(
            latest=Max('message__timestamp'))
        ctxt['threads'] = threads.order_by(F('latest').desc(nulls_last=True))

        return ctxt

    def get_success_url(self):
        return reverse("message:message_thread", args=[self.object.thread_id])

    def form_valid(self, form):
        target = form.cleaned_data['recipient']
        assert isinstance(target, Member)

        t = find_group(target, self.request.user.member)
        m = send_message(self.request.user.member, t, form.cleaned_data['message'])
        self.object = m
        return super().form_valid(form)


class Thread(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = Respond
    template_name = "messaging/detail.html"

    def test_func(self):
        thread = get_object_or_404(MessageThread, id=self.kwargs['pk'])
        # make sure the user is in the thread
        return self.request.user.member in thread.participants.all()

    def get_context_data(self, **kwargs):
        count = 10
        ctxt = super().get_context_data(**kwargs)
        ctxt['thread'] = thread = get_object_or_404(MessageThread, id=self.kwargs['pk'])
        ctxt['thread_messages'] = thread.message_set.order_by('-timestamp')[:count]
        ctxt['more'] = (thread.message_set.count() > count)
        return ctxt

    def get_success_url(self):
        return reverse("message:message_thread", args=[self.object.thread_id])

    def form_valid(self, form):
        t = MessageThread.objects.get(pk=self.kwargs['pk'])
        m = send_message(self.request.user.member, t, form.cleaned_data['message'])
        self.object = m
        return super().form_valid(form)


class CreateGroup(LoginRequiredMixin, FormView):
    template_name = "messaging/newgroup.html"
    form_class = MemberFormset

    def get_success_url(self):
        return reverse("message:message_thread", args=[self.object.pk])

    def form_valid(self, form):
        members = set()
        for subform in form:
            r = subform.cleaned_data['recipient']
            if r not in members:
                members.add(r)
        if self.request.user.member not in members:
            members.add(self.request.user.member)

        self.object = find_group(*members)
        return super().form_valid(form)


class FullThread(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Message
    paginate_by = 30
    template_name = "messaging/fullthread.html"
    context_object_name = "thread_messages"

    def test_func(self):
        thread = get_object_or_404(MessageThread, id=self.kwargs['thread'])
        # make sure the user is in the thread
        return self.request.user.member in thread.participants.all()

    def get_context_data(self, object_list=None, **kwargs):
        ctxt = super().get_context_data(object_list=object_list, **kwargs)
        ctxt['thread'] = get_object_or_404(MessageThread, id=self.kwargs['thread'])
        return ctxt

    def get_queryset(self):
        thread_ = get_object_or_404(MessageThread, pk=self.kwargs['thread'])
        return thread_.message_set.order_by('-timestamp').all()


class DMThread(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        rec = Member.objects.get(id=kwargs['recipient'])
        q = find_group(self.request.user.member, rec)
        return reverse("message:message_thread", args=[q.id])
