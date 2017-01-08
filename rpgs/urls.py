from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='rpgs'),
	url(r'^(?P<pk>[0-9]+)/$', views.Detail.as_view(), name='rpg'),
	url(r'^join/$', views.Join.as_view(), name='rpg_join'),
	url(r'^create/$', views.create, name='rpg_create'),
	url(r'^create/finish/$', views.create_done, name='create_done')
]