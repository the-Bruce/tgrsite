from django.conf.urls import url
from . import views

# todo: apply this everywhere
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^schedule/$', TemplateView.as_view(template_name='statics/schedule.html'), name='schedule'),
	url(r'^gallery/$', TemplateView.as_view(template_name='statics/gallery.html'), name='gallery'),
	url(r'^larp/$', TemplateView.as_view(template_name='statics/larp_info.html'), name='larp_info'),
	url(r'^larp/lore/$', TemplateView.as_view(template_name='statics/larp_lore.html'), name='larp_lore'),
]
