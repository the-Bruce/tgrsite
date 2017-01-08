from django.shortcuts import render

from .models import ExecRole

def index(request):
	context = {
		'execs': ExecRole.objects.all(),
	}
	return render(request, 'exec/index.html', context)