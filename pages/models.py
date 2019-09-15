from django.db import models
from django.shortcuts import reverse


class Page(models.Model):
    name = models.CharField(max_length=64, blank=False, help_text='Internal name of page')
    title = models.CharField(max_length=64, blank=True, help_text='Page title to display in titlebar of browser/tab')
    page_title = models.CharField(max_length=64, blank=True, help_text='Title to appear at the top of the page')
    breadcrumb_child = models.CharField(max_length=64, blank=True, help_text='Child element of the breadcrumb list')
    body = models.TextField(max_length=16384, blank=True, help_text='Page contents')
    head = models.TextField(max_length=16384, blank=True, help_text='Custom HTML to go in the <head> of the page')
    css = models.TextField(max_length=16384, blank=True, help_text='Custom CSS styles for the page')
    leftbar = models.TextField(max_length=16384, blank=True, help_text='Left sidebar contents (use cards)')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("page", kwargs={"name": self.name})


class BreadcrumbParents(models.Model):
    url = models.CharField(max_length=2048, blank=False, help_text='URL of parent')
    name = models.CharField(max_length=64, blank=False, help_text='Name to display')
    order = models.IntegerField(blank=False, help_text='Order parents are to appear (lower is earlier)')
    page = models.ForeignKey(Page, blank=False, on_delete=models.CASCADE, related_name="breadcrumb_parents")