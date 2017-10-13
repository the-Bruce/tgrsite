from django.shortcuts import render, get_object_or_404

from .models import Page

def page(request, name):
	instance = get_object_or_404(Page, name__iexact=name)
	return render(request, 'pages/page.html', {'page': instance})
