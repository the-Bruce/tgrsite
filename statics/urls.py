from django.conf.urls import url
from . import views

# todo: apply this everywhere
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^schedule/$', views.schedule, name='schedule'),
	url(r'^gallery/$', views.gallery, name='gallery'),
	url(r'^larp/$', views.larp_info, name='larp_info'),
	url(r'^larp/lore/$', views.larp_lore, name='larp_lore'),
]
