from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Page


class ViewPage(generic.DetailView):
    model = Page
    slug_field = 'name'
    slug_url_kwarg = 'name'
    context_object_name = 'page'
    template_name = "pages/page.html"
