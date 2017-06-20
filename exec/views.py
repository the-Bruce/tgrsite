from django.shortcuts import render

from .models import ExecRole

def index(request):
	context = {
		'execs': ExecRole.objects.all().order_by('sort_order'),
	}
	return render(request, 'exec/index.html', context)
