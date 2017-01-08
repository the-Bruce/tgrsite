from django.shortcuts import render
from django.views import View

# testing
from django.http import HttpResponse

def index(request):
	return render(request, 'tgrsite/index.html')