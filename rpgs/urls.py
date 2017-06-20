from django.conf.urls import url
from django.shortcuts import render
from . import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='rpgs'),
	url(r'^(?P<pk>[0-9]+)/$', views.Detail.as_view(), name='rpg'),
	url(r'^tagged/(?P<tag>[^/]+)/$', views.Filter.as_view(), name='rpg_tag'),
	url(r'^tag_form/$', views.tag_form, name='rpg_tag_form'),
	url(r'^join/$', views.join, name='rpg_join'),

	url(r'^leave/$', views.leave, name='rpg_leave'),
	url(r'^kick/$', views.kick, name='rpg_kick'),

	url(r'^create/$', views.create, name='rpg_create'),
	url(r'^add_to/$', views.add_to, name='rpg_add_to'),
	url(r'^(?P<pk>[0-9]+)/edit$', views.edit, name='rpg_edit'),
	url(r'^(?P<pk>[0-9]+)/edit/done$', views.edit_process, name='rpg_edit_done'),

	# these are nowhere near usable
	#url(r'^(?P<pk>[0-9]+)/manage$', views.manage, name='rpg_manage'),
	#url(r'^(?P<pk>[0-9]+)/manage/done$', views.manage_process, name='rpg_manage_done'),

	url(r'^(?P<pk>[0-9]+)/delete$', views.delete, name='rpg_delete'),
	url(r'^create/finish/$', views.create_done, name='create_done'),
]
