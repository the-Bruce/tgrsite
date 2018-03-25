from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	# TODO: convert this and all url() calls to path()
	url(r'^$', views.page, {'name': 'index'}, name='homepage'),
	path('page/<name>', views.page, name='page'),
]
