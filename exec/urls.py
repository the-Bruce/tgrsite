from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='exec'),
	url(r'^editbio/(?P<pk>[0-9]+)/$', views.editbio, name=
		'exec_editbio'),
	url(r'^editbio/(?P<pk>[0-9]+)/done', views.editbio_done, name='exec_editbio_done'),
]
