from django.shortcuts import render
from django.views import generic
from .models import Report

from django.contrib.auth.mixins import LoginRequiredMixin

class Index(LoginRequiredMixin, generic.ListView):
	model = Report

class Detail(LoginRequiredMixin, generic.DetailView):
	model = Report

class Create(LoginRequiredMixin, generic.CreateView):
	model = Report
	fields = ['title', 'body', 'feature']

	def form_valid(self, form):
		form.instance.reporter = self.request.user.member
		return super(Create, self).form_valid(form)
