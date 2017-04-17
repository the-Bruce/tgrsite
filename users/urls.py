from django.conf.urls import url

from . import views

urlpatterns = [

	url(r'^edit/', views.edit, name='edit'),

	url(r'^(?P<pk>[0-9]+)/$', views.viewmember, name='user'),
	url(r'^me/$', views.viewmember, {'pk': 'me'}, name='me'),

	url(r'^update/$', views.update, name='update'),

	url(r'^allmembers/$', views.allmembers, name='allmembers'),

]
