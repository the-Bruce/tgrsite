from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from .models import Newsletter

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class Index(generic.ListView):
	model = Newsletter

class Detail(generic.DetailView):
	model = Newsletter

class Create(PermissionRequiredMixin, generic.edit.CreateView):
	model = Newsletter
	fields = ['title', 'body']

	permission_required = 'newsletters_create'

	def form_valid(self, form):
		form.instance.author = self.request.user.member
		form.instance.pub_date = timezone.now()
		return super(Create, self).form_valid(form)
