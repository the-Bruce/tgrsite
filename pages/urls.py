from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	# TODO: convert this and all url() calls to path()
	url(r'^$', views.page, {'name': 'index'}, name='homepage'),
	path('schedule', views.page, {'name': 'schedule'}, name='schedule'),
	path('sponsorships', views.page, {'name': 'sponsorships}, name='sponsorships'),
	path('page/<name>', views.page, name='page'),
]
