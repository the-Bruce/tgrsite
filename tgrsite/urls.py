from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name='tgrsite/index.html'), name='homepage'),
	url(r'^admin/', admin.site.urls),
	url(r'^forum/', include('forum.urls')),
	url(r'^games/', include('rpgs.urls')),
	url(r'^exec/', include('exec.urls')),
	url(r'^', include('users.urls')),
	url(r'^messages/', include('messaging.urls')),
	url(r'^bugs/', include('bugreports.urls')),

	# Pseudo "Static" pages - those with no models or fancy behaviour.
	# e.g. the larp intro page
	url(r'^', include('statics.urls')),

]
