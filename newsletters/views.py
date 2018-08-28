from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Newsletter
from .forms import NewsletterForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404

class Index(generic.ListView):
	model = Newsletter
	ordering = ['ispublished','-pub_date']

class Detail(generic.DetailView):
	model = Newsletter

	def get_object(self, queryset=None):
		obj = super(Detail, self).get_object()
		if not obj.ispublished and not self.request.user.has_perm('newsletters.newsletters_edit'):
			raise Http404
		return obj

class Create(PermissionRequiredMixin, generic.edit.CreateView):
	model = Newsletter
	form_class = NewsletterForm

	permission_required = 'newsletters_create'

	def form_valid(self, form):
		form.instance.author = self.request.user.member
		form.instance.pub_date = timezone.now()
		return super(Create, self).form_valid(form)

class Update(PermissionRequiredMixin, generic.edit.UpdateView):
	model = Newsletter
	form_class = NewsletterForm

	permission_required = 'newsletters_edit'
	raise_exception = True

	def form_valid(self, form):
		if form.instance.ispublished: form.instance.pub_date = timezone.now()
		return super(Update, self).form_valid(form)

	def get_object(self, queryset=None):
		""" Hook to ensure object is owned by request.user. """
		obj = super(Update, self).get_object()
		if obj.author and obj.author != self.request.user.member:
			raise Http404
		return obj

class Delete(PermissionRequiredMixin, generic.edit.DeleteView):
	model = Newsletter

	permission_required = 'newsletters_delete'
	raise_exception = True
	success_url = reverse_lazy('newsletters_index')

	def get_object(self, queryset=None):
		""" Hook to ensure object is owned by request.user. """
		obj = super(Delete, self).get_object()
		if obj.author and obj.author != self.request.user.member:
			raise Http404
		return obj
