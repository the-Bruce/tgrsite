from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='message_list'),
	url(r'^dm$', views.dm, name='message_dm'),
]