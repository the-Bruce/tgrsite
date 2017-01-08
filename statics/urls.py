from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^schedule/', views.schedule, name='schedule'),
	url(r'^gallery/', views.gallery, name='gallery'),

]
