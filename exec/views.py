from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, UpdateView

from .forms import ExecBioForm
from .models import ExecRole


def index(request):
    context = {
        'execs': ExecRole.objects.all().order_by('sort_index')
    }
    return render(request, 'exec/index.html', context)


class Index(ListView):
    model = ExecRole
    template_name = "exec/index.html"
    context_object_name = "execs"
    ordering = ("sort_index",)


class Edit(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = ExecRole
    form_class = ExecBioForm
    template_name = "exec/editbio.html"
    success_url = reverse_lazy('exec:exec')
    success_message = "Exec Bio Updated"

    def test_func(self):
        role = get_object_or_404(ExecRole, id=self.kwargs['pk'])
        return role.incumbent == self.request.user.member
