from django.shortcuts import render
from django.views import generic
from .models import Report
# strictly these aren't necessary, as in the URLconf we can
# use, say, url('...', ListView.as_view(), model=Report, name=...)
class Index(generic.ListView):
	model = Report
class Detail(generic.DetailView):
	model=Report
class Create(generic.CreateView):
	model=Report
	fields=['title', 'body', 'feature']
