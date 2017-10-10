from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.page, {'name': 'index'}, name='homepage'),
]
