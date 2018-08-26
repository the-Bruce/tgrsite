from django.urls import path
from django.shortcuts import render
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	path('', views.Index.as_view(template_name='newsletters/index.html'), name='newsletters_index'),
	path('create', views.Create.as_view(template_name='newsletters/create.html'), name='newsletters_create'),
	path('<int:pk>', views.Detail.as_view(template_name='newsletters/detail.html'), name='newsletters_detail'),
	path('edit/<int:pk>', views.Update.as_view(template_name='newsletters/update.html'), name='newsletters_update'),
	path('delete/<int:pk>', views.Delete.as_view(template_name='newsletters/delete.html'), name='newsletters_delete'),
]

