from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='forum'),
	url(r'^(?P<pk>[0-9]+)/$', views.forum, name='subforum'),
	url(
		r'^thread/(?P<pk>[0-9]+)/(?P<response_id>[0-9]+)/$',
		views.thread,
		name='viewresponse'
	),
	url(
		r'^thread/(?P<pk>[0-9]+)/$',
		views.thread,
		name='viewthread'
	),

	url(
		r'^thread/respond$',
		views.create_response,
		name='createresponse'
	),

	url(r'^thread/create', views.create_thread, name='createthread'),
]
